# Design

Is the solution understandable, cohesive, and proportionate to the problem?

- Follow a likely change through the design. Look for scattered knowledge,
  unclear ownership, or callers that must understand another module's internals.
- Judge abstractions by the complexity they hide, the work they save, and the
  boundaries they enforce. Weigh those benefits against concrete maintenance
  costs in this project.
- Look for opportunities to remove redundant decisions or moving parts at their
  owner without shifting the same burden onto callers.
- Check how the change represents its domain. Rules kept in one place, such as
  a state machine, a typed model, or a table, stay consistent. The same rules
  repeated across conditionals, or in flags that must stay in sync, drift
  apart. When a change adds another case to a chain of branches that encodes
  such rules, report it if a likely change would have to update the rules in
  several places.
- Check that each piece of state has one owner, each task one supported way,
  and each list one source the others derive from. Duplicates diverge when a
  later change updates only the copy it sees.
- Ask whether a new requirement was designed in or bolted on. Would the code
  look like this if the requirement had been known from the start?
- Check that the change solves its problem where the problem originates. A
  special case, flag, suppressed error, or caller-side check that compensates
  for a flaw elsewhere leaves the flaw in place for the next caller.
- Respect project terminology, constraints, and architectural decisions. Explain
  concrete maintenance costs rather than treating design heuristics as rules.
  Clear, local code that is unlikely to grow needs no added structure.

Evaluate the proposed remedy as critically as the existing design. Recommend the
change the cause requires, whatever its size. A patch that leaves a design
problem in place falls short of that; unrelated restructuring and speculative
extensibility go beyond it.
