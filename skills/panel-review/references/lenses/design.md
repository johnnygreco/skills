# Design

Is the solution understandable, cohesive, and proportionate to the problem?

- Follow a likely change through the design. Look for scattered knowledge,
  unclear ownership, or callers that must understand another module's internals.
- Judge abstractions by the complexity they hide, the work they save, and the
  boundaries they enforce. Weigh those benefits against concrete maintenance
  costs in this project.
- Look for opportunities to remove redundant decisions or moving parts at their
  owner without shifting the same burden onto callers.
- Respect project terminology, constraints, and architectural decisions. Explain
  concrete maintenance costs rather than treating design heuristics as rules.

Evaluate the proposed remedy as critically as the existing design. Prefer a
focused simplification; a finding should not become an excuse for unrelated
restructuring or speculative extensibility.
