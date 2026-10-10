# Image generation integration playbook

This is an on-demand method, not a prescribed provider/framework/layout. Choose only relevant sections while preserving authorization and evidence gates.

## Levels and ownership

asset-only suits one-time project assets: persist a selected generated result in the project and wire the consumer. It usually needs no provider, key setup, or CLI. developer-tool suits repeated human work: expose a native entry point for prompt, reference, specification, destination, and resume ID, reusing the provider/client. runtime-provider suits products and automated pipelines: join native registry/service/configuration/secret seams with explicit state, idempotency, timeout, retry, storage, audit, and cost boundaries. Escalate only for durable user value.

## Native boundary inspection

Read project rules, image/asset/publishing entry points, provider/client/transport, configuration, example environment, secret storage, API/payment gates, networking, final asset naming/manifests, consumer code, tests, external-call isolation, and dirty state. Trace:

```text
user/task -> prompt/reference -> provider/client -> submit or synchronous result
          -> state/normalization -> final asset -> actual project consumer
```

Reuse existing owners; introduce abstractions only when no stable seam exists. Preserve still-used legacy paths.

## Current provider contract

Verify endpoint, authentication mechanism/source, model availability, request fields/defaults, supported size/quality, reference formats (URL/data/multipart/file ID), synchronous versus asynchronous behavior, status/terminal error semantics, result URL/base64/envelope, expiry, download, and content type. An OpenAI-like endpoint does not prove compatibility; historical success does not prove current model access.

Credentials may come from authorized environment variables, local ignored configuration, keychain, or native secret providers. Parse only required environment-file values into the process; do not source an untrusted file. Never print keys, place them in CLI arguments/fixtures/manifests/Git, or copy another project's credentials without explicit source authorization. Diagnose presence, source layer, and status code rather than full values. Engineering authorization does not imply paid smoke-test authorization.

Submission returning a task ID creates a durable state authority:

```text
new prompt -> submit once -> task ID -> poll/resume -> terminal response
           -> download/normalize -> stable asset
```

Persist the ID immediately and support continuation. Poll timeout, TLS/client compatibility failure, interrupted process, or download failure does not imply submission failed. Unknown/queued/running state permits recovery only. Correct and resubmit after confirmed terminal failure with no usable asset; a successful but semantically wrong image needs a distinct bounded correction authorized within the total submission budget. Prefer the original result as correction reference when supported.

## Execution workflow

1. Establish pixel ownership from user requirements and whether deterministic postprocessing is allowed. Ask only if the answer changes behavior, cost, or truthfulness.
2. Choose asset-only/tool/runtime and inspect native owners.
3. Verify current protocol with documentation, model discovery, or real responses.
4. Define default provider/model, explicit overrides, permission gate, submit/poll/resume, result normalization, storage, and compatibility in native public-interface tests where appropriate.
5. Implement minimal integration, safe configuration, resume, stable naming, and real consumer wiring. Temporary session output is not a durable project asset.
6. Compile semantic prompts, preflight facts/specification/references, and obey a total submission cap covering candidates, corrections, and failed resubmissions.
7. Recover uncertain attempts before new submissions and consolidate inspected defects into one correction per image rather than serial fragmented edits.
8. Inspect final assets and consumers; report evidence levels and remaining gaps.

## Verification matrix

| Layer | Evidence supports |
|---|---|
| Configuration | Actual defaults and explicit overrides |
| Gate | Disabled/unapproved paths avoid network/payment |
| Protocol | Correct request/state/result handling via fixtures |
| Recovery | Existing IDs resume without duplicate submission |
| Asset | Decodable file, correct format/dimensions |
| Visual | Real inspected semantics, readability, and composition |
| Consumer | Product/page/package actually references the final asset |

Select tests by risk. Cover missing credentials, disabled gates, authorization errors, timeouts, provider failures, submit/query separation, resume, URL/base64 normalization, environment isolation, legacy compatibility, and manifest privacy where applicable. Fixtures do not prove live keys, model permission, service stability, or image quality.

## Semantic prompt package

Use fields needed for the task: text generation versus exact-target edit versus reference guidance; usage and audience; user-visible goal; verified source facts; non-negotiable semantic anchors; core visual relationship/event; verbatim text/numbers/formulas and language; creative freedom; prohibited errors/objects/watermarks; and acceptance conditions.

For new text-only generation, clarify “no reference image required; not an edit” if the API misclassifies it. Transmit intent and semantic boundaries rather than dictating every coordinate, panel count, and color. Reduce and emphasize critical anchors in high-accuracy tasks rather than squeezing a whole document into one image.

When all pixels must be generated, the model also renders exact text/formulas/numbers. Reject core errors and use an authorized full correction request; never cover errors locally and label the result fully generated.

## Preflight and correction

Lock facts/text, dimensions/crop/safe area/readability, possible cross-platform master reuse, reference roles, semantic anchors versus artistic freedom, batch style, and naming. Inspect all defects together; distinguish semantic/text/crop errors from minor aesthetics. Correct only affected images, combine their changes, and inspect the entire corrected result for drift. Correct labels with reversed arrows, geometry, quadrants, contact points, or curves still fail semantics.

## Failure recovery

| Failure | Preferred action | Forbidden shortcut |
|---|---|---|
| Authentication | Check authorized project source and precedence | Print/copy keys |
| Model denied | Verify current availability and authorized model boundary | Silent model switch |
| TLS | Use trusted CA/system certificates | Disable verification |
| Poll failure after submit | Resume original ID; compatible transport may query it | Duplicate submit |
| Terminal text-generation misclassification | Clarify non-edit intent within budget | Resubmit unknown/running attempts |
| Download failure | Download original result again | Generate again |
| Core formula/geometry/identity/fact error | Reject, consolidate, and correct via generation | Hide it with local drawing |
| Missing tools/permission | Report blocker and offline evidence | Claim placeholder validation |

Transport changes cannot bypass authentication, permissions, certificate validation, or cost gates.

## Completion evidence

configured means implementation/configuration exists; fixture-verified means offline protocol tests passed; live-reachable means the service accepted or returned an interpretable response; task-completed means a real successful terminal task; artifact-inspected means visual/content acceptance; consumer-verified means actual project use. Report mode, defaults/overrides, provider/model, entry point, asset/consumer, test/live evidence, recovery, unknowns, checkpoint, and push separately rather than compressing them into “integrated and verified.”
