# Correctness

Does the behavior hold across supported situations, including failure?

- Trace inputs through state changes and outputs. Check the invariants callers
  rely on, including realistic boundary cases.
- Examine partial failure, repeated work, interruption, and recovery wherever
  they can leave behavior inconsistent.
- Consider ordering, shared state, and resource lifetime when they affect the
  result. Identify an actual sequence that can violate the contract.
- Determine whether the change introduces a problem or exposes a previously
  dormant one. Separate unrelated existing defects.

Before accepting a hypothetical failure, inspect the caller and any upstream
constraint that could prevent it. Connect the finding to a reachable scenario and
observable consequence.
