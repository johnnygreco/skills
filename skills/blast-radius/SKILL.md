---
name: blast-radius
description: Blast radius, downstream impact, or what could this break.
---

# Blast Radius

Trace a change's consequences through the surrounding system and check the
assumptions that determine whether supported behavior remains intact. Return an
evidence-backed impact report.

## Establish the Question

Reuse the caller's frozen target, context, and scope. For a standalone request,
resolve the change and comparison point, record versions or diff commands, and
make included staged, unstaged, and untracked work explicit. Preserve a snapshot
when needed; do not alter user work to obtain one.

State the behavior that changes and the question being investigated. Identify
supported consumers and operating conditions from evidence. Ask for missing
context only when it prevents a useful investigation.

When invoked by a panel reviewer, stay within that reviewer's assignment and
return evidence to the lead. This investigation does not expand the repair scope
or require another panel. Report by default; changes need separate authorization.

## Trace Consequences

Follow causal paths from changed behavior to affected contracts, state, and
consumers. Search for direct uses, then examine connections that names alone
may miss:

- Shared data representations, configuration, persisted records, and messages
  consumed across language or process boundaries.
- Ordering, ownership, lifecycle, and failure recovery that callers rely on.
- Dependencies at the pinned version, including local modifications.
- Versions or environments that coexist during build, rollout, or operation.

For each plausible material effect, connect the changed behavior to a supported
scenario and observable consequence. Inspect upstream constraints before calling
a failure reachable. Continue until the path reaches an affected consumer, an
enforced boundary rules it out, or missing evidence prevents resolution.

Prioritize paths that can change the answer. Keep unrelated pre-existing issues
outside the investigation. When a boundary is inaccessible, state what is unknown
instead of inventing downstream consumers or treating a search miss as proof.

## Check the Critical Assumptions

Identify the few facts on which the impact assessment depends. For each, state
what would falsify it and seek evidence appropriate to its consequence:

- **Source evidence:** the contract, implementation, or pinned dependency supports
  the claim; cite the relevant location.
- **Path reasoning:** a concrete input, state, or execution sequence establishes
  how the effect occurs or why a constraint prevents it.
- **Observed behavior:** a targeted check runs the relevant implementation and
  records the inputs, command, version, and result.

Prefer a focused test, temporary script, or application reproduction for a
consequential assumption that inspection cannot settle. Exercise the real path
with an independent expected result; a mock that assumes the disputed behavior
cannot establish it. Match the check to the claim: a narrow unit check may leave
an integration or timing assumption unresolved.

Keep temporary checks and their outputs isolated from reviewed files and live
systems. Preserve useful commands or artifacts for reproduction. If execution is
unavailable, report the evidence obtained and the remaining uncertainty; do not
present reasoning as a test result. A successful check supports the conditions
tested, not every possible use.

## Report the Impact

Return a concise report with:

- The target, question, and observed or intended behavior change.
- Confirmed risks: affected consumer or contract, trigger, consequence, and evidence.
- Material concerns investigated and ruled out, with the constraint or observation
  that ruled them out.
- Critical assumptions and whether each is supported, contradicted, or unverified,
  including the evidence method and reproduction commands when applicable.
- Unresolved boundaries and the smallest next check that would settle them.

Stop when the question has an evidenced answer or a clearly identified evidence
gap. For a proposed design, distinguish intended effects from implementation facts
that cannot yet be checked. Return findings to the requesting reviewer without
starting fixes, publishing a review, or declaring the whole change safe.
