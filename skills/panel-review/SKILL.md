---
name: panel-review
description: >-
  Run a deep, multi-agent expert panel review of a PR, branch, design, or substantial change. Use when the user asks for panel review, deep review, multi-agent review, specialist reviewers, merge-readiness review, review until clean, or independent checks across robustness, correctness, maintainability, complexity, tests, security, user or agent experience, documentation, and integration risks.
metadata:
  short-description: Expert-panel deep review
---

# Panel Review

Run an independent, specialist review panel for substantive review work. The lead agent designs the reviewer mix for the target, then owns the outcome: verify every finding against the real code, fix accepted issues, rerun validation, and repeat review until no accepted findings remain.

## Contract

- Use subagents. If no subagent tool is available, say that panel-review requires subagents and do not replace it with a single self-review.
- Tailor the panel to the change. Do not mechanically spawn a fixed set of reviewers when fewer, broader, narrower, or different specialists would review the target better.
- Keep reviewer agents independent. Start them with fresh context where possible; do not include implementation chat history, your private conclusions, or expected findings.
- Run the panel concurrently. Spawn reviewers in parallel and blind to each other, then aggregate once they all return.
- Close out reviewer subagents when done. If your harness uses persistent or pool-limited subagents, release each reviewer once you have captured its result, and close superseded reviewers from a prior round before spawning the next. If a spawn fails because the subagent limit is reached, close completed or stale reviewers and retry once before treating it as blocked.
- Review a frozen target per round. Pin the change to a stable reference and give every reviewer in that round the same diff; after fixes, create a new frozen target for the next round.
- Reviewer output is advisory. Verify findings by reading the actual code path, adjacent files, project standards, and external docs when relevant.
- Prefer actionable findings over nits. Reject speculative risks, taste-only feedback, broad rewrites, and edge cases that do not matter for the target.
- Guard strictly against over-engineering. Treat needless abstraction, cleverness, generic machinery, duplicated concepts, or extra moving parts as review-worthy only when they materially hurt the code's future maintainability.
- Fix accepted findings at the right ownership boundary. When one finding reveals a repeated bug class, inspect sibling instances in the target scope.
- Rerun the relevant reviewers after review-triggered code changes. Continue until all accepted findings are fixed or consciously rejected and the final pass reports no accepted findings.
- Do not push only to run this skill. Push or update a PR only when the user asked for that.

## Target Setup

You know git; choose the commands yourself. This section defines *what* the reviewers need, not the exact plumbing to produce it.

1. Identify the review target.
   - Use any base ref, commit, tag, or PR the user names.
   - Otherwise, if an open PR exists, use its base ref; failing that, use the repository's default remote branch.
   - If the working tree has uncommitted changes, decide explicitly whether they belong to the target. If they do, include them — do not let a commit-only diff silently drop them.
2. Freeze the target for this review round before spawning reviewers. Use a stable head SHA plus an explicit patch/ref for any included uncommitted work, or make an explicit local commit/stash decision when that is appropriate for the repo. Record the exact command or commands that reproduce the diff. After fixes, create a fresh frozen target for the next round.
3. Assemble a target packet every reviewer receives:
   - the change itself: branch, working-tree status, base/merge-base/head, commit list, changed files, diff stat, and the exact diff command to run
   - project context that should shape review: AGENTS.md, CONTRIBUTING, README, relevant docs, ADRs, specs, the issue/PR/spec description, CI config, and package/test manifests
   - validation already run, and the commands to run after fixes
   - the accepted scope and known non-goals, so reviewers do not flag intentionally deferred behavior unless the current target creates a concrete blocker for it

## Review Panel

Load `references/review-lenses.md` before spawning reviewers.

First design the panel:

