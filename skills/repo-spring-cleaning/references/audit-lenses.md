# Audit Lenses

Use this as a checklist bank. Select lenses based on the repository rather than
running every item mechanically.

## Repository Shape

- Confirm the intended project layout, source roots, generated files, vendored
  files, examples, tests, scripts, docs, and release artifacts.
- Check `.gitignore`, editor/tool config, packaging metadata, and root docs for
  contradictions or stale references.
- Look for duplicate concepts spread across docs, scripts, config, and code.

## Build, Test, And CI

- Discover the canonical install, lint, type-check, test, build, and validation
  commands from docs and CI. Prefer commands the project already advertises.
- Verify local commands align with CI and do not depend on hidden state.
- Check whether changed behavior has tests that would fail if regressed.
- Flag flaky, skipped, or over-mocked tests when they hide real health risks.

## Language And Framework Standards

- Identify each language and framework in use, then inspect the local idioms
  before applying generic style rules.
- Prefer the repository's existing abstractions and formatters over new patterns.
- Check error handling, resource cleanup, typing, async/concurrency behavior,
  public API contracts, and boundary validation where relevant.

## Dependencies And Supply Chain

- Inspect dependency manifests, lockfiles, tool versions, engines, and package
  scripts for drift.
- Do not upgrade dependencies just to appear current. Upgrade only for concrete
  compatibility, security, correctness, or maintenance reasons, and validate.
- Watch for unused dependencies, unsafe scripts, checked-in secrets, private
  registry leaks, license surprises, and generated lockfile churn.

## Architecture And Maintainability

- Look for needless abstraction, duplicated concepts, unclear ownership,
  dead branches, stale compatibility layers, hidden global state, and files that
  have become incohesive.
- Prefer small simplifications that reduce future reasoning cost.
- Avoid broad rewrites unless the evidence shows localized fixes cannot address
  the health problem.

## Documentation And Onboarding

- Verify README, install steps, examples, environment variables, release notes,
  troubleshooting, and contribution docs against the current project.
- Remove obsolete prose, marketing filler, repeated explanations, and commands
  that no longer work.
- Keep docs concise but operational: a new maintainer should know how to install,
  validate, develop, release, and recover from common failures.

## Agent Instructions And Skills

- Inspect AGENTS files, prompt assets, skills, tool metadata, and agent-specific
  examples for accuracy and overlap with ordinary docs.
- A skill is justified when it changes agent behavior at task time through
  trigger guidance, workflow, tool usage, scripts, references, or assets.
- Prefer ordinary docs for durable project facts that every maintainer needs,
  and skills for procedural guidance that should load only for matching tasks.
- Check skill names, frontmatter, allowed folders, concise bodies, linked
  references, no local absolute paths, no private URLs, and no secrets.

## Security And Privacy

- Search for committed credentials, unsafe defaults, sensitive logs, insecure
  examples, broad permissions, injection surfaces, path traversal, SSRF, XSS,
  deserialization, and command execution risks tied to repository code.
- Treat illustrative fixtures differently from real production contracts, but
  remove fake secrets that are likely to be copied into real use.

## Performance And Operations

- Review hot paths, startup scripts, package size, slow CI steps, caching,
  concurrency, retries, timeouts, migration safety, rollback notes, and
  observability when the repository owns operational behavior.
- Flag only issues supported by project scale, documented requirements, or
  concrete evidence.

## Release Readiness

- Inspect versioning policy, changelog or release notes, package metadata,
  generated artifacts, publish scripts, tags, and CI release workflows.
- For patch releases, verify the changes are backward-compatible fixes or
  maintenance improvements unless the user explicitly permits more.
- Do not cut or publish a release unless the user requested it and validation,
  review, and repository release conventions are satisfied.
