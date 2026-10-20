---
name: show-me-your-work
description: >-
  Keep an evidence-backed decision log for long-running, unattended, or multi-phase
  work that a human will review later. Use when asked to show your work, maintain
  an audit trail, record decisions and verification, or audit an existing trail.
  Not for ordinary progress updates or a one-off explanation of an answer.
disable-model-invocation: true
---

# Show Me Your Work

Maintain one append-only TSV log of consequential decisions, their rationale,
evidence, and observed outcomes. Keep explanations brief and suitable for a
teammate reviewing the work later.

## Establish the Trail

Reuse the task's existing log and output conventions. Otherwise use
`decisions.tsv` in the working directory, or `.audit/<task-slug>.tsv` when several
efforts share a workspace. Treat it as a local working artifact; do not stage,
commit, publish, or change ignore rules unless the task authorizes that action.
Check explicit staging paths so incidental logs do not enter a commit.

Read [log-format.md](references/log-format.md) before creating or extending a log.
It defines the columns, helper usage, run boundaries, and correction references.
Read an existing log before appending; preserve its history. Give each run a
stable identifier and record a `start` row at the beginning of each writer's
stretch. The lead owns writes to a shared log; helpers return evidence to it.

Logging does not expand the underlying task. An audit-only request authorizes
inspection and corrections to the trail, not implementation changes or rerunning
operations with external effects.

## Record Decisions and Checkpoints

Log meaningful choices, completed units with verification, changed approaches,
reverts, blockers, and iteration outcomes as they occur. Skip routine commands
that do not affect the result. Record a consequential failed or abandoned approach
when it explains the final choice.

Use [scripts/log.py](scripts/log.py) to append a timestamped row. Link evidence
that supports the specific claim: a versioned source location, captured command
output, test report, diff, or other inspectable artifact. For execution results,
retain the exact executable command, relevant version or inputs, exit status, and
output together. Save inline verification code or a runnable script when the
command depends on it, including for preservation and audit checks.
A command string alone proves neither execution nor success.

Distinguish what was observed from what is proposed or inferred. Use `open`,
`blocked`, `not run`, or `inconclusive` when appropriate; do not turn an intended
check into a passing result. Explicitly mark unavailable evidence and the
remaining uncertainty. Keep secrets and unnecessary private content out of both
the log and its evidence artifacts.

Correct mistakes with a new row that identifies and supersedes the old row.
Never rewrite history to match the final outcome. For a retrospective entry,
record the current timestamp and say it was reconstructed from available evidence.

## Audit Before Handoff

Walk this run's stretches against the available conversation, tool results, and
referenced artifacts. Check that actions actually occurred, outcomes match the
evidence, and consequential pivots or failures are represented. Append missing
entries and corrections; do not silently adopt earlier runs' claims as verified.
Resolve each relative file pointer from the log's directory and check that the
cited file and line exist. For a log in `.audit/`, a workspace-root file needs a
pointer such as `../application.py`, including in newly appended corrections.

Use a transcript only when its location or access tool is explicitly available
for the current conversation. Do not search unrelated chat stores or assume a
particular product's transcript directory. If full history is unavailable, audit
what is accessible and identify the coverage gap.

Have an independent subagent review the trail when agent execution is available
and permitted. Prefer a different model family when the environment supports it;
otherwise an independent agent on the available model is useful. Give it the log,
this run's row ranges, and the accessible transcript or evidence. Ask for weak
evidence, overstated verification, risky choices, and omitted turning points,
with row references. Keep this a review of the trail, without redoing the task or
starting a review panel. Verify flags and append corrections where warranted.

If independent review cannot run, finish the useful audit and disclose that only
self-review was performed. Never invent a reviewer identity or claim that missing
history was checked.

## Return the Trail

Link the log and any evidence needed to review it. End the handoff with a brief
**Attention** section naming the actual review coverage, unresolved flags with
row references, and verification gaps. Say "No flags" only for the scope actually
checked. Identify the reviewer's model only when known.

Other skills can use this trail without duplicating its schema or replacing their
own deliverables. A request to inspect an existing trail should return findings
and any authorized corrections, without inventing a new implementation task.
