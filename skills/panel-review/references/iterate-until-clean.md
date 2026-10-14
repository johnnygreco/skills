# Iterate Until Clean

This workflow applies only after the user explicitly requests repeated fixing and
review. Preserve the original scope and any existing authorization; the request
does not authorize unrelated redesign, publishing, or merging.

## Review, Fix, and Review Again

1. Run the review workflow in [SKILL.md](../SKILL.md) against a frozen target. Verify
   and classify findings before editing; reviewer suggestions are advisory.
2. Batch accepted findings into a coherent fix pass. Fix at the appropriate owner
   and inspect sibling instances within the target when the same bug may recur.
   Keep reviewers read-only; the lead owns implementation and integration.
3. Run focused validation and required repository checks after the fixes. For a
   behavior bug, prefer a reproduction or meaningful regression check that fails
   before the fix and passes after it. Do not add tests that simply mirror the
   implementation or test scaffolding for low-impact prose changes.
4. Freeze the updated target, keeping the original comparison base so reviewers
   can inspect the cumulative change. Include the fix delta and validation results.
5. Spawn independent review agents again for every lens whose finding led to a
   fix and every risk surface affected by those fixes. Redesign and rerun the full
   panel for broad, architectural, security-sensitive, or public-contract changes.
   Monitor and steer each round as described in [SKILL.md](../SKILL.md#monitor-and-steer-the-panel).
   Give reviewers the updated artifacts and relevant cases to verify without
   telling them to confirm the lead's conclusion. They must check for regressions
   as well as whether the original issue was addressed.
6. Verify new findings and repeat the fix/review cycle while accepted issues
   remain. Carry forward prior coverage only for unchanged surfaces of the same
   target. Do not stop at tests passing or fixes being applied: the updated target
   must receive a completed review with no remaining accepted findings.

## Completion and Limits

A clean result requires no remaining accepted findings, completed applicable
review coverage, and passing required validation on the final version. Record
rejection reasons and out-of-scope follow-ups. Once those conditions hold, stop;
do not launch another round just to obtain a more reassuring report.

If validation cannot run or an external check fails, report what is verified and
what remains blocked. Do not call the overall result clean. Likewise, a timed-out
reviewer or unavailable evidence is a gap to resolve or disclose, not a pass.

Resolve conflicting advice from the project's requirements and record the decision.
Do not repeatedly reverse a fix just because another reviewer prefers a different
design. Do not reject a substantiated issue solely to finish the loop.

When a finding recurs after attempted fixes, identify the assumption those fixes
share and check it against the failing path before trying another patch. Seek a
root-cause correction within scope; do not accumulate compensating workarounds.

If that investigation cannot restore progress, or a necessary fix exceeds the
authorized scope, stop with the remaining issue, attempted fixes, evidence, and
the decision or access needed. Continue independent work that remains within
scope; ask only for what actually blocks completion.

## Final Report

Use the report described in [SKILL.md](../SKILL.md), adding the findings fixed,
rounds and lenses rerun, final target version, final validation results, and either
the clean result or exact unresolved blockers. Retain enough evidence to
distinguish an initial finding from a verified fix and a remaining problem.
