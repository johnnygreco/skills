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

- The user's overall objective is the goal; GitHub is the durable state that survives handoffs.
- One issue should be one independently implementable unit of work.
- Issues are context delivery. A fresh agent should be able to implement an issue without hidden chat history; links supplement context but do not replace it.
- PRs are the reviewer interface. An issue is not done until its PR has passed independent review and merged.
- Keep PRs small enough to review deeply. Split or re-scope work that becomes diffuse. Before opening a PR, sanity-check size along two axes: volume, such as roughly 500+ changed lines a reviewer must reason about (count production code and tests; discount generated code, lockfiles, snapshots, golden files, and bulk fixtures), and spread, such as changes across many files or ownership boundaries. Either axis is a signal to reconsider splitting the issue. When a PR is unavoidably large or cross-cutting, say so explicitly in the reviewer notes and widen the review panel rather than letting a big diff get a thin review.
- Keep the progress tracker issue authoritative: current plan, shared context, issue checklist, and final status.
- Do not add backward compatibility unless explicitly required by the user or tracker. Avoid shims, legacy framing, and constraints for hypothetical old integrations; correct stray wording when it does not change behavior.
- Be willing to pursue a large goal when the plan is sound. Prefer the cohesive, modern solution over timid incremental patches; confidence must come from repo context, validation, and review.

## Templates

Load `references/templates.md` when creating or updating the progress tracker, implementation issues, or PR descriptions.

## Concurrency Model

- **Implementation issues in the tracker run sequentially.** Within the GitHub goal delivery program, design each implementation issue to build on the merged result of the previous one, then work one issue at a time in dependency order. Do not open parallel branches for separate implementation issues. This avoids conflicts between independent efforts inside the program; it does not assume the rest of the repository is frozen.
- **Parallel agents within a single issue are allowed only when their work is separable.** Fan out research or implementation agents on the same issue when they can work without overlapping edits or competing decisions. One integration owner must combine their output into one branch, resolve contradictions, and confirm the PR is self-consistent and conflict-free. Keep the issue serial when agents would touch the same code or make competing design choices.
- **Parallel reviewers are encouraged.** Independent review may use several reviewer agents at once, split across the Review Standard focus areas. Aggregate their findings before responding. Across a long multi-PR run, close out completed reviewer agents once their findings are captured so a limited subagent pool is not exhausted. Treat resource, limit, or quota spawn failures as operational: close completed or stale reviewers and retry before treating the review as blocked. Do not ask the user to authorize reviewers unless the harness reports a policy or permission failure.
- **Small process or guidance PRs may interrupt the sequence** only when they unblock the goal or prevent stale instructions from misleading later work (for example, correcting tracker or issue wording). Link them from the tracker, review and merge them like any other PR, then rebase and revalidate any open implementation PR before merging it.

## Review Standard

Independent PR review must cover at least: code robustness, correctness, maintainability, complexity (strictly guard against over-engineering), test coverage, security, user/agent experience, and documentation when applicable.

A multi-reviewer panel is the default. A single general reviewer is acceptable at the lead agent's discretion, but only for simple, narrow changes that one reviewer can fully digest and give meaningful feedback on across the applicable lenses. The larger or riskier the diff, the more the panel should be split across lenses; do not reduce a large or security-sensitive change to a single reviewer.

Every PR must carry a **Review Record** before it merges; merging without one is a process violation. The record is what proves review happened and lets a later reader reproduce exactly what was reviewed. Load its shape from `references/templates.md` when you write one.

## Start

1. Verify repository, GitHub remote, issue access, PR access, branch/merge conventions, `gh` version, and any optional `gh` features you plan to rely on. If any are unavailable, record the blocker or fallback and ask only for missing access or decisions.
2. Create or reuse one progress tracker issue titled `GitHub goal delivery: <goal>` with the tracker template.
3. Discover the project's validation commands up front (test, lint, build, type-check) and record them in the tracker so every issue validates against the same baseline.
4. Put in the tracker: goal, shared context, definition of done (including whether release, publish, README, and user-facing docs are in scope), risks, validation strategy, draft issue plan, and integration notes.
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

