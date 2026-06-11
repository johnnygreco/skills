# Kata Goal Delivery Templates

Copy these skeletons into temporary files for `kata create --body-file` or `kata comment --body-file`. Fill every field; delete a line only when it genuinely does not apply.

When a body or comment contains multiline markdown, backticks, `$`, quotes, or command output, write it from a file or stdin rather than an inline shell string, then reread with `kata show <ref> --agent` to confirm the content survived.

## Parent Tracker Issue

Title: `Kata goal delivery: <goal>`

```markdown
## Goal
<one-paragraph statement of the overall objective>

## Source Of Truth
Governing sources, in order, when instructions conflict:
1. Active user goal and explicit user corrections.
2. This Kata parent tracker and its comments.
3. The active child issue scope and comments.
4. Named plan/spec/design docs.
5. Repo docs, local skills, and historical behavior.
Record any material conflict and the chosen precedence here.

## Shared Context
<facts every child issue needs: architecture, conventions, key decisions; state "backward compatibility is not required" unless the user explicitly required it>

## Definition Of Done
<observable conditions that mean the whole goal is complete; state whether release, publish, README, migration, and user-facing docs are in or out of scope>

## Validation Strategy
<the exact commands every child should run: test / lint / build / type-check / docs / screenshots>
- test: `<command>`
- lint: `<command>`
- build: `<command>`

## Risks
<known risks and how to mitigate or watch them>

## Issue Graph
Kata relationships are authoritative. Draft child plan, in dependency order:
- <draft child title> - dependencies: <none | prior child title>
- <draft child title> - dependencies: <prior child title>

## Integration Notes
<how the pieces fit together; cross-child contracts>

## Current State
Live updates are tracker comments. The latest `Current State` comment is authoritative for handoff.

## Final Status
<filled during the Final Pass: summary, validation evidence, review evidence, known risks>
```

## Child Implementation Issue

Title: `<short imperative title>`

```markdown
## Objective
<what this child accomplishes and the expected outcome>

## Context
- Tracker: <tracker-ref>
- Self-contained context: <summarize enough architecture, conventions, decisions, and constraints to implement without hidden chat history>
- Supporting links: <optional docs, files, designs, logs, prior issue refs, or commits>

## Scope
- In scope: <what to do>
- Non-goals: <what explicitly not to do here>
- Backward compatibility: do not worry about it unless explicitly specified; do not preserve legacy behavior, add shims, or frame work as legacy support by default
- Dependencies: <Kata refs that must close first, or "none">
- Sequencing: <where this sits in the order>

## Implementation Notes
<relevant files, APIs, commands, data contracts, design constraints>

## Acceptance Criteria
- [ ] <observable, testable condition>
- [ ] <observable, testable condition>

## Required Validation
<commands to run and what a pass looks like; screenshots or logs when useful>

## Review Expectations
<review lenses, local diff or PR expectations, screenshots/logs/perf numbers, known tricky areas>
```

Create children with the tracker as parent and explicit blockers:

```sh
kata create "<short imperative title>" \
  --parent <tracker-ref> \
  --blocked-by <previous-child-ref> \
  --label goal-delivery \
  --label "goal-<goal-slug>" \
  --body-file <child-body-file> \
  --idempotency-key "kata-goal-delivery-<tracker-ref>-<child-slug>" \
  --agent
```

Omit `--blocked-by` for the first child or independent process children.

## Current State Comment

Post this on the tracker before handoff, after issue start, review completion, close, blocker discovery, and plan changes.

```markdown
## Current State
Active child / owner / branch:
Active review target:
Last closed child / commit:
Validation status:
Review status:
Blockers:
Next action:
Issue graph changes:
```

## Review Record Comment

Post this on the child issue after review converges and before close. The record is durable proof that review happened and lets a later reader reproduce exactly what was reviewed.

```markdown
## Review Record

Kata issue: <child-ref>
Review surface: <local diff | branch | commit range | PR URL>
Frozen target: `<base-ref> <base-sha>..<head-ref> <head-sha>`
Diff command: `<exact command that reproduces the reviewed diff>`

Panel:
- <reviewer name>: <lenses> -> clean | findings
- <reviewer name>: <lenses> -> clean | findings
Skipped Review-Standard lenses: <lens - one-line reason each, or "none">

Accepted findings fixed:
- <finding -> fix>

Rejected findings:
- <finding -> why rejected: intentional / speculative / out of scope / not a bug>

Validation after fixes:
- <command> -> <result>

Final status: <all rerun reviewers clean | exact unresolved blocker>
```

For a single-reviewer review, the panel is just one line and the skipped lenses must still be explicit.

## Final Status Comment

Post this on the tracker before closing it.

```markdown
## Final Status
Summary:
Closed children:
- <child-ref> <title> - <commit/evidence>

Final review:
<holistic review surface, reviewers, and status>

Final validation:
- <command> -> <result>

Known risks or follow-ups:
- <none | non-blocking follow-up refs and rationale>

Completion proof:
<why the original goal's definition of done is satisfied>
```
