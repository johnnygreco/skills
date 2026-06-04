---
name: github-goal-delivery
description: >-
  Use when the user asks an agent to complete a long-running, long-horizon, or multi-PR goal using GitHub issues as the durable tracker and pull requests as the reviewer interface. Requires GitHub issue and PR access. Guides decomposition into self-contained issues, sequential implementation PRs, independent review, and final holistic review.
metadata:
  short-description: Deliver long goals through GitHub
---

# GitHub Goal Delivery

Use GitHub as the required durable coordination layer for a long-running goal. This skill requires a GitHub remote plus issue and PR access; if those are unavailable, record the blocker and ask for access rather than adapting to another tracker. Prefer the `gh` CLI for issue and PR operations; use another available GitHub interface only when `gh` is unavailable.

## Principles

- The harness goal is the overall objective; GitHub is the durable state that survives handoffs.
- One issue should be one independently implementable unit of work.
- Issues are context delivery. A fresh agent should be able to implement an issue without hidden chat history; links supplement context but do not replace it.
- PRs are the reviewer interface. An issue is not done until its PR has passed independent review and merged.
- Keep PRs small enough to review deeply. Split or re-scope work that becomes diffuse. Before opening a PR, sanity-check its size: if the diff is large (a useful rule of thumb is roughly 500+ changed lines or many touched files), reconsider splitting the issue first. When a PR is unavoidably large, say so explicitly in the reviewer notes and widen the review panel rather than letting a big diff get a thin review.
- Keep the progress tracker issue authoritative: current plan, shared context, issue checklist, and final status.
- Do not worry about backward compatibility unless explicitly told to. Do not add compatibility shims, preserve legacy behavior, or constrain the design for hypothetical old callers unless the user or tracker requires it.
- Be willing to pursue a large goal when the plan is sound. Prefer the cohesive, modern solution over timid incremental patches; confidence must come from repo context, validation, and review.

## Templates

Load `references/templates.md` when creating or updating the progress tracker, implementation issues, or PR descriptions.

## Concurrency Model

- **Implementation issues in the tracker run sequentially.** Within the GitHub goal delivery program, design each implementation issue to build on the merged result of the previous one, then work one issue at a time in dependency order. Do not open parallel branches for separate implementation issues. This avoids conflicts between independent efforts inside the program; it does not assume the rest of the repository is frozen.
- **Parallel agents within a single issue are allowed only when their work is separable.** Fan out research or implementation agents on the same issue when they can work without overlapping edits or competing decisions. One integration owner must combine their output into one branch, resolve contradictions, and confirm the PR is self-consistent and conflict-free. Keep the issue serial when agents would touch the same code or make competing design choices.
- **Parallel reviewers are encouraged.** Independent review may use several reviewer agents at once, split across the Review Standard focus areas. Aggregate their findings before responding.

## Review Standard

Independent PR review must cover at least: code robustness, correctness, maintainability, complexity (strictly guard against over-engineering), test coverage, security, user/agent experience, and documentation when applicable.

A multi-reviewer panel is the default. A single general reviewer is acceptable at the lead agent's discretion, but only for simple, narrow changes that one reviewer can fully digest and give meaningful feedback on across the applicable lenses. The larger or riskier the diff, the more the panel should be split across lenses; do not reduce a large or security-sensitive change to a single reviewer.

Every PR must carry a **Review Record** (see `references/templates.md`) before it merges: the frozen base..head SHAs reviewed, the reviewers and their lenses, accepted findings fixed, rejected findings with reasons, and the final clean status. A PR merged without a Review Record is a process violation — the record is what proves review actually happened and what a later reader uses to reproduce exactly what was reviewed.

## Start

1. Verify repository, GitHub remote, issue access, PR access, and branch/merge conventions. If any are unavailable, record the blocker and ask for the missing access or decision.
2. Create or reuse one progress tracker issue titled `GitHub goal delivery: <goal>` with the tracker template.
3. Discover the project's validation commands up front (test, lint, build, type-check) and record them in the tracker so every issue validates against the same baseline.
4. Put in the tracker: goal, shared context, definition of done, risks, validation strategy, draft issue plan, and integration notes.
5. Create implementation issues from the draft plan, in dependency order.
6. Update the tracker checklist with GitHub task links, such as `- [ ] #123 Short issue title`, ordered so each issue depends only on issues above it.

Each implementation issue must include the fields in the issue template (`references/templates.md`):

- Objective and expected outcome.
- Link to the progress tracker and enough summarized context to implement in isolation.
- Scope, explicit non-goals, dependencies, and sequencing notes.
- Relevant files, APIs, commands, data contracts, or design constraints.
- Acceptance criteria and required validation.
- PR expectations, including screenshots or logs when useful.

## Issue Cycle

Work issues one at a time. Select the next unchecked issue whose dependencies have all merged.

1. Comment that work is starting, then create a focused branch using repo conventions.
2. Implement only the issue scope. Update tests, docs, README, comments, config, migrations, or examples when the change requires it. Optionally fan out parallel agents on this single issue per the Concurrency Model; one agent must integrate their output into the one branch and confirm it is self-consistent and conflict-free.
3. Keep shared facts in the progress tracker when they affect later issues.
4. Run the validation commands recorded at Start plus any issue-specific required validation, then note exact commands and results.
5. Update the branch against the latest base, then open a PR linked to the issue using the PR template (`references/templates.md`): issue link, summary, validation, risks, and reviewer notes.
6. Request comprehensive review from independent review agents that do not share this implementation's context. Use the review skill when available; otherwise spawn one or more fresh reviewer agents (see the parallel-reviewer pattern in the Concurrency Model). Do not self-approve.
7. Address every finding with commits. If rejecting a finding, explain why in the PR and ask the reviewer to confirm.
8. Repeat review until there are no unresolved findings and required checks pass, then post the Review Record on the PR (`references/templates.md`).
9. Confirm the PR carries a Review Record and required checks are green, then merge according to repo policy, mark the implementation issue complete, and check it off in the progress tracker. Do not merge a PR that has no Review Record.

## When Blocked

If progress stalls mid-cycle, do not silently abandon the work:

- **Validation keeps failing:** capture the exact failing command and output in the tracker, fix forward, and only escalate to the user if the failure indicates a flawed plan rather than a code bug.
- **PR cannot merge** (conflicts, red required checks): rebase or resolve against the latest base; if checks are red for reasons outside the issue scope, record it and decide whether to fix here or file a separate issue.
- **Issue turns out mis-scoped or too large:** stop, split it into smaller issues in the tracker, re-derive dependency order, and resume.
- **Independent review cannot run** (no subagent permission in this session, review skill unavailable, no reviewer access): do not merge the PR unreviewed and do not fall back to self-approval. Record the blocker in the tracker, leave the PR open, and ask the user to grant review/delegation access or decide how to proceed. An unreviewed merge is never the workaround.
- **Missing access or an external decision is required:** record the blocker in the tracker and ask the user; do not work around it by guessing.

## Final Pass

After all planned PRs have merged:

1. Re-read the progress tracker, issues, PRs, and final diff as one solution.
2. Perform a deep holistic review against the Review Standard, plus integration cohesion, duplicated abstractions, documentation, comments, README updates, operational notes, and removal of any compatibility work added without an explicit requirement. Parallel reviewers focused on different concerns are encouraged here.
3. Run broad validation using the recorded commands, plus any end-to-end checks appropriate to the repository.
4. If gaps remain, create follow-up issues and run the same issue-to-PR-to-review cycle.
5. When the solution is cohesive and validated, update the progress tracker with the final summary, validation evidence, and remaining known risks, then complete the harness goal.
