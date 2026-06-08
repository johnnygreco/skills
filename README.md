# Agent Skills

A small, evolving set of agent skills I'm actively experimenting with. Each one packages a focused workflow — instructions, and any scripts or references an agent needs — so a capable agent can pick it up and run with it.

These follow the [Agent Skills specification](https://agentskills.io/specification) and work with Claude Code, Codex, and other compatible agents.

> Consider these experimental. They change as I learn what works.

## Install

Install with the [Skills CLI](https://skills.sh):

```bash
npx skills add johnnygreco/skills
```

It walks you through selecting which skills to install, whether to install them for the current project or globally, and which agent harnesses to set them up for.

To browse or update later:

```bash
npx skills check     # see available updates
npx skills update    # update installed skills
```

## Catalog

| Skill | What it does | When to use | Combined workflow |
| --- | --- | --- | --- |
| [`panel-review`](skills/panel-review) | Runs an independent, multi-agent expert panel that reviews a change across robustness, correctness, maintainability, complexity, tests, security, and more — then fixes accepted findings and re-reviews until clean. | You want a deep, merge-readiness review of a PR, branch, design, or substantial change — beyond a single-pass look. | [GitHub goal delivery with panel review](docs/github-goal-delivery-with-panel-review.md) |
| [`github-goal-delivery`](skills/github-goal-delivery) | Drives a long-horizon, multi-PR goal using GitHub issues as the durable tracker and pull requests as the reviewer interface: decompose into self-contained issues, ship sequential PRs, review independently, then review holistically. | You're handing an agent a big goal that spans many PRs and needs durable tracking and review. Requires GitHub issue and PR access. | [GitHub goal delivery with panel review](docs/github-goal-delivery-with-panel-review.md) |

## Contributing & authoring

Authoring conventions, layout rules, and validation steps live in [AGENTS.md](AGENTS.md) — read that before adding or editing a skill.

## License

Apache License 2.0. See [LICENSE](LICENSE). A skill may include its own `LICENSE.txt` if it needs different terms.
