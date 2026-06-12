---
name: kata-goal-delivery
description: >-
  Use when the user asks an agent to complete a long-running, long-horizon, or multi-step goal using Kata as the durable local issue ledger. Requires the kata CLI and a workspace-bound kata project. Guides decomposition into parent and child kata issues, sequential implementation, independent review of local diffs or commit ranges, evidence-based closes, and final holistic review.
metadata:
  short-description: Deliver long goals through Kata
---

# Kata Goal Delivery

Use Kata as the required durable coordination layer for a long-running goal. This skill requires the `kata` CLI and a Kata project bound to the workspace; if they are unavailable, initialize Kata when the project name is obvious or ask for the missing install/project decision. Do not silently substitute GitHub Issues, markdown plans, chat history, or TODO files as the tracker.

Kata is the source of truth for issue decomposition, ownership, state changes, comments, relationships, and close evidence. It is not a git hosting or PR system. Use the repository's normal branch, commit, or review workflow when available, but record durable progress, review proof, and final status in Kata. Include a PR URL only when the repository already requires one; the Kata issue and comments remain required.

## Principles

- The user's overall objective is the goal; Kata is the durable state that survives handoffs.
- One child issue should be one independently implementable unit of work.
- Issues are context delivery. A fresh agent should be able to implement a child issue without hidden chat history.
- Relationships are scheduling data: use `--parent` for the tracker/child hierarchy and `--blocked-by` or `--blocks` for dependency order.
- Close discipline matters. A Kata close asserts completion; do not close attempted, partial, or unreviewed work.
- Close each verified child promptly. Do not save a batch of sibling closes for the end; Kata can throttle more than three sibling closes by one actor under one parent within 60 seconds.
- Keep the tracker parent authoritative: goal, shared context, issue graph, validation strategy, current-state comments, and final status.
- Keep changes small enough for deep review. For code work, sanity-check size by reviewer burden: roughly 500+ meaningful changed lines or changes spread across many files/ownership boundaries are signals to split or widen review.
- Do not add backward compatibility unless explicitly required by the user or tracker. Avoid shims, legacy framing, and constraints for hypothetical old integrations.
- Be willing to pursue a large goal when the plan is sound. Confidence must come from repo context, validation, Kata evidence, and review.

## Kata Operating Contract

Start every session from the workspace:

```sh
kata quickstart
kata list --agent
kata ready --unowned --agent
kata ready --unowned --label goal-<goal-slug> --agent
kata whoami --agent
```

Default to `--agent` for ordinary reads and mutations in agent logs. Use `--json` only when scripting needs complete structured data.

Before creating any issue, search:

```sh
kata search "Kata goal delivery: <goal>" --agent
```

Create with stable idempotency keys so retries do not duplicate work:

```sh
kata create "Kata goal delivery: <goal>" \
  --body-file <tracker-body-file> \
  --label goal-delivery \
  --label "goal-<goal-slug>" \
  --idempotency-key "kata-goal-delivery-<goal-slug>-tracker" \
  --agent
```

Use `kata claim <ref> --agent` before working a child issue in multi-agent contexts. If the claim fails because another actor owns the issue, treat that as coordination data and select another ready issue; do not force-claim unless the user or current owner explicitly authorizes it.

Never run `kata delete` or `kata purge` unless the user explicitly asks for that exact destructive operation and issue ref.

## Templates

Load `references/templates.md` when creating the tracker, child issues, current-state comments, review records, or final status.

For multiline issue bodies and comments, write the markdown to a temporary file and pass `--body-file` or `--body-stdin`; then reread with `kata show <ref> --agent` to confirm the body or comment survived. `kata edit` does not provide `--body-file` in current Kata, so prefer comments for running state updates and only replace bodies when necessary and verified.

## Concurrency Model

- **Child issues under one tracker run sequentially by default.** Design each implementation child to build on the verified result of previous children. Use `--blocked-by` links when order matters.
- **Parallel agents within a single child are allowed only when their work is separable.** One integration owner must combine the output into one coherent branch, worktree, or artifact and confirm there are no conflicting decisions.
- **Parallel reviewers are encouraged.** Independent review may use several reviewer agents at once, split across the Review Standard focus areas. Aggregate their findings before responding.
- **Small process or tracker-fix issues may interrupt the sequence** only when they unblock the goal or prevent stale instructions from misleading later work. Link them to the tracker and review/close them like any other child.

## Review Standard

Independent review must cover at least: code robustness, correctness, maintainability, complexity, test coverage, security, user/agent experience, and documentation when applicable.

A multi-reviewer panel is the default. A single general reviewer is acceptable only for simple, narrow changes that one reviewer can fully digest across the applicable lenses. Use the `panel-review` skill when available; otherwise use fresh reviewer agents that did not share the implementation context. Do not self-approve.

Every implementation child must receive a **Review Record** as a Kata comment before it closes. If the repository also uses PRs, include the PR URL in the record and in close evidence, but the Kata comment is still required. After any post-review code change, amend, rebase, force-push, or material artifact change, the prior review and validation evidence is stale; rerun affected reviewers and validation or record exact diff-equivalence before closing.

## Start

