# Private identity input template

This distributed template is empty. Fill values only in an authorized ignored private audit workspace, never inside the installed skill or public repository. Values can be sensitive even when they are not credentials. Do not print matched secrets in reports.

```text
Intended public display name:
Allowed public author/committer emails:
Private real names/aliases:
Corporate and personal email domains requiring review:
Private project names/codenames:
Private tool names:
Internal service hosts and private remote URLs:
Machine-specific user and volume identifiers:
Explicitly public identity exceptions with source evidence:
```

Infer public identity from repository-local configuration, README/license, existing policy, and user intent. An explicitly authorized public identity is not a leak just because it is personal. An empty/unavailable private-token list is coverage debt: generic patterns cannot prove that unknown private codenames are absent.

Use exact/escaped patterns for known private tokens. Generic words such as internal, private, confidential, token, and password are review triggers: language keywords, safety explanations, regex definitions, and placeholders are not automatically findings. Name each false-positive guard and the visitor-visible harm before assigning severity.
