---
name: repo-spring-cleaning
description: >-
  Use when the user asks for repository spring cleaning, periodic codebase
  maintenance, deep repo audit with cleanup, comprehensive cleanup,
  documentation streamlining, dependency/tooling hygiene, agent-instruction or
  agent-skill audit, or release-readiness cleanup across a codebase. Guides
  evidence-based inventory, behavior-preserving cleanup and refactoring,
  validation, independent review, and repeatable maintenance reporting for any
  language or repository.
metadata:
  short-description: Repository spring cleaning
---

# Repo Spring Cleaning

Run an evidence-based maintenance pass that leaves the repository cleaner,
better documented, and easier to keep healthy. Prefer small, defensible fixes
over speculative rewrites.

## Contract

- Treat the user's objective, repository instructions, current worktree, and
  project docs as the source of truth. Preserve user changes.
- Start with inventory before edits: languages, package managers, CI, release
  process, validation commands, docs, agent instructions, generated files, and
  ownership boundaries.
- Use high-confidence cleanup by default: stale docs, broken commands, dead
  references, invalid config, duplicated instructions, obvious code smells, and
  missing validation around touched behavior.
- Preserve product and runtime behavior by default. Limit code edits to
  behavior-preserving refactors and hygiene fixes; record suspected behavior
  bugs or semantic changes as findings or follow-ups unless the user explicitly
  authorizes fixing them.
- Do not remove code, docs, dependencies, or skills merely because they look
  unused. Find evidence first, then record the rationale.
- If the work is broad enough to need durable coordination, use an available
  goal-delivery skill or project tracker before making sweeping changes.
- Use `panel-review` for substantive cleanup, refactoring, documentation
  rewrites, agent-skill pruning, or release preparation when it is available.
  If it is not available, use another independent reviewer or subagent workflow
  with a frozen target. If no independent review is possible, stop before broad
  or destructive cleanup unless the user explicitly accepts the risk, and record
  the missing review gate as remaining risk.
- Keep the result reproducible: record changed files, commands, validation
  output, accepted/rejected review findings, remaining risks, and follow-ups.

## Workflow

1. **Scope the check.** Restate the spring-cleaning goal, explicit release or
   publishing requirements, non-goals, and risk tolerance. Ask only for missing
   decisions that cannot be safely inferred.
2. **Build a baseline.** Inspect repository instructions, README, contribution
   docs, CI, package manifests, lockfiles, test config, release metadata, and
   git status. Identify generated or vendored files to avoid editing by hand.
   For repositories with code, record each detected language/framework,
   package manager or toolchain, formatter, linter, type checker, test/build
   command, key config file, and local idiom or contract inspected. Skip this
   only with an explicit no-code/runtime-surface rationale.
3. **Select audit lenses.** Read [audit-lenses.md](references/audit-lenses.md)
   and choose only the lenses relevant to this repository. Note skipped lenses
   when they would otherwise be expected.
4. **Plan cleanup slices.** Group findings into safe quick fixes, risky changes
   that need review, and follow-ups. Keep each implementation slice cohesive;
   split work that crosses many ownership boundaries.
5. **Clean deliberately.** Update docs and agent instructions to match reality,
   remove stale material with evidence, simplify overcomplicated code without
   changing behavior, align tooling with language norms, and add or repair
   tests that prove touched areas still behave as expected.
6. **Validate.** Run the repository's documented validation commands plus any
   targeted checks for touched areas. If a skill is changed, run its validator.
   If a script is changed or added, also run a representative sample and report
   the command used.
7. **Review and iterate.** Freeze the diff, run `panel-review` or another
   available independent review workflow, verify every reviewer finding against
   the codebase, fix accepted issues, rerun validation, and repeat review where
   the fix changes the reviewed surface. Do not substitute a single self-review
   for unavailable independent review.
8. **Report.** Use [report-template.md](references/report-template.md) for the
   final maintenance summary or tracker/PR update.

## Agent Skills And Instructions

When the repository contains skills, prompts, AGENTS files, or other agent-facing
assets, audit them as first-class maintainability surfaces:

- Keep trigger guidance in skill frontmatter and keep loaded bodies concise.
- Move detailed but useful material to `references/`; remove material that
  belongs in ordinary project docs instead of a skill.
- Validate folder names, frontmatter names, allowed files, local path leaks,
  secrets, and representative script behavior.
- Remove or merge skills only when repository evidence shows they are stale,
  redundant, misleading, or better represented as documentation.
