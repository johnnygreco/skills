# GitHub Goal Delivery Templates

Copy-paste skeletons for the progress tracker issue, implementation issues, and pull requests. Fill every field; delete a line only when it genuinely does not apply, and explain why if that omission affects implementation or review.

## Progress Tracker Issue

Title: `GitHub goal delivery: <goal>`

```markdown
## Goal
<one-paragraph statement of the overall objective>

## Shared Context
<facts every implementation issue needs: architecture, conventions, key decisions; state "backward compatibility is not required" unless the user explicitly required it>

## Definition of Done
<observable conditions that mean the whole goal is complete>

## Validation Strategy
<the exact commands every issue must run: test / lint / build / type-check>
- test: `<command>`
- lint: `<command>`
- build: `<command>`

## Risks
<known risks and how we mitigate or watch them>

## Issue Checklist (dependency order; replace draft titles with issue links)
- [ ] <draft issue title>
- [ ] #<issue-number> <short issue title>

## Integration Notes
<how the pieces fit together; cross-issue contracts>

## Final Status
<filled in during the Final Pass: summary, validation evidence, known risks>
```

## Implementation Issue

Title: `<short imperative title>`

```markdown
## Objective
<what this issue accomplishes and the expected outcome>

## Context
- Tracker: #<tracker-issue-number>
- Self-contained context: <summarize enough architecture, conventions, decisions, and constraints to implement without hidden chat history>
- Supporting links: <optional links to tracker sections, docs, files, designs, logs, or prior PRs>

## Scope
- In scope: <what to do>
- Non-goals: <what explicitly NOT to do here>
- Backward compatibility: do not worry about it unless explicitly specified; do not preserve legacy behavior or add shims by default
- Dependencies: <#issues that must merge first, or "none">
- Sequencing: <where this sits in the order>

## Implementation Notes
<relevant files, APIs, commands, data contracts, design constraints>

## Acceptance Criteria
- [ ] <observable, testable condition>
- [ ] <observable, testable condition>

## Required Validation
<commands to run and what a pass looks like; screenshots or logs when useful>

## PR Expectations
<anything the reviewer will need: screenshots, logs, perf numbers>
```

## Pull Request

```markdown
## Summary
<what changed and why, in a few sentences>

Closes #<issue-number>

## Validation
<exact commands run and their results>
- test: `<command>` -> <result>
- lint: `<command>` -> <result>

## Risks
<what could go wrong; blast radius; rollout/migration notes>

## Reviewer Notes
<where to focus; tricky decisions; anything intentionally out of scope; state whether backward compatibility was explicitly required>
```

## Review Record

Post this on the PR once review converges, before merge. It is the durable proof that review happened and lets a later reader reproduce exactly what was reviewed. Use this single shape whether the review came from the panel-review skill or from fresh reviewer agents.

```markdown
## Review Record

Frozen target: `<base-ref> <base-sha>..<head-ref> <head-sha>`
Diff command: `<exact command that reproduces the reviewed diff>`

Panel:
- <reviewer name>: <lenses> -> clean | findings
- <reviewer name>: <lenses> -> clean | findings
Skipped Review-Standard lenses: <lens — one-line reason each, or "none">

Accepted findings fixed:
- <finding -> fix>

Rejected findings:
- <finding -> why rejected (intentional / speculative / out of scope)>

Validation after fixes:
- <command> -> <result>

Final status: <all rerun reviewers clean | exact unresolved blocker>
```

For a single-reviewer review (allowed for narrow diffs per the Review Standard), the panel is just one line.
