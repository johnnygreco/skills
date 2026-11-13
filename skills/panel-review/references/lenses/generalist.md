# Generalist

What material issue might a focused review overlook across the target as a whole?

- Judge the change in the context of the full codebase, not just the diff.
  Explore beyond the changed files: does it fit the existing architecture and
  conventions, reuse or duplicate existing code, and keep callers, contracts,
  and shared assumptions elsewhere intact? For other artifacts, trace the whole
  artifact, its intended use, and supporting evidence.
- Prioritize by consequence: reachable defects and contract breaks first, then
  gaps against the requested outcome, then documented-rule violations.
- Where another reviewer owns a lens, your independent read of the same ground
  is the point; do not skip an area because someone else covers it.
- Hold the same evidence standard as a focused lens: concrete trigger, location,
  and observable consequence.

Every panel includes at least one Generalist. Use it for broad coverage and to
connect risks across focused assignments. It does not replace the lead's coverage accounting or imply that
every perspective has been examined deeply.
