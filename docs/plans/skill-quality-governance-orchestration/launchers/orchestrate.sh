#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PLAN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel)"
GRAPH="$SCRIPT_DIR/package-graph.tsv"
STATE="$PLAN_ROOT/status/state.tsv"
PROMPTS="$SCRIPT_DIR/agent-prompts.md"
LOCKDIR="$PLAN_ROOT/status/.orchestrate.lock"
MAX_PARALLEL="${ORCHESTRATION_MAX_PARALLEL:-10}"

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

log() {
  printf '%s\n' "$*"
}

rows() {
  awk -F '\t' 'FNR == 1 { next } NF { print }' "$GRAPH"
}

field_for() {
  local pkg="$1"
  local idx="$2"
  awk -F '\t' -v pkg="$pkg" -v idx="$idx" 'FNR == 1 { next } $1 == pkg { print $idx; exit }' "$GRAPH"
}

state_of() {
  local pkg="$1"
  awk -F '\t' -v pkg="$pkg" 'FNR == 1 { next } $1 == pkg { print $2; exit }' "$STATE"
}

set_state() {
  local pkg="$1"
  local new_state="$2"
  local tmp
  local now
  tmp="$(mktemp)"
  now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  awk -F '\t' -v OFS='\t' -v pkg="$pkg" -v new_state="$new_state" -v now="$now" '
    NR == 1 { print; next }
    $1 == pkg {
      $2 = new_state
      if (new_state == "launched" || new_state == "in_progress" || new_state == "finalizing") $3 = now
      if (new_state == "completed" || new_state == "finalized" || new_state == "blocked") $4 = now
    }
    { print }
  ' "$STATE" > "$tmp"
  mv "$tmp" "$STATE"
}

ensure_state_rows() {
  local tmp
  tmp="$(mktemp)"
  cp "$STATE" "$tmp"
  while IFS=$'\t' read -r pkg _status_file _status_path _deps _dep_type _wave branch worktree _manual _finalize; do
    if ! awk -F '\t' -v pkg="$pkg" 'FNR > 1 && $1 == pkg { found = 1 } END { exit found ? 0 : 1 }' "$tmp"; then
      printf '%s\tpending\t\t\tagent\t%s\t%s\t\t\t\t\t\t\n' "$pkg" "$branch" "$worktree" >> "$tmp"
    fi
  done < <(rows)
  mv "$tmp" "$STATE"
}

preflight() {
  [[ -f "$GRAPH" ]] || die "missing graph: $GRAPH"
  [[ -f "$STATE" ]] || die "missing state: $STATE"
  [[ -f "$PROMPTS" ]] || die "missing prompts: $PROMPTS"

  awk -F '\t' '
    FNR == 1 { next }
    seen[$1]++ { printf("duplicate package id: %s\n", $1) > "/dev/stderr"; bad = 1 }
    $10 == "1" { finalize++ }
    END {
      if (finalize != 1) {
        printf("expected exactly one finalize package, found %d\n", finalize) > "/dev/stderr"
        bad = 1
      }
      exit bad ? 1 : 0
    }
  ' "$GRAPH"

  awk -F '\t' '
    FNR == 1 { next }
    { exists[$1] = 1; deps[$1] = $4 }
    END {
      for (pkg in deps) {
        if (deps[pkg] == "") continue
        n = split(deps[pkg], parts, ",")
        for (i = 1; i <= n; i++) {
          dep = parts[i]
          gsub(/^ +| +$/, "", dep)
          if (dep != "" && !(dep in exists)) {
            printf("missing dependency: %s depends on %s\n", pkg, dep) > "/dev/stderr"
            bad = 1
          }
        }
      }
      exit bad ? 1 : 0
    }
  ' "$GRAPH"
}

deps_satisfied() {
  local deps="$1"
  local dep
  [[ -z "$deps" ]] && return 0
  IFS=',' read -ra dep_array <<< "$deps"
  for dep in "${dep_array[@]}"; do
    dep="${dep#"${dep%%[![:space:]]*}"}"
    dep="${dep%"${dep##*[![:space:]]}"}"
    [[ -z "$dep" ]] && continue
    case "$(state_of "$dep")" in
      completed|finalized) ;;
      *) return 1 ;;
    esac
  done
  return 0
}

has_bad_state() {
  awk -F '\t' 'FNR > 1 && ($2 == "blocked" || $2 == "stale" || $2 == "invalid") { found = 1 } END { exit found ? 0 : 1 }' "$STATE"
}

