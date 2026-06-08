# Repository Instructions

This repository publishes reusable Agent Skills.

## Layout

- Put each skill directly in `skills/<skill-name>`.
- Do not create auxiliary docs inside individual skill folders. A skill folder should contain only `SKILL.md` and resources the agent may use: `agents/`, `scripts/`, `references/`, and `assets/`.

## Creating Or Editing Skills

- Use the `skill-creator` guidance when available.
- Keep skill names lowercase with digits and hyphens only.
- Match `SKILL.md` frontmatter `name` to the folder name.
- Put all trigger guidance in the frontmatter `description`; the body is loaded only after selection.
- Keep `SKILL.md` concise and move detailed material to linked reference files.
- Add `agents/openai.yaml` when Codex UI metadata, invocation policy, or tool dependencies are useful.
- Do not commit secrets, private URLs, proprietary snippets, or local absolute paths.

## Validation

Run validation before finishing skill changes:

```bash
scripts/validate-skills.py
```

Or validate one skill directly with the reference validator:

```bash
uvx --from skills-ref agentskills validate skills/SKILL_NAME
```

If a skill includes scripts, run a representative sample and report the command used.

## Publishing checklist

- Keep repository-level docs in the root (`README.md`, `AGENTS.md`), not inside individual skill folders.
- Keep each skill focused on one job.
- Move large or variant-specific details out of `SKILL.md` into `references/`.
- Test any scripts a skill ships before publishing.
- Do not commit credentials, private URLs, proprietary material, or machine-local paths.