1. Reread the tracker, the issue body, and the merged dependency PRs before branching. Pre-created issues go stale; if source-of-truth, scope, non-goals, validation, or sequencing assumptions changed, update the issue body first. Then comment that work is starting and create a focused branch using repo conventions.
2. Implement only the issue scope. Update tests, docs, README, comments, config, migrations, or examples when the change requires it. Optionally fan out parallel agents on this single issue per the Concurrency Model; one agent must integrate their output into the one branch and confirm it is self-consistent and conflict-free.
3. Keep shared facts in the progress tracker when they affect later issues.
4. Run the validation commands recorded at Start plus any issue-specific required validation, then note exact commands and results.
5. Update the branch against the latest base, then open a PR linked to the issue using the PR template (`references/templates.md`): issue link, summary, validation, risks, and reviewer notes.
6. Request comprehensive review from independent review agents that do not share this implementation's context. Use `panel-review` when available; otherwise spawn one or more fresh reviewer agents (see the parallel-reviewer pattern in the Concurrency Model). Do not self-approve.
7. Address every finding with commits. If rejecting a finding, explain why in the PR and ask the reviewer to confirm.
8. Repeat review until there are no unresolved findings and required checks pass, then post the Review Record on the PR (`references/templates.md`).
9. Confirm the PR carries a Review Record whose head SHA matches the current PR head and required checks are green, then merge according to repo policy, mark the implementation issue complete, and check it off in the progress tracker. Do not merge a PR that has no Review Record. After any post-review head change (review-fix commit, amend, rebase, force-push), the prior review and CI evidence is stale: rerun affected reviewers and validation on the new head, or record diff-equivalence, before merging.

## When Blocked

If progress stalls mid-cycle, do not silently abandon the work:

- **Validation keeps failing:** capture the exact failing command and output in the tracker, fix forward, and only escalate to the user if the failure indicates a flawed plan rather than a code bug.
- **PR cannot merge** (conflicts, red required checks): rebase or resolve against the latest base; if checks are red for reasons outside the issue scope, record it and decide whether to fix here or file a separate issue.
- **Issue turns out mis-scoped or too large:** stop, split it into smaller issues in the tracker, re-derive dependency order, and resume.
- **Independent review cannot run** (no subagent permission in this session, `panel-review` unavailable, no reviewer access): first distinguish policy or permission failures from operational resource failures. For resource, limit, or quota errors, close completed or stale reviewer agents and retry before escalating. If review still cannot run, do not merge the PR unreviewed and do not fall back to self-approval. Record the blocker in the tracker, leave the PR open, and ask the user to grant review/delegation access or decide how to proceed. An unreviewed merge is never the workaround.
- **Missing access or an external decision is required:** first confirm the decision is actually required by the goal or tracker, not implied by examples, fixtures, samples, or legacy artifacts in the repo; illustrative data is not a constraint. If a safe, reversible default exists, take it, label it as an assumption in the tracker, and keep moving. Block on the user only when the decision is irreversible or cannot be defaulted safely. When you ask, make the question answerable in one message: define terms, give the concrete question, list options, and recommend a default. Do not park a draft PR on a self-imposed gate and call it progress.

## Final Pass

After all planned PRs have merged:

1. Re-read the progress tracker, issues, PRs, and final diff as one solution.
2. Perform a deep holistic review against the Review Standard, plus integration cohesion, duplicated abstractions, documentation, comments, README updates, operational notes, and removal of any compatibility work added without an explicit requirement. Parallel reviewers focused on different concerns are encouraged here.
3. Run broad validation using the recorded commands, plus any end-to-end checks appropriate to the repository.
4. If gaps remain, triage by severity: blocker/high gaps gate completion, while related low/medium gaps should be bundled into as few follow-up PRs as possible or recorded as known follow-ups without blocking. Keep cohesive fixes together rather than splitting trivial PRs. If the final pass keeps generating new follow-ups across rounds, pause and confirm remaining scope with the user.
5. When the solution is cohesive and validated, update the progress tracker with the final summary, validation evidence, and remaining known risks, then report the goal complete.
