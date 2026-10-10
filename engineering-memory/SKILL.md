---
name: engineering-memory
description: Maintain a small, auditable, correctable project memory of durable engineering decisions, preferences, constraints, findings, and artifact locations. Recall is read-only; memory supplies leads for revalidation, never current evidence.
---

# Engineering Memory

Reduce repeated investigation without solidifying guesses, sensitive content, or stale conclusions into facts.

## Intelligence Adaptation Contract

- **Hard invariants**: Never record credentials, sensitive account details, or unverified severe conclusions. Memory does not replace current evidence. Never automatically include private memory in public outputs.
- **Mode contracts**: recall, record, and remember are separate actions. Recall is read-only; only record/remember create or modify storage. Recall when relevant and record only durable value.
- **User value priors**: Small, high-signal, auditable, human-correctable memory reduces repetition without noise.
- **Adaptive heuristics**: Select entry count, kind, summary, and recall scope by reuse value and user intent. No lasting value means no recording.
- **Examples and resources**: The bundled `scripts/engineering_memory.py` provides a CLI and JSONL/Markdown storage; equivalent safe project-local sidecars may replace it.

## Capability Load

Self-probe: is recall useful, is the entry auditable and high-signal, does it contain sensitive information, and does skipping recall risk repeated work more than stale memory risks error? Skip|Delta means no write; Light means recall or one note; Full means several events and curation. Uncertainty about privacy or evidence requires review, not fabricated confidence.

## Storage

Default storage is the target project's .memory/engineering directory, containing artifacts.jsonl and per-project Markdown notes. Keep this directory ignored. Verify ignore behavior before writing; do not store runtime data in skill definitions, release sources, or public repositories. The CLI also supports an explicit memory root and ENGINEERING_MEMORY_ROOT; use overrides only within an authorized private boundary.

## Actions

Resolve the installed skill directory before running these commands; bracketed placeholders must be replaced.

```bash
python3 <skill-dir>/scripts/engineering_memory.py recall --project <project-root>
python3 <skill-dir>/scripts/engineering_memory.py record --skill <skill> --project <project-root> --task <task> --summary <summary>
python3 <skill-dir>/scripts/engineering_memory.py remember --project <project-root> --kind decision --text <text>
```

- recall: treat results as candidate checkpoints and revalidate before citing them.
- record: save a small artifact event with important decisions/findings and next actions.
- remember: promote stable decision, finding, preference, or constraint notes, avoiding duplicates.

Do not save entire conversations, unfiltered tool outputs, credentials, emotional judgments, or one-off speculation. Respect a refusal to record and prioritize requested corrections/deletions. Recall only relevant entries. Shared project access can use the same sidecar; missing memory does not block the task or require reconstructing history. Default outputs to English unless the user asks otherwise.
