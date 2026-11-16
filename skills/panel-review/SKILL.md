---
name: panel-review
description: Panel review or deep review.
---

# Panel Review

Design a panel around the target's actual risks, spawn independent review agents,
monitor and steer their work, and verify their findings before reporting them.

We want material problems, not nitpicks. Do not report taste, style, or minor
polish. Keep scope on the stated problem, and hold both the target and the
panel's own recommendations to sound engineering in both directions. An added
abstraction, option, or handler for a hypothetical case is a cost that needs a
concrete justification. A patch that silences a symptom and leaves its cause or
a design problem in place is a cost too. Judge a change by whether it solves the
problem where the problem originates, not by the size of its diff.

## Choose the Mode

Produce a report in the conversation by default. Review does not authorize edits
to the reviewed artifacts, commits, pushes, or posting to a PR or tracker.

A request to fix findings authorizes those fixes, not a repeated review cycle.
Follow [Fix Findings When Asked](#fix-findings-when-asked) after the report.

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
scope, and evidence standard. Allow intentional overlap for consequential risks.
Record material gaps.

Always include at least one holistic reviewer, using the Generalist lens, who
judges the change in the context of the full codebase rather than the diff
alone: whether it fits existing architecture and conventions, duplicates or
bypasses existing code, or breaks callers and assumptions elsewhere. For a
non-code target, the equivalent is the whole artifact and the system it serves.

Apply repository standards across the selected lenses and keep documented-rule
violations distinguishable from gaps in the requested behavior. Cover meaningful
risks with the smallest useful panel. The holistic Generalist alone may cover a
narrow target; add focused reviewers for substantial or varied risks.
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
  Seek the simplest remedy that resolves the cause, and question a recommendation
  that only guards the symptom as readily as one that overbuilds.
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
- Keep defects, documented-rule violations, and design problems distinct, and
  accept each on its own evidence. A design problem is substantiated when the
  code shows who pays for it: a likely change that must touch several places, a
  caller that must know another module's internals, state with more than one
  writer. Weigh it against project constraints. A change that is under-designed
  for its problem is as reportable as one that is overbuilt. Exclude nits,
  taste-only comments, speculative rewrites, scope expansion, and issues below
  the agreed reporting bar.
- Assess whether a suggested remedy reaches the cause and what it adds; a valid
  finding may come with an overbuilt fix or with one that only masks the
  symptom. The size of the right remedy does not lower a finding's standing.
  Record consequential unresolved questions as limitations.

## Report

Lead with verified findings ordered by impact. For each, give the location, the
trigger or the design cost, the evidence, the cause, the consequence, and a
recommendation that addresses the cause. Retain lens labels and requirement or
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

## Fix Findings When Asked

Fix the accepted findings, validate, and verify the delta in proportion to its
size: your own check for a small delta, or one independent reviewer for a
substantial one. Ask that reviewer whether each finding is resolved at its
cause and whether the delta introduced a regression. A fix that handles only
the reported trigger is partial.

Fix each finding at its cause. Correct the code or design that made the issue
possible, and let the cause set the size of the change. Aiming for the smallest
diff produces guards and special cases that hide the trigger and leave the
problem in place.

- Ask whether the state that triggered a defect can legitimately occur. If it
  can, handling that state is the fix. If it should never exist, a guard, retry,
  swallowed error, clamped value, or discarded state only hides the defect; fix
  what produces the state.
- When a fix does not resolve its finding, write down the assumption the attempt
  relied on and test it directly before trying another fix on the same
  assumption.
- When the cause lies outside what the user authorized, report it and the
  decision needed instead of patching around it.
