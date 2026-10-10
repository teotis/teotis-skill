---
name: public-release-sweep
description: Audit public-release safety across Git identity and secrets, tracked files, private references, binary metadata, licensing, configuration, and private/public synchronization. Produce an Exposure Map, coverage debt, visitor evidence, and a bounded release verdict; analysis-only by default.
---

# Public Release Sweep

Judge what a real visitor can discover from a repository, public mirror, or release package. A completed checklist is not evidence of the actual published state or permission to claim safety.

## Intelligence Adaptation Contract

- **Hard invariants**: Analysis-only by default; applicable dimensions need coverage or explicit debt. P0/HIGH findings require concrete evidence and a visitor scenario. Verify actual public state and respect verdict permission. Destructive operations require explicit action-specific authorization.
- **Mode contracts**: Only a formal audit may grant a bounded safe-to-publish verdict. Quick/targeted work may stop early with unexamined dimensions and no comprehensive safety claim.
- **User value priors**: Prevent visitor-visible identity/credential leaks and private/public drift with useful evidence rather than noisy keyword checklists.
- **Adaptive heuristics**: Dimension order, tools, report shape, and handoff granularity follow repository shape and risks.
- **Examples and resources**: `references/full-workflow.md` provides commands, visitor scenarios, severity, and fix gates. `references/private-identity-template.md` provides an empty private-input template; never publish a filled copy. New exposure surfaces must enter the verdict even if absent from the catalog.

## Capability Load

Self-probe: what exposure dimensions apply, how will history/secrets/private paths be covered, what evidence supports a safety verdict, and what could be missed by stopping early? Skip|Delta for a single known risk; Light for targeted triage with debt; Full for a formal multidimensional verdict. Uncertainty about consequential exposure calls for Full coverage, not a stronger claim.

## Authorization

An explicit audit request or a necessary release-safety judgment permits analysis. It does not itself permit commits, pushes, publication, deletion, history rewriting, or credential operations. Reuse existing authorization when it covers specific repairs or publication; never reinterpret generic cleanup as permission for irreversible history rewriting. Implement authorized content repairs without inventing a second approval gate.

## Standalone Investigation Contract

This local projection of investigation-kernel@v1 and public-safety-verdict@v1 is self-contained. Build an Exposure Map first covering target/nested repositories, remotes, actual public state, history, inventory, content, metadata, license, configuration, and synchronization. Formal artifacts may live under the target project's reports/public-release-sweep directory. Central maintainer contracts and companion skills are not runtime dependencies.

Track evidence as verified/inference/unknown/blocked/missing evidence; task state as task-success/partial/awaiting-user/failed/workspace-dirty; release state as candidate, ready-to-publish, stored-locally, uploaded, published, or withdrawn. These axes are independent. Local cleanliness does not imply safety, and readiness does not imply publication.

Record remote/tool/identity/mirror gaps as coverage debt. Address every applicable dimension before any formal verdict; blocked/deferred exposure-relevant dimensions prevent an unqualified safe verdict. Missing HTML tools permit Markdown/chat with identical evidence. Missing metadata tools do not permit a clean metadata claim.

## Adaptive Audit

1. Establish publication model, target, intended public identity, and current remote state.
2. Cover Git identity; historical secrets; tracked inventory; private references; binary metadata; license/legal; configuration/environment; and synchronization.
3. Each finding names file/commit/content, visitor scenario, confidence, false-positive guard, verdict impact, lifecycle, and authorized fix boundary.
4. Include memory residue, generated reports, registry/provenance, and any other newly observed surface.
5. Review marginal information gain before expanding scope; budget exhaustion lowers coverage and claim strength, never the evidence threshold.

## Output and Claim Permission

Default to English unless requested otherwise. Deliver Exposure Map, findings, coverage debt, verdict permission, and an authorized repair handoff when useful. Negative findings are valuable evidence. Formal Markdown and optional HTML share stable IDs and conclusions; artifacts must be independently understandable.

No concrete visitor evidence plus incomplete applicable coverage means no safe-to-publish claim. Never publish known real credentials or unintended private identity. Credential rotation happens at the issuing service; removing text alone is insufficient. History rewriting needs explicit authorization, backup/recovery boundaries, and published-state revalidation.
