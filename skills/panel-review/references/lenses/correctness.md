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
- When the change is a fix, check that it removes the cause and not only the
  reported instance. Ask whether the state that triggered the failure can
  legitimately occur. If it can, handling it is the fix. If it should never
  exist, a guard, retry, swallowed error, clamped value, or discarded state
  hides the defect, and the fix belongs where that state is produced. Look for
  sibling paths that reach the same failure.

Before accepting a hypothetical failure, inspect the caller and any upstream
constraint that could prevent it. Connect the finding to a reachable scenario and
observable consequence.
