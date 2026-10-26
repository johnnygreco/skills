---
name: panel-review
description: Panel review or deep review.
---

# Panel Review

Design a panel around the target's actual risks, spawn independent review agents,
monitor and steer their work, and verify their findings before reporting them.

## Choose the Mode

Produce a report in the conversation by default. Review does not authorize edits
to the reviewed artifacts, commits, pushes, or posting to a PR or tracker.

A request to fix findings authorizes those fixes, not a repeated review cycle:
fix the accepted findings, validate, and verify the delta in proportion to its
size, with your own check for a small delta or one independent reviewer for a
substantial one.

## Establish the Target

1. Honor the user's target and comparison point. For a Git change without an
   explicit base, infer it from the PR or default branch and state the assumption.
   Verify refs resolve and check for an empty diff before dispatching; do not
   substitute another target. For a document, design, or other artifact, establish
   whether to assess the whole artifact or a change from a prior version.
2. Freeze the reviewed version. Record base, merge-base, head, and diff commands
   for Git changes; otherwise use versioned copies or content hashes. Explicitly
   include or exclude staged, unstaged, and untracked work; preserve included patches and
   new files. Give all reviewers the same snapshot and matching surrounding files.
   Use temporary copies as needed without committing, stashing, or discarding user
   work. Refresh affected reviews if the target changes.
3. Gather the user's requirements, relevant spec or issue, repository instructions,
   standards, ADRs, and validation commands. State missing context without
   inventing requirements; ask only when it prevents a useful review.
4. Share a target packet: snapshot and diff access, changed files, relevant context
   paths or contents, checks already run, scope, non-goals, and severity bar.
   Include the intended users, scale, and known constraints. Unknown conditions
   are uncertainties to investigate or disclose, not invented requirements.

## Choose Lenses and Spawn Reviewers

Read the [lens index](references/review-lenses.md) and only the selected lens
files. Identify the target's material risks and give each an owner. Lenses focus
attention; they do not prohibit noticing problems across boundaries. Combine,
specialize, or invent lenses to fit the target. Give a custom lens a clear question,
scope, and evidence standard. Use a Generalist for broad coverage when useful,
and allow intentional overlap for consequential risks. Record material gaps.

Apply repository standards across the selected lenses and keep documented-rule
violations distinguishable from gaps in the requested behavior. Cover meaningful
risks with the smallest useful panel. One independent Generalist may cover a
narrow target; several focused reviewers may suit substantial or varied risks.
Size by complexity, uncertainty, and consequence, not line or module count alone.

Choose each reviewer's model and reasoning effort as deliberately as its lens,
from the latest version of each family at medium to xhigh effort:

- **Opus:** a strong, creative coder.
- **GPT Sol:** a strong coder, analytical and thorough.
- **Fable:** a deep, creative thinker.

Match these strengths to the risks you assigned, and spend more effort where a
risk is subtle or consequential. Different models bring different perspectives,
which is most valuable where reviewers overlap on a consequential risk. If a
family is unavailable, use the others and record the gap.

Spawn **independent review agents** with T3 Code's `delegate_task`,
concurrently where practical. Do not silently substitute the lead's own review
for an available, permitted independent review. If independent execution is
unavailable, fails, or conflicts with the user's constraints, perform the useful
review that remains and disclose the cause and loss of independence.

Read the [reviewer brief](references/reviewer-brief.md) when preparing assignments.
Give each reviewer the target packet, relevant rules and lens questions, scope,
and expected response. Inline short instructions or provide specific accessible
references; do not make reviewers reload the lead's workflow or every lens. Use
fresh context where supported, omitting implementation chat history, suspected
findings, and other reviewers' conclusions. Reviewers inspect without editing.

## Monitor and Steer the Panel

The lead owns reviewer progress through synthesis. Set effort expectations that
fit the target and any runtime limits, leaving time to verify and report. Use the
environment's completion notifications, waits, or bounded status checks; avoid
busy polling and unattended background work. Meanwhile, inspect the target for
later verification. Intervene when progress, scope, or evidence warrants it:

- Redirect scope creep and over-engineering early. Ask which supported user or
  caller can encounter the problem, whether an existing constraint prevents it, and
  what requirement or concrete maintenance cost justifies the proposed change.
  Seek the simplest adequate remedy.
- Supply missing context or narrow a stalled investigation. Stop redundant work
  while preserving meaningful coverage. Follow downstream evidence as needed
  without expanding the authorized repair scope. Route material cross-lens
  discoveries to an owner. For a long-running check, ask what it has established,
  what uncertainty remains, and whether continuing could change the report.
- Preserve independent initial judgments. For subsequent verification, share the
  disputed evidence when useful without directing a verdict. Do not suppress a
  substantiated issue to obtain a clean result.

Account for every assigned review before the final report. Check that each result
names the assigned snapshot and reports evidence and methods for any claimed
validation. Send stale, mismatched, or unsupported results back for correction;
replace the reviewer when useful, or record incomplete coverage. If a reviewer
cannot finish within the available constraints, collect partial findings and
report the gap. Stop owned checks and release workers as needed before finishing.

## Verify and Synthesize

- Verify findings against the actual path, adjacent code, and requirements.
  Reviewer agreement and a passing test suite do not establish correctness.
- For a consequential claim, identify the assumption it depends on and seek
  evidence proportionate to the risk. Separate source inspection, execution-path
  reasoning, and observed test or reproduction results; label unverified claims.
- Deduplicate by root cause while retaining lens labels and evidence. Resolve
  disagreements from source material rather than votes.
- Classify findings as **accepted** (substantiated and in scope), **rejected**
  (unsupported, unreachable, intentional, or taste-only), or **follow-up** (real
  but outside scope or pre-existing). A finding outside one reviewer's assignment
  can still be in the panel's scope. Include material, relevant follow-ups that
  respect the user's reporting scope; do not turn review into an unrelated audit.
  Acceptance includes a finding in the report; it does not authorize edits.
- Keep defects and documented-rule violations distinct from design judgments.
  Assess design proportionality when structure or maintenance is a relevant risk,
  using concrete costs and project constraints. Assess a suggested remedy's
  complexity as well as its benefit; a valid finding may have an overbuilt proposed
  fix. Exclude taste-only nits, speculative rewrites, and issues below the agreed
  reporting bar. Record consequential unresolved questions as limitations.

## Report

Lead with verified findings ordered by impact: location, trigger, evidence,
consequence, and a focused recommendation. Retain lens labels and requirement or
standards citations. If none survive verification, say no actionable findings
were found within the reviewed scope.

Include a compact review record:

- Target version, comparison point, reproducible commands or snapshot, and included
  uncommitted work.
- Reviewers with their lenses, models, and reasoning effort; material skipped or
  incomplete coverage; and any fallback with its actual cause.
- Accepted findings, reasons for consequential rejections, and relevant follow-ups
  with their location and trigger.
- Validation commands and observed results, with checks not run clearly identified.
- Review status: **findings**, **clean within reviewed scope**, or **incomplete**.
  Missing material coverage or evidence prevents a clean verdict. Report validation
  status separately; review alone does not certify merge readiness.

Return the report to any coordinating workflow, which owns storage, publishing,
and completion decisions. Finish after accounting for the panel and delivering
the report; do not keep waiting for already-completed work.
