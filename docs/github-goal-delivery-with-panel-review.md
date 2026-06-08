# GitHub Goal Delivery with Panel Review

`github-goal-delivery` coordinates a long-running goal through issues and PRs. `panel-review` supplies independent specialist review for each PR before it merges.

## Usage

Start by working with your coding agent to develop a concrete plan. The plan should be specific enough that another session could pick it up: target outcome, important context, implementation phases, validation expectations, and anything that should happen after the code lands.

Put that plan in a document, then start a goal from it:

```text
/goal Use the github-goal-delivery skill to execute the plan in <path-to-plan-document>. Use panel-review for each PR. <Add any task-specific instructions, such as whether to publish a release after the goal is complete.>
```

> Warning: this workflow can burn a lot of tokens. The cost grows quickly when `panel-review` uses several specialist reviewers and runs multiple review/fix/re-review iterations for each PR.

```text
+-----------------------------+
| Big goal                    |
+-----------------------------+
              |
              v
+-----------------------------+
| github-goal-delivery        |
| - create tracker issue      |
| - split self-contained      |
|   implementation issues     |
| - order by dependencies     |
+-----------------------------+
              |
              v
+-----------------------------+
| Pick next ready issue       |
+-----------------------------+
              |
              v
+-----------------------------+
| Implement focused PR        |
| - scope: one issue          |
| - concurrency can happen    |
|   inside this issue         |
+-----------------------------+
              |
              v
+-----------------------------+
| panel-review                |
| - independent specialists   |
|   across review areas       |
| - aggregate findings        |
+-----------------------------+
      | needs changes       | clean
      v                     v
+----------------------+   +-----------------------------+
| Fix accepted review  |   | Merge PR and mark issue     |
| findings             |   | complete in tracker         |
+----------------------+   +-----------------------------+
      |                                  |
      +------ rerun panel-review         v
              on updated PR       +-----------------------------+
                                  | Any implementation issues   |
                                  | still unmerged?             |
                                  +-----------------------------+
                                      | yes              | no
                                      v                  v
                              back to pick next   +-----------------------------+
                              ready issue         | Final holistic review       |
                                                  | and tracker update          |
                                                  +-----------------------------+
                                                                |
                                                                v
                                                  +-----------------------------+
                                                  | Completed goal              |
                                                  +-----------------------------+
```
