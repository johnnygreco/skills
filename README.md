# Agent Skills

Public catalog of reusable agent skills.

Skills in this repository follow the [Agent Skills specification](https://agentskills.io/specification) and are intended for Codex and other compatible agents. Each skill is a focused folder of instructions, optional scripts, references, and assets.

## Repository Layout

```text
skills/
  skill-name/
    SKILL.md
    agents/openai.yaml
    scripts/
    references/
    assets/
```

- `skills/<skill-name>/`: one reusable skill per directory.
- `agents/openai.yaml`: optional Codex UI metadata, invocation policy, and tool dependency declarations.

## Installing Skills

After this repository is published, install a skill by pointing your agent at the skill folder.

For Codex, ask the installer skill to install the GitHub skill folder:

```text
Use $skill-installer to install https://github.com/OWNER/REPOSITORY/tree/main/skills/SKILL_NAME
```

For GitHub Copilot CLI, once skills are published through GitHub's skill flow:

```bash
gh skill preview OWNER/REPOSITORY SKILL_NAME
gh skill install OWNER/REPOSITORY SKILL_NAME
```

For manual local use, copy or symlink a skill directory into one of the locations supported by your agent, such as `$HOME/.agents/skills` for user-wide skills or `.agents/skills`, `.github/skills`, or `.claude/skills` for repository-scoped skills.

## Adding a Skill

Create new skills directly in `skills/<skill-name>`.

Minimum skill structure:

```text
skill-name/
  SKILL.md
```

`SKILL.md` must start with YAML frontmatter:

```md
---
name: skill-name
description: Describe exactly what the skill does and when an agent should use it.
---
```

Keep names lowercase with digits and hyphens only. Match the directory name exactly. Put trigger conditions in `description`, because agents use that field before loading the full skill body.

## Validation

Validate all skills:

```bash
scripts/validate-skills.py
```

Validate one skill directly with the reference validator:

```bash
uvx --from skills-ref agentskills validate skills/SKILL_NAME
```

## Publishing Checklist

- Keep repository-level docs in the repository root, not inside individual skill folders.
- Keep each skill focused on one job.
- Move large or variant-specific details from `SKILL.md` into `references/`.
- Test scripts included in a skill before publishing.
- Do not commit credentials, private URLs, proprietary source material, or machine-local paths.
- Inspect third-party skills before installing them, especially skills that include scripts.
- Use `gh skill publish --dry-run` before publishing through GitHub's skill flow.
- Package skills as a Codex plugin later if you want an installable distribution unit that bundles multiple skills, apps, MCP settings, or presentation assets.

## License

The repository is MIT licensed by default. A skill can include its own `LICENSE.txt` if it needs different terms.
