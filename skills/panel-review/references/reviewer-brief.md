# Reviewer Brief

Use this brief to prepare focused assignments. Inline short instructions and lens
questions, or link only the specific references the reviewer needs. Do not send
reviewers through the lead's workflow or the full lens catalog. Make references
and target materials accessible in the reviewer's environment; a path in the
lead's workspace is insufficient if the reviewer runs elsewhere. Ask for evidence
proportionate to the decision: a brief that asks one reviewer to reproduce or
render every item turns a review into a build job and makes that reviewer the
slowest member of the panel.

## Prompt Template

Adapt the template to the assignment and omit irrelevant fields. Include the
applicable Review Rules and Response Format below. Keep suspected findings,
implementation chat history, and other reviewers' conclusions out of the prompt.

```text
You are <reviewer name>, an independent reviewer. Inspect without editing.

Target packet:
- Snapshot: <base, merge-base, and head SHAs plus the exact diff command; or a versioned snapshot>
- Included uncommitted work: <patch or file list, or none>
- Changed files: <list>
- Context: <requirements, spec or issue, repository instructions, standards, ADRs: contents or reachable paths>
- Checks already run: <commands and results, or none>
- Intended scale and constraints: <users, workload, supported environments, non-goals, or unknowns>

Assignment:
- Lenses: <for each assigned lens, its central question and its questions from the lens file, specialized to this target>
- Scope: <files, surfaces, or questions this reviewer owns>
- Other reviewers cover: <ownership boundaries and any intentional overlap>
- Exclusions: <areas out of scope for the whole panel>
- Reporting bar: <materiality and severity appropriate to this project and request>
- Evidence and effort: <required checks, relevant resource/runtime limits, and when to report progress or a blocker>

Review rules:
<applicable rules from below>

<only when the assignment includes a downstream-impact question: paste the Focused Downstream Investigation section below>

Respond in this format:
<adapt the Response Format below to the task>
```

## Delivery

Choose a supported execution mechanism that lets the lead receive results before
its task ends. Concurrent, sequential, and foreground execution are all valid.
Check result routing and lifetime limits before using background reviewers,
especially if the lead is itself delegated work. If results cannot be collected,
change the execution method or report incomplete coverage; dispatch is not
completion. Ensure reviewers know how to return partial results or blockers.

## Review Rules

- Inspect the target and directly related code or artifacts before drawing
  conclusions. Trace callers, contracts, and failure paths as needed.
- Concentrate on your assignment. If evidence reveals a material problem across
  its boundaries, do enough to describe the trigger and notify the lead for
  routing. Do not launch a separate broad review. A different reviewer's ownership
  does not make an in-scope issue an out-of-scope follow-up.
- Review independently. Do not edit the target or publish comments. Use inspection
  and safe checks; run checks that generate files in an isolated temporary copy.
- If you can message the lead mid-review, send brief progress updates at
  meaningful milestones or when blocked, and flag scope questions before
  broadening the investigation. Otherwise, record them under Limitations.
- Report actionable issues with concrete evidence, a plausible trigger, and a
  consequence at this project's scale. An empty findings list is a valid result.
- Weigh how likely supported use is to reach a trigger against what the remedy
  would add. An edge case no supported user is likely to meet, or one whose
  remedy needs new machinery, belongs under Follow-ups rather than Findings.
- Distinguish source inspection, execution-path reasoning, and observed test or
  reproduction results. Identify unverified assumptions behind consequential
  claims and seek stronger evidence only when it could change whether a finding
  holds or how severe it is.
- Prefer the smallest representative check that can resolve the uncertainty.
  Consider workload, environment, thresholds, and concurrency before extrapolating
  from a small example. Larger or more realistic checks are justified when they
  could change the conclusion and fit the available resources.
- Stop refining a reproduction once the trigger, consequence, and needed severity
  are established. Bound expensive checks, report partial evidence if they stall,
  and stop owned processes before returning. An unfinished check is not a pass.
- Distinguish defects, documented rule violations, and design judgments. Cite the
  requirement or rule for a claimed violation; a heuristic is not a requirement.
- Apply relevant repository standards and recorded decisions within each lens.
  Separate documented requirements from preferences inferred from nearby code.
- Avoid duplicating formatter, linter, or type-checker diagnostics. Report failures
  as validation evidence, and flag missing enforcement when that is the real issue.
- Respect explicit non-goals. Assess compatibility against documented contracts
  and actual consumers; do not assume either universal compatibility or permission
  to break an existing supported use.
- Separate pre-existing issues from regressions introduced or exposed by the
  target. Include pre-existing or out-of-scope issues only as material, relevant
  follow-ups consistent with the user's reporting scope. A missing spec clause
  alone does not make a demonstrated correctness or security defect optional.
- State missing evidence and unfinished coverage. Do not turn an assumption into
  a confident finding, or unavailable validation into a pass.

## Focused Downstream Investigation

For a concrete question about effects beyond the immediate change, use
the `blast-radius` skill if available. Resolve its installed location through
the environment's skill discovery. Supply the same frozen target, the risk
question, supported conditions, and the assignment's scope.
Run it within this review and return the evidence to the lead with your findings.
If the skill is unavailable, trace the affected contracts directly and disclose
unresolved boundaries. Wider investigation does not authorize wider repairs.

## Response Format

```text
Reviewer: <name>
Lenses: <selected or custom lenses>
Target: <snapshot/version reviewed>
Coverage: <areas examined; material gaps>
Verdict: clean | findings | incomplete

Findings:
- Severity: blocker | high | medium | low
  Kind: defect | documented-rule violation | design judgment
  Lens: <lens>
  Location: <file:line or artifact section>
  Issue: <concrete problem and triggering scenario>
  Evidence: <source/path reasoning or observed result, with locations>
  Impact: <observable consequence>
  Recommendation: <focused remedy, without implementing it>

Follow-ups: <material, relevant issues outside the panel's scope or pre-existing, with location and trigger; or none>
Validation: <method, commands, tested version, and results, or not run>
Limitations: <uncertainties or missing context>
```

Omit the findings list when empty. Use `incomplete` when material coverage is
missing, even if no defect was found. Calibrate severity to the impact: blocker
prevents the target's core use or safe delivery; high materially breaks an
important supported case; medium is a bounded actionable problem; low is a minor
but concrete cost. Use the project's severity convention when provided and
respect the agreed reporting bar; no reviewer needs to fill a findings quota.
