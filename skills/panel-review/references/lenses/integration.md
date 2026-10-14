# Integration

Does the change fit the surrounding system and its delivery and operating model?

- Follow affected contracts across callers, data, configuration, and external
  dependencies, including consumers outside the edited files.
- Inspect assumptions shared across versions or environments, especially during
  transitions, rollout, and recovery.
- Trace how the result is built, distributed, configured, and operated. Check
  relevant artifacts and operational evidence instead of assuming local success
  proves the whole path works.
- Evaluate compatibility against supported consumers and explicit commitments,
  including intentional breaking changes and their adoption plan.

Focus on a concrete mismatch or failed transition. For uncertain downstream
effects, use the focused investigation described in the
[reviewer brief](../reviewer-brief.md#focused-downstream-investigation).
