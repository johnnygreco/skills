# Agent Skills

A small, evolving set of agent skills I'm actively experimenting with.

The skills follow the [Agent Skills specification](https://agentskills.io/specification) and work with Claude Code, Codex, and other compatible agents.

## Install

Use the [Skills CLI](https://skills.sh):

```bash
npx skills add johnnygreco/skills
```

The CLI asks which skills to install, where to install them, and which agent tools to configure.

To browse or update later:

```bash
npx skills check     # see available updates
npx skills update    # update installed skills
```

## Catalog

| Skill | What it does | When to use |
| --- | --- | --- |
| [`repo-spring-cleaning`](skills/repo-spring-cleaning) | Runs an evidence-based repository spring cleaning pass, including docs, tooling, agent assets, validation, and independent review when available. | For periodic maintenance or broad cleanup work that should improve maintainability without changing behavior. |
| [`panel-review`](skills/panel-review) | Spawns independent review agents with tailored lenses and produces a verified report. Fixes and repeats review until clean only when explicitly requested. | For deep review of a PR, branch, design, or substantial change. |
| [`blast-radius`](skills/blast-radius) | Traces downstream effects and verifies critical assumptions, returning an impact report. | For investigating what a change could break, on its own or within a panel review. |

## Contributing & authoring

See [AGENTS.md](AGENTS.md) for layout rules and validation before adding or editing a skill.

## License

Apache License 2.0. See [LICENSE](LICENSE). A skill may include its own `LICENSE.txt` if it needs different terms.
