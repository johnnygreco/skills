# Review Lenses

Use this file as a lens bank, not a fixed role list. The lead agent should combine, split, or specialize these lenses to fit the actual diff.

## Output Format

Reviewers must respond with:

```text
Reviewer: <custom reviewer name>
Lenses: <selected lenses>
Verdict: clean | findings

Findings:
- Severity: blocker | high | medium | low
  File: <path:line or path>
  Issue: <one concrete problem>
  Evidence: <why the diff creates the risk>
  Fix: <specific change that would address it>

Notes:
- <optional uncertainty, skipped areas, or validation run>
```

If there are no findings, return `Verdict: clean` and omit the findings list.

## Shared Rules

- Review only the target diff and directly related code.
- Prefer a small number of high-confidence findings over long nit lists.
- Cite files and lines when possible.
- Read adjacent code before claiming a bug.
- Distinguish hard bugs from judgment calls.
- Do not edit files.
- Do not approve based only on tests passing.
- Do not flag issues that existing tooling already enforces unless the tooling is missing or misconfigured.
- Flag compatibility breaks only when the user asked for backward compatibility or the target packet states compatibility is in scope.
- Do not flag intentionally deferred behavior named as a non-goal unless the current target creates a concrete blocker for it.

## Core Lenses

Always consider these lenses while designing the panel. They do not each need a separate reviewer.

### Robustness And Correctness

Look for behavior bugs, likely regressions, brittle error paths, missing edge-case handling, stale state, incorrect async ordering, bad retries, cancellation problems, idempotency bugs, compatibility breaks, and contradictions with the issue, PR, spec, or surrounding code contract.

### Maintainability And Complexity Discipline

Guard strictly against over-engineering and unnecessary complexity. Look for abstractions that do not earn their keep, generic machinery hiding simple data shapes, clever or magical code, scattered special cases, duplicated concepts, needless optionality, cast-heavy boundaries, wrapper layers, misplaced ownership, and files or components becoming less cohesive.

Prefer feedback that simplifies the model, removes moving parts, or moves logic to the canonical owner. Do not ask for a refactor merely because a different structure is possible.

### Tests And Coverage

Look for missing tests around changed behavior, regressions, permissions, edge cases, error paths, migrations, and integration points. Check whether tests assert behavior instead of implementation details, whether mocks or snapshots hide the real risk, and whether relevant validation was rerun after fixes. A test for a required case should fail if that case is removed; be wary of expected values derived from the same implementation constant they are meant to guard.

### Security And Privacy

Look for concrete risks in authentication, authorization, tenant isolation, injection, path traversal, SSRF, XSS, CSRF, unsafe redirects, deserialization, command execution, secret handling, sensitive logging, telemetry, external API trust boundaries, weakened validation, and unsafe defaults.

Report only risks tied to a changed code path or a missing mitigation the project normally relies on.

### User And Agent Experience

For user-facing changes, review workflow clarity, accessibility, keyboard and focus behavior, responsive layout, loading and error states, copy, discoverability, and whether the UI helps users recover from mistakes.

For agent-facing or developer-tool changes, review prompt surfaces, tool ergonomics, error messages, deterministic behavior, observability for debugging, instruction clarity, and whether future agents can use the workflow without hidden context.

### Documentation And Adoption

Apply when the change affects user behavior, APIs, configuration, operations, workflows, generated artifacts, or maintainer expectations. Look for missing docs, README updates, changelog notes, examples, migration guidance, runbooks, or comments explaining non-obvious invariants.

## Optional Lenses

Use these only when the diff has the relevant risk.

### Data And Migrations

Review schema changes, migrations, backfills, data retention, indexing, locking, transactionality, reversibility, and compatibility between old and new application versions.

### Performance And Concurrency

Review hot paths, algorithmic complexity, batching, caching, parallelism, locks, race conditions, memory pressure, and slow external calls.

### API Contracts

Review public APIs, SDKs, generated types, backwards compatibility, request and response validation, error semantics, and versioning.

### Integration And Operations

Review deployment safety, rollouts, feature gates, cache invalidation, rollback behavior, observability, environment assumptions, packaging, generated artifacts, queues, events, and downstream compatibility. For release/packaging changes, inspect the actual publish path and the produced artifact's tags, metadata, and target-registry constraints; a green local build or metadata lint does not prove the artifact is publishable.

### Dependency And Supply Chain

Review new or changed dependencies, lockfiles, build scripts, code generation, package provenance, permissions, maintenance risk, and license concerns.

### Native Extensions And FFI Boundaries

For native extensions, FFI, plugins, generated bindings, or host-language integration, review user-controlled sizes, allocation and growth/reserve paths, panic/error translation, and resource limits. A panic wrapper does not cover every abort or out-of-memory path; exposed constructors and capacity APIs should use bounded or fallible allocation and surface host-language errors rather than crashing the process.
