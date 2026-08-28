#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PLAN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
ORCHESTRATE="$SCRIPT_DIR/orchestrate.sh"

run_orchestrate() {
  ORCHESTRATION_EXECUTION_PLATFORM=opencode ORCHESTRATION_RUNNER=opencode bash "$ORCHESTRATE" "$@"
}

usage() {
  cat <<EOF
Usage: $(basename "$0") [start|doctor|status|sessions|advance|retry|finalize|cleanup|mark-state|repair-state|collect-logs|verify-package|verify-finalize|scratch-path|bind-platform|compatibility|migrate|handoff] [args...]

Default:
  $(basename "$0") start

OpenCode helpers:
  $(basename "$0") sessions
  $(basename "$0") resume <session-id>
EOF
}

cmd="${1:-start}"
[ "$#" -eq 0 ] || shift

case "$cmd" in
  start)
    run_orchestrate doctor --environment
    run_orchestrate start
    run_orchestrate status
    cat <<EOF

OpenCode runner evidence:
  tail -f "$PLAN_ROOT/status/launch-<package-id>.log"
  $(basename "$0") sessions
  $(basename "$0") resume <session-id>

Continue only on the bound OpenCode platform. No Codex or Claude fallback is selected.
EOF
    ;;
  doctor)
    if [ "$#" -eq 0 ]; then
      run_orchestrate doctor --environment
    else
      run_orchestrate doctor "$@"
    fi
    ;;
  status|advance|retry|finalize|cleanup|mark-state|repair-state|collect-logs|verify-package|verify-finalize|scratch-path|bind-platform|compatibility|migrate|handoff)
    run_orchestrate "$cmd" "$@"
    ;;
  sessions)
    opencode session list
    ;;
  resume)
    session_id="${1:-}"
    [ -n "$session_id" ] || { usage >&2; exit 2; }
    opencode run --format json --session "$session_id"
    ;;
  help|--help|-h)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
