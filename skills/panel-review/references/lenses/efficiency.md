# Efficiency

Does the change use time and resources reasonably for the expected workload?

- Identify input size, frequency, and resource bounds from supported use.
  Inspect how the change affects latency, throughput, memory, storage, or cost.
- Look for unnecessary repeated work, unbounded growth, or coordination that
  becomes expensive under plausible load.
- Distinguish a measured regression from a cost model or untested hypothesis.
  When measurement could change the recommendation, use a bounded, representative
  workload. Check for thresholds, contention, or environment differences before
  extrapolating; use realistic scale when necessary and feasible.
- Account for the complexity and correctness risks introduced by an optimization.

State the workload and consequence behind the finding. Avoid hypothetical scale
targets or micro-optimizations with no meaningful benefit.