1. Verify workspace, Kata availability, actor identity, project binding, repo conventions, branch/merge conventions, and validation commands. Useful commands: `kata version --agent`, `kata quickstart`, `kata whoami --agent`, `kata projects show <project>`, `git status --short`, and repo-specific test/lint/build discovery.
2. If the workspace is not initialized and the project name is obvious, run `kata init`; otherwise ask for the project name. For agent-heavy repos, consider `kata init --with-agents` only when updating `AGENTS.md` is appropriate for the repo.
3. Create or reuse one parent tracker issue titled `Kata goal delivery: <goal>` using the tracker template. Label the tracker and every child with `goal-delivery` plus a goal-specific label such as `goal-<goal-slug>` so `kata ready --label goal-<goal-slug>` can isolate this program's work.
4. Discover validation commands up front and record them in the tracker. Include test, lint, build, type-check, docs, screenshots, or end-to-end checks that apply.
5. Put in the tracker: goal, source-of-truth order, shared context, definition of done, validation strategy, risks, draft issue graph, integration notes, and how final completion will be proven.
6. Create child implementation issues from the draft plan in dependency order using `--parent <tracker-ref>`. Add `--blocked-by <previous-child-ref>` when a child depends on a previous child.
7. Comment on the tracker with the actual child refs and ordering once creation succeeds. Kata relationships are authoritative for dependencies; the comment is for human handoff.

Each child issue must include the fields in `references/templates.md`: objective, tracker ref, self-contained context, scope, non-goals, dependencies, sequencing, implementation notes, acceptance criteria, required validation, and review expectations.

## Issue Cycle

Work one child at a time. Select the next ready child whose blockers are closed.

1. Reread the tracker, the child body, child comments, relevant dependency issues, and recent Kata events before changing code. If assumptions changed, add a tracker or child comment first.
2. Claim the child with `kata claim <ref> --agent`.
3. Implement only the child scope. Update tests, docs, README, comments, config, migrations, examples, or screenshots when the change requires it.
4. Keep shared facts in the tracker when they affect later children. Use comments for running state, blockers, and decisions.
5. Run the validation commands recorded at Start plus child-specific validation. Record exact commands and results.
6. Freeze the review target: base ref/SHA, head ref/SHA, changed files, diff stat, and exact diff command. If the repo requires PRs, open or update the PR; otherwise review the local branch, commit range, or patch directly.
7. Request independent review against the frozen target. Address every accepted finding with commits or artifact updates. If rejecting a finding, record why in the child comment and ask the reviewer to confirm when appropriate.
8. Repeat review until there are no unresolved accepted findings and required checks pass.
9. Post the Review Record from `references/templates.md` as a Kata comment on the child.
10. Close the child as soon as it is verified:

```sh
kata close <child-ref> --done \
  --message "<what changed + what verification proves>" \
  --commit <sha> \
  --evidence "test:<command>" \
  --reviewed <path> \
  --agent
```

Use `--pr <url>` when a PR exists. Repeat `--evidence "test:<command>"` for multiple validation commands and repeat `--reviewed <path>` for multiple reviewed paths. If no repository commit exists because the deliverable is non-code, close with appropriate `test:` and `reviewed-paths:` evidence or use `--audit-no-change` for verified no-change work.

## When Blocked

If progress stalls, preserve the state in Kata and fix forward:

- **Kata unavailable:** run `kata health` or `kata daemon status` when useful. If the binary is missing, the remote daemon is unreachable, or the workspace cannot be bound safely, ask for the missing access/decision rather than switching trackers.
- **Validation keeps failing:** comment with the failing command and relevant output, fix forward, and only escalate if the plan is wrong rather than the code.
- **Review cannot run:** run `kata label add <child-ref> needs-review --agent`, comment with what is ready and what review is missing, and do not close it.
- **Claim fails:** choose another ready unowned issue or inspect the owner with `kata show`; do not use `--force` as a shortcut.
- **Issue is mis-scoped or too large:** split it into smaller child issues, connect dependencies with `--blocked-by`/`--blocks`, and comment on the tracker with the revised graph.
- **External decision required:** take a safe, reversible default when one exists and record it as an assumption. Ask the user only when the decision is irreversible or cannot be defaulted safely.
- **Close blocked by open children or throttling:** close verified children individually as they finish. If the throttle is already hit, wait and continue with non-close work rather than rewriting history.

## Final Pass

After all planned children have closed:

1. Reread the tracker, children, comments, close evidence, recent events, and final diff/artifacts as one solution.
2. Run a holistic review against the Review Standard plus integration cohesion, duplicated abstractions, documentation, comments, README updates, operational notes, and removal of compatibility work added without an explicit requirement.
3. Run broad validation using the recorded commands plus any end-to-end checks appropriate to the repository.
4. If gaps remain, create follow-up child issues under the tracker and complete them before closing the tracker, unless they are explicitly non-blocking known follow-ups.
5. Comment on the tracker with the final summary, validation evidence, review record, and known risks.
6. Close the tracker only after every child is closed and the final pass proves the overall goal:

```sh
kata close <tracker-ref> --done \
  --message "<overall goal completed + final verification summary>" \
  --commit <sha> \
  --evidence "test:<broad validation command>" \
  --reviewed <path> \
  --agent
```

Then report the goal complete.
