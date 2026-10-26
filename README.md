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
| [`panel-review`](skills/panel-review) | Spawns independent review agents with tailored lenses and produces a verified report. | For deep review of a PR, branch, design, or substantial change. |
| [`blast-radius`](skills/blast-radius) | Traces downstream effects and verifies critical assumptions, returning an impact report. | For investigating what a change could break, on its own or within a panel review. |
| [`show-me-your-work`](skills/show-me-your-work) | Maintains an append-only decision log with evidence, verification outcomes, and a handoff audit. | For long-running or unattended work that needs a reviewable trail, or auditing an existing trail. |
| [`sol-loop`](skills/sol-loop) | Loops a single GPT Sol reviewer over a change within a small round budget, keeping fixes minimal and recording a findings ledger. | When you say "sol loop" to harden a change before or after filing a PR. |
| [`full-send`](skills/full-send) | Takes a change to a merged PR unattended: proof, Sol review, filing, a panel review, babysitting, and merge once the gate passes. | When you say "full send" and won't be watching the thread. |
| [`full-stop`](skills/full-stop) | Runs the `full-send` workflow but stops with the PR ready for you to merge. | When you say "full stop" and want to make the final merge call. |
| [`babysit-pr`](skills/babysit-pr) | Watches a PR through CI and bot review with an event-driven watcher, fixing real findings and declining the rest. | When asked to monitor, watch, or babysit a PR. |
| [`leaving-pr-comments`](skills/leaving-pr-comments) | Formats agent-authored GitHub comments with an attribution callout and a direct style. | Whenever an agent comments on GitHub on your behalf. |
| [`file-pr`](skills/file-pr) | Commits and opens a pull request whose overview explains the problem and the result in plain words before any technical detail. | When you invoke it explicitly, and whenever `full-send` or `full-stop` files a PR, even if the repository has its own PR skill. |

## Contributing & authoring

See [AGENTS.md](AGENTS.md) for layout rules and validation before adding or editing a skill.

## Credits

- [`sol-loop`](skills/sol-loop), [`full-send`](skills/full-send), [`full-stop`](skills/full-stop), [`babysit-pr`](skills/babysit-pr), and [`leaving-pr-comments`](skills/leaving-pr-comments) come from [`t3dotgg/tstack`](https://github.com/t3dotgg/tstack/tree/main/skills), Copyright (c) 2026 Theo Browne, used under the MIT License. [`file-pr`](skills/file-pr) adapts that repository's `file-pr` skill.

## License

Apache License 2.0. See [LICENSE](LICENSE). A skill may include its own `LICENSE.txt` if it needs different terms.
