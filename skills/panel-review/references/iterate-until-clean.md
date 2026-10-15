# Iterate Until Clean

This workflow applies only after the user explicitly requests repeated fixing and
review. Preserve the original scope and any existing authorization; the request
does not authorize unrelated redesign, publishing, or merging.

The loop exists to remove defects from the user's change, not to harden the
project until no reviewer can think of anything. Reviewers can always find one
more item, and every fix pass is a fresh chance to regress, so the loop needs a
fixed bar to converge to and a lead who notices when it starts reviewing itself.

## Set the Bar Before Round One

Honor a bar the user states. Otherwise decide what earns a fix and write it into
every brief: a reachable defect, a documented-rule violation, or a gap against the
requested outcome at or above the agreed severity. Fix a low-severity defect when
the remedy is a local correction. Record everything else as a follow-up instead of
fixing it: design judgments, hardening beyond the stated scope or threat model,
polish, and anything whose remedy needs a new rule, state, option, category, or
branch to cover a case outside supported use. "Cheap to write" is not a reason to
fix; what the change adds and what it can break are.

Clean means no remaining accepted findings at this bar on a fully reviewed final
version. Tell reviewers the bar and that items below it belong under Follow-ups,
so they calibrate instead of filling a list.

## Review, Fix, and Review Again

1. Run the review workflow in [SKILL.md](../SKILL.md) against a frozen target. Verify
   and classify findings against the bar before editing. Reviewer suggestions are
   advisory, and a reviewer's own low or design-judgment rating is evidence about
   the bar, not an invitation to fix the item because the change looks small.
2. Batch accepted findings into one coherent fix pass. Apply the smallest change
   that removes the trigger at its owner; prefer removing or simplifying to adding.
   Inspect sibling instances within the target when the same bug may recur. Keep
   reviewers read-only; the lead owns implementation and integration.
3. Run focused validation and required repository checks after the fixes. For a
   behavior bug, prefer a reproduction or regression check that fails before the
   fix and passes after it. Do not add tests that mirror the implementation or
   scaffolding for low-impact prose changes.
4. Freeze the updated target, keeping the original comparison base so reviewers
   can inspect the cumulative change. Include the fix delta and validation results.
5. Re-review with independent reviewers sized to the delta, not to the first
   panel: one reviewer carrying the relevant lenses can verify a small, local
   delta; rerun the full panel only when the fix pass was broad, architectural,
   security-boundary, or public-contract. Carry forward coverage for unchanged
   surfaces. Ask three questions: is each prior accepted finding resolved, did the
   delta introduce a regression, and does the delta contain a defect at the bar.
   Do not ask for residual threats, further hardening, or anything else the
   reviewer can think of; an open question in a brief is answered with a finding.
   Prepare the assignment with the [reviewer brief](reviewer-brief.md#re-review-assignments)
   and monitor as in [SKILL.md](../SKILL.md#monitor-and-steer-the-panel).
6. Verify the new findings, classify them against the bar, and repeat while
   accepted findings remain. Summarize each round for the user: what was fixed,
   what was deferred and why, and the size of the delta.

## Check for Convergence at Each Round Boundary

Before starting another fix pass, look at what the round's accepted findings are
about. The loop is converging when they concern the original change, severity is
falling, and the delta is shrinking.

It is spiraling when findings are mostly about the previous fix pass; when a
remedy needs another rule, branch, state, or message to cover the case the last
fix created; when the same component is patched in consecutive rounds; when fix
passes keep introducing regressions; or when the cumulative change has grown well
beyond the user's original change. At that point the panel is inspecting its own
work rather than the user's, and each pass costs more than it removes.

When you see these signs, stop extending the fix. Revert or simplify the change
that started the chain, keep only what removes a real defect, record the rest as
follow-ups, and tell the user what you did and why. Finish with a narrow
verification of the last delta rather than another full round: one independent
reviewer when the delta changes behavior, your own check plus validation when it
is a local correction the reviewers' evidence already covers. Say which in the
report; a clean verdict rests on independent coverage of every behavior change.

## Completion and Limits

A clean result requires no remaining accepted findings at the bar, completed
applicable review coverage of the final version, and passing required validation
on it. Record rejection reasons and follow-ups. Once those conditions hold, stop;
do not launch another round to obtain a more reassuring report.

If validation cannot run or an external check fails, report what is verified and
what remains blocked. Do not call the overall result clean. A timed-out reviewer
or unavailable evidence is a gap to resolve or disclose, not a pass.

Resolve conflicting advice from the project's requirements and record the decision.
Do not repeatedly reverse a fix because another reviewer prefers a different
design. Do not reject a substantiated issue solely to finish the loop.

When a finding recurs after attempted fixes, identify the assumption those fixes
share and check it against the failing path before trying another patch. Seek a
root-cause correction within scope; do not accumulate compensating workarounds.

If that investigation cannot restore progress, or a necessary fix exceeds the
authorized scope, stop with the remaining issue, attempted fixes, evidence, and
the decision or access needed. Continue independent work that remains within
scope; ask only for what actually blocks completion.

## Final Report

Use the report described in [SKILL.md](../SKILL.md), adding a per-round ledger:
findings fixed, reviewers and lenses rerun, anything reverted or simplified and
why, follow-ups deferred with their reasons, the final target version, final
validation results, and either the clean result or the exact unresolved blockers.
Retain enough evidence to distinguish an initial finding from a verified fix and
a remaining problem.
