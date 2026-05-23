# Optimization Notes: From HTML Delivery to Adaptive HTML Response

## Design change

The original package is valuable for file annotation and long report review, but its activation model is output-type-driven: file,
long text, or mixed. The revised package turns it into a universal response presentation policy. It can represent any agent reply,
while generating HTML only when the medium reduces cognitive or feedback cost.

## Main changes

| Original behavior | Revised behavior | Reason |
|---|---|---|
| Trigger based mainly on files or long text | Trigger based on comprehension/review value with explicit scoring | Short decisions may deserve HTML; long simple prose may not |
| File Review / Text Report / Dual only | Eight task-oriented modes | Covers decisions, plans, explanations, evidence, technical and artifact review |
| Generic decision panel | Mode-specific feedback vocabulary | Feedback reflects what user is doing |
| Claims self-contained HTML but mandates Mermaid CDN | Offline-first, inline SVG/CSS default; online enhancement only when declared | Removes internal contradiction |
| Base64 page embedding as default | Portable single file vs local review bundle | Avoids huge unusable HTML files |
| Clipboard assumed | Clipboard plus manual-copy/download fallback | Local HTML/browser permissions vary |
| Limited accessibility constraints | Keyboard alternatives, target size, focus, reduced motion, semantic structure | Lower reading and interaction barriers |
| Export may imply action | Safe continuation directive; no unauthorised execution | Feedback must not silently grant permission |
| No validation helper | Added `validate_html.py` | Fast quality/safety lint before delivery |

## Retained strengths

- Browser-first review experience.
- Page/region annotation for rendered artifacts.
- Feedback persistence and export.
- Local browser opening and preview-conversion helpers.
