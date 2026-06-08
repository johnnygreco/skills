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

| Skill | What it does | When to use | Docs |
| --- | --- | --- | --- |
| [`panel-review`](skills/panel-review) | Runs specialist reviewers against a PR, branch, design, or substantial change, then fixes accepted findings and re-reviews until clean. | Before merging work where a single review pass is likely to miss something important. | [Example: GitHub goal delivery with panel review](docs/github-goal-delivery-with-panel-review.md) |
| [`github-goal-delivery`](skills/github-goal-delivery) | Breaks a larger GitHub-backed goal into tracked issues and focused PRs, with review gates along the way and a final pass over the whole result. | For work large enough to need GitHub issues and PRs as durable state. Requires issue and PR access. | [Example: GitHub goal delivery with panel review](docs/github-goal-delivery-with-panel-review.md) |

## Contributing & authoring

See [AGENTS.md](AGENTS.md) for layout rules and validation before adding or editing a skill.

## License

Apache License 2.0. See [LICENSE](LICENSE). A skill may include its own `LICENSE.txt` if it needs different terms.
