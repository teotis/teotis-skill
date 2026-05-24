# Quality Checklist

Run this checklist before delivery. Failures should be corrected or clearly disclosed.

## Purpose and Mode

- [ ] HTML materially improves orientation, comprehension, inspection, actionability, or feedback — or was explicitly requested.
- [ ] The smallest appropriate presentation mode was selected.
- [ ] A concise chat answer accompanies the artifact when important conclusions exist.

## Reading Experience

- [ ] The first viewport states the answer, recommendation, task state, or review objective.
- [ ] Headings are meaningful and correctly nested.
- [ ] Long detail is progressively disclosed without hiding critical risk or uncertainty.
- [ ] Tables/comparisons align criteria and include a takeaway.
- [ ] The page is usable on narrow screens and printable where relevant.

## Accessibility

- [ ] Correct `lang`, descriptive `<title>`, viewport, semantic landmarks, and skip link.
- [ ] All functionality works with keyboard/single-click alternatives; drag is not required.
- [ ] Focus is visible and not obscured by sticky controls.
- [ ] Touch/click targets are at least 24 by 24 CSS pixels.
- [ ] Diagrams/charts include accessible text interpretation or data equivalent.
- [ ] Reduced-motion preference is respected.

## Offline, Performance, and Packaging

- [ ] Offline-first output contains no undeclared CDN or remote dependency.
- [ ] Single-file output is not bloated by excessive embedded page images; large previews use a local bundle.
- [ ] The user receives a durable link/path and any sharing requirements for bundled assets.

## Security and Privacy

- [ ] Untrusted content is escaped; no uncontrolled HTML/script injection.
- [ ] No `eval`, `new Function`, `javascript:` URLs, or inline event-handler attributes.
- [ ] CSP is included or omission is explicitly justified.
- [ ] No unnecessary secrets, private source data, or hidden instructions are embedded.
- [ ] User feedback can be cleared; local persistence handles failure safely.

## Feedback and Continuation

- [ ] Feedback controls match the user's task rather than using generic decisions everywhere.
- [ ] Review units have stable IDs and exported feedback preserves them.
- [ ] Clipboard has a manual-copy fallback.
- [ ] Exported continuation text never authorizes changes/actions the user has not explicitly approved.

## Technical Check

Where the validation script is present, run:

```bash
python3 <skill-path>/scripts/validate_html.py <generated_html_path>
```

Treat the script as a minimum lint pass, not a substitute for reading and testing the page.
