# Verification

Does the available evidence justify confidence in the changed behavior?

- Map important claims to checks that exercise the relevant behavior through
  the interfaces actually used. Identify integration gaps where isolated evidence
  does not reach the risk.
- Ask whether a plausible broken implementation would fail the check. Expected
  results should come from an independent example or contract.
- Inspect mocks, fixtures, and snapshots for assumptions that conceal defects.
  Avoid tests that merely restate implementation details.
- Separate checks run on this version from earlier results, proposed checks, and
  conclusions based only on inspection. Consider evidence appropriate to the
  artifact, including a workflow walkthrough for instructions or designs.

Explain what a missing check would establish and why it matters. Do not demand
redundant assertions or test scaffolding for low-impact prose changes.