1. Inspect the target packet and changed files.
2. Identify the risk surfaces: behavior, robustness, maintainability, complexity, tests, security, user experience, agent experience, documentation, APIs, data, operations, performance, or other domain concerns.
3. Choose the smallest set of independent reviewers that covers the meaningful risks. Combine lenses for small diffs; split lenses when a risk is deep enough to deserve focused attention.
4. Explicitly skip inapplicable lenses instead of spawning low-value reviewers. For example, documentation may be skipped when no user-visible behavior, API, workflow, or operational contract changed. Record which applicable lenses you skipped and why — an unexplained gap in coverage is itself a review weakness.
5. Avoid redundant reviewer stacking. Three near-identical reviewers all on the data contract while correctness, tests, and security go unreviewed is wasted coverage. If you do put more than one reviewer on the same lens — useful for a deep, high-risk surface — give each a distinct subscope or state why the redundancy is intentional, and still cover the other applicable lenses.

A multi-reviewer panel is the default. A single general reviewer is acceptable at the lead agent's discretion, but only for simple, narrow changes that one reviewer can fully digest and give meaningful feedback on across the applicable lenses. The larger or riskier the diff, the more the panel must split across lenses; never reduce a large, architectural, or security-sensitive change to a single reviewer.

Typical panels are three to six reviewers, but the correct number depends on the diff. Examples:

- Small internal refactor: correctness/robustness, maintainability/complexity, tests.
- Auth or permissions change: security/privacy, correctness/robustness, tests/integration.
- Frontend workflow change: user experience/accessibility, correctness, maintainability/tests, docs if user-facing behavior changed.
- Agent-tooling change: agent experience, correctness/robustness, maintainability/complexity, tests/docs.

Each reviewer prompt must include:

- the target packet
- relevant context file paths
- the selected lenses and any relevant guidance from `references/review-lenses.md`
- the reviewer's scope, exclusions, and severity bar
- instructions to inspect code and run read-only commands as needed
- instructions not to edit files
- the required output format from `references/review-lenses.md`

## Aggregation

1. Wait for all reviewers. Treat each reviewer return as one incremental result, not panel completion — a non-timeout wait can mean a single reviewer finished. Do not aggregate, declare clean, or decide to merge until every expected reviewer has completed, timed out, or been deliberately superseded.
2. Deduplicate findings by root cause, not by file.
3. Verify each finding locally. Accept it only when it is concrete, actionable, and supported by the code or project requirements.
4. Classify each finding as:
   - `accepted`: fix now
   - `rejected`: explain why it is intentional, speculative, out of scope, or not a real risk
   - `follow-up`: real but outside the requested review scope
5. Fix accepted findings, then run focused validation and any broad validation required by the repository.

## Iteration

After any fix caused by the review:

1. Create a fresh frozen target packet so reviewers see the updated diff.
2. Rerun every reviewer whose finding led to a fix.
3. Also rerun any lens whose risk surface changed because of the fix.
4. Redesign and rerun the panel when the fix is broad, architectural, security-sensitive, or changes public behavior.

Stop only when:

- no accepted findings remain,
- validation has passed or an external failure is clearly documented,
- rejected findings have concise reasons,
- follow-ups are explicitly out of scope and recorded.

## When Review Does Not Converge

Panel review can loop or creep. Do not iterate blindly:

- If a fix would exceed this target's scope or change architecture, public behavior, or security posture, stop and surface it to the user rather than growing the diff inside the review.
- If new accepted findings keep appearing across rounds with no sign of settling, pause, summarize what is and is not resolved, and ask the user how to proceed.
- If two reviewers give conflicting guidance, the lead decides, records the rationale, and does not relitigate it in later rounds.
- Do not run an extra round just to produce a cleaner report. Once a pass returns no accepted findings, that pass is the result.

## Final Report

Report:

- review target and base, as the frozen `base-ref base-sha..head-ref head-sha` plus the exact diff command, so a reader can reproduce exactly what was reviewed
- reviewer panel design and why those lenses were chosen; always list applicable lenses that were skipped and the one-line reason for each
- reviewers run, including reruns
- accepted findings fixed
- rejected findings with short rationale
- validation commands and results
- clean review status or the exact unresolved blocker

When this review backs a github-goal-delivery PR, post the result in the Review Record shape from that skill's `references/templates.md` so review evidence is consistent across PRs.
