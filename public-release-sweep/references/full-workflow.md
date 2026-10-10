# Public release audit methods

Use these methods proportionately. A targeted scan may end with debt and a limited claim; a formal release verdict requires all applicable dimensions and actual visitor evidence. Additional exposure surfaces enter the ledger even if absent below.

## Scope and evidence map

Establish target repository, independent mirrors/nested repositories, release package, intended public identity, remote/default branch, current publication state, and requested scope. Infer facts from current evidence and ask only if a consequential target or authorization boundary cannot be established.

For each dimension record surface, evidence/action, result state, finding IDs, debt, and verdict impact. Each finding includes file/line or commit, exposed type, visitor scenario, severity/confidence, false-positive guard, lifecycle, and authorized fix boundary. An external visitor can inspect files, clone reachable history/tags, read authorship, download binaries, and follow links: reproduce the relevant scenario rather than relying on ignore rules.

## 1. History identity

```bash
git log --all --format='%an <%ae>'
git log --all --format='%cn <%ce>'
git config --local --get user.name
git config --local --get user.email
```

Deduplicate identities and compare with intended public identity, allowed exceptions, private names, and corporate/personal domains from the private template. A currently correct config cannot clear historical metadata. Missing private identity input remains debt. Distinguish intentionally public authorship from unintended private/corporate identity.

## 2. History secrets

Use available trusted scanners or bounded Git/object scanning without printing credentials. Scan current files and reachable historical blobs/commit messages across branches/tags, not just HEAD. Credential-pattern definitions and synthetic examples need explicit false-positive review. Generic password/token words prompt inspection rather than prove a secret.

An illustrative pattern-based candidate search is:

```bash
git log --all -G 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16}|-{5}BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY' --format='%H %s'
```

This only locates candidate changes; it is not a comprehensive scanner. Inspect candidate blobs privately, record locations and redacted evidence, and consider service-specific tokens, signing keys, passwords, internal endpoints, and connection strings. A real exposed credential requires issuer-side rotation; removing it from a file does not revoke it.

## 3. Tracked inventory

```bash
git ls-files
git status --short
git ls-files '*.apk' '*.ipa' '*.zip' '*.jar' '*.war' '*.pem' '*.key'
```

Review agent instructions, internal governance, plans/reports/specs, runtime memory, private tooling, local settings, environment files, cache/system noise, and unreleased assets. Evaluate context: an intentional public example may be legitimate, while actual private governance is not. Untracked/ignored files can still be accidentally staged or packaged. Use explicit approved paths, never bulk staging in a dirty workspace.

## 4. Content and references

Scan all release text plus historical versions where publication scope requires it for machine-specific paths, private identity/tokens/tools/hosts/remotes, sensitive case studies, Chinese residue in English-only packages, hidden language defaults, and unresolved dependencies. Known private patterns must come from private inputs, not be hardcoded into the public skill.

Review low-confidence internal/private/confidential terms in context. Language keywords and descriptions of safety policy are not disclosure. The visitor scenario must explain what unintended information becomes discoverable. Check Markdown/HTML links and template defaults, not only entry files.

## 5. Binary and metadata

```bash
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)'
```

Identify large/historical binaries and inspect image EXIF, document author/creator, embedded paths, archives, debug builds, and generated artifacts with available tools. Classify SVG/HTML as readable content when applicable. No applicable binary means not-applicable with inventory evidence; missing metadata tools for actual binaries means blocked/debt, never clean.

## 6. License and legal

Check root LICENSE, notices/copyright identity and year, package ownership, copied dependencies, assets, and upstream license requirements. Placeholder notices and missing/incorrect licenses need repair. A repository license does not automatically establish rights to third-party content. Legal uncertainty remains explicit rather than invented clearance.

## 7. Configuration/environment

Review tracked environment/local settings, example configs, endpoints, tool declarations, hidden metadata, and ignore rules. Ensure example files contain placeholders, not values usable as credentials. Public adapter metadata can enhance use but must not become a hard dependency for the core workflow.

## 8. Synchronization and portability

For split repositories verify independent Git roots, explicit approved package allowlist, public author identity, public source equality, dependency closure, English/privacy/license gates, and exact staging. Never copy the whole private repository or skill tree for convenience. Include only public-required references/scripts/assets, excluding internal reports/evals/configuration unless separately authorized and audited.

A single copied skill directory must retain safety/evidence/claim gates. Every required resource exists inside it with no escaping symlink. Companion tools/skills are optional with fallback in the same paragraph. Maintainer contracts must not become runtime dependencies. Script fixtures or static examples do not prove live behavior.

## Additional surfaces

Check runtime memory, generated reports, private registry metadata, release provenance, conversation residue, inferred author identity, and links to sensitive source material. Update the Exposure Map rather than declaring the eight-item list exhaustive.

## Severity, debt, and verdict

P0: concrete live credential/key or equivalent blocking exposure. HIGH: unintended private identity/internal material with a real visitor scenario. MEDIUM: contextual concern requiring review. LOW: optional improvement. General words or placeholders alone do not support P0/HIGH.

Evidence is verified/inference/unknown/blocked/missing evidence. Task progress is independent of release lifecycle: candidate -> ready-to-publish -> stored-locally -> uploaded -> published/withdrawn. A push needs remote verification; local HEAD alone is not published-state evidence. Readiness is scoped to inspected refs/package/commit, not every unseen fork or branch.

Formal safety requires actual public-state evidence, all applicable dimensions addressed, no unresolved blocking exposure, and no exposure-relevant blocked/deferred debt. A targeted audit names unexamined dimensions and gives no comprehensive safe verdict. Budgets may reduce claim strength, never safety evidence thresholds.

## Reports and repair boundary

Use an independently understandable project-local Markdown Exposure Map with stable dimension/finding IDs, visitor evidence, positive results, debt, verdict, lifecycle, and next action. Optional HTML shares the same conclusions and offers navigation/evidence; plain Markdown is a complete fallback without a companion skill. Do not include private inputs or credentials in public reports.

Audit authorization permits analysis only. Existing explicit authorization may cover content edits, exact staging/commits, push, or publication: reuse it within scope. Destructive history rewrites, force pushes, credential rotation, and data-loss operations need explicit specific authorization; generic cleanup does not grant it. Back up recoverable refs outside the public push set before authorized rewrites and re-audit rewritten and actual remote history afterward. Never publish known real secrets or unintended private identity.