all_functional_completed() {
  local incomplete=0
  while IFS=$'\t' read -r pkg _doc _status deps _dep_type _wave _branch _worktree _manual finalize; do
    if [[ "$finalize" != "1" && "$(state_of "$pkg")" != "completed" ]]; then
      incomplete=1
    fi
  done < <(rows)
  [[ "$incomplete" == "0" ]]
}

launch_agent() {
  local pkg="$1"
  local name="teotis-${pkg}"
  local msg
  msg="Execute package ${pkg}. Read ${PLAN_ROOT}/INDEX.md and ${PLAN_ROOT}/packages/${pkg}.md. Update ${PLAN_ROOT}/status/${pkg}.md and ${STATE}. End by calling ${SCRIPT_DIR}/orchestrate.sh advance --from ${pkg}."

  if ! command -v claude >/dev/null 2>&1; then
    log "claude command not found; leaving ${pkg} ready for manual execution from ${PROMPTS}"
    set_state "$pkg" ready
    return 0
  fi

  set_state "$pkg" launched
  (cd "$REPO_ROOT" && claude --bg --name "$name" "$msg")
  log "launched ${pkg} as ${name}"
}

launch_ready() {
  local launched=0
  while IFS=$'\t' read -r pkg _doc _status deps _dep_type _wave _branch _worktree _manual finalize; do
    [[ "$finalize" == "1" ]] && continue
    [[ "$launched" -ge "$MAX_PARALLEL" ]] && break
    case "$(state_of "$pkg")" in
      pending|ready)
        if deps_satisfied "$deps"; then
          launch_agent "$pkg"
          launched=$((launched + 1))
        fi
        ;;
    esac
  done < <(rows)
  log "ready launch pass complete; attempted ${launched} package(s)."
  log "view agents with: claude agents --cwd \"$REPO_ROOT\""
}

launch_finalize() {
  local pkg="99-finalize"
  case "$(state_of "$pkg")" in
    finalized)
      log "99-finalize already finalized."
      ;;
    launched|in_progress|finalizing)
      log "99-finalize already launched."
      ;;
    *)
      set_state "$pkg" ready
      launch_agent "$pkg"
      ;;
  esac
}

status_cmd() {
  awk -F '\t' '
    FNR == 1 {
      printf "%-34s %-12s %-55s %-24s %s\n", "PACKAGE", "STATE", "BRANCH", "VERIFICATION", "LAST_ERROR"
      next
    }
    {
      printf "%-34s %-12s %-55s %-24s %s\n", $1, $2, $6, $10, $13
    }
  ' "$STATE"
}

start_cmd() {
  preflight
  ensure_state_rows
  launch_ready
}

advance_cmd() {
  preflight
  ensure_state_rows
  if has_bad_state; then
    status_cmd
    die "blocked/stale/invalid package present; not unlocking downstream work"
  fi
  if all_functional_completed; then
    launch_finalize
  else
    launch_ready
  fi
}

retry_cmd() {
  local pkg="${1:-}"
  [[ -n "$pkg" ]] || die "usage: orchestrate.sh retry <package-id>"
  case "$(state_of "$pkg")" in
    blocked|stale|invalid)
      set_state "$pkg" pending
      log "reset ${pkg} to pending"
      ;;
    *)
      die "retry only supports blocked, stale, or invalid packages"
      ;;
  esac
}

finalize_cmd() {
  preflight
  ensure_state_rows
  if ! all_functional_completed; then
    status_cmd
    die "cannot finalize until every functional package is completed"
  fi
  launch_finalize
}

usage() {
  cat <<USAGE
Usage: bash launchers/orchestrate.sh <command>

Commands:
  start
  advance [--from <package-id>]
  status
  retry <package-id>
  finalize
USAGE
}

main() {
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    start) start_cmd ;;
    advance) advance_cmd ;;
    status) status_cmd ;;
    retry) retry_cmd "${1:-}" ;;
    finalize) finalize_cmd ;;
    *) usage; exit 2 ;;
  esac
}

mkdir "$LOCKDIR" 2>/dev/null || {
  if [[ "${1:-}" == "status" ]]; then
    main "$@"
    exit $?
  fi
  die "another orchestration command is running: $LOCKDIR"
}
trap 'rmdir "$LOCKDIR"' EXIT
main "$@"

