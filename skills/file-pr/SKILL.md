---
name: file-pr
description: File, open, or create a pull request, or refresh an open PR's description.
disable-model-invocation: true
---

# File PR

Turn finished work into a pull request that a reviewer understands in a minute.
The description is written for people: say what problem the change solves and
what is different now, in plain words, before any technical detail.

Use this skill for every pull request, even when the repository has its own
pull request skill. Still honor the repository's conventions: its
`.github/PULL_REQUEST_TEMPLATE.md`, branch, commit, and title styles, and
writing rules.

## Prepare the Branch

1. Check whether a pull request for this branch already exists. Update it
   rather than opening a second one.
2. Read `git status --short` and the diff against the base branch (usually
   `origin/<default-branch>`). Confirm the contents match the goal and nothing
   unrelated is included. Stage paths by name so files another agent is editing
   in the same checkout stay out.
3. On the default branch, create a branch first. Follow the repository's naming;
   otherwise use `<owner>/<topic>` in lowercase with hyphens.
4. Commit one coherent change per commit. Follow the repository's commit style
   from `git log`; otherwise write a one-line subject in the imperative mood and
   sentence case, with no trailing period, that says what the change does. Do
   not add `Co-Authored-By`, "Generated with", or other AI attribution.

## Write the Title

Titles usually become commit messages, so follow the repository's title
conventions; look at recently merged pull requests for examples. Say why the
change matters, not how it works:

> ❌ perf(server): negotiate permessage-deflate on the websocket

> ✅ perf(server): cut websocket frame size by 70%+ with gzipping

## Write the Overview

The overview is the opening of the description and the part most people read.
Write it for a teammate who knows the product but has not seen this code.

- Open with the problem as someone experienced it, drawn from the user's
  original request; if the request names no problem, say what was asked for
  and why, without inventing one. Then say what is different now. Keep it short enough to
  take in at a glance.
- Use everyday words. Name things by what people see or do, not by function,
  file, flag, or class names. If a technical term is unavoidable, say what it
  means.
- Be concrete: a before and after, an example, or a number beats an abstract
  claim.
- Do not open with an inventory of edits or restate the diff in prose. That
  detail belongs under "What changed", if anywhere.
- Reread it as an outsider. If they could not say what changed and why it
  matters, rewrite it.

> ❌ Removed implicit workspace carry-over from every "new thread" entry point (cmd+n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads inherit only the project from context; branch, worktree, and env mode always come from the configured defaults. Deleted buildContextualThreadOptions, startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.

> ✅ My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

## Fill In the Body

With a template, keep every heading, write "None" under one with nothing to
say, and replace each prompt comment with its answer. Without one, use the
overview followed by these sections:

- **What changed:** short bullets, each starting with one emoji: ✨ new
  capability · 🔧 changed behavior · 🐛 fix · 📝 docs · 🧪 tests · 🧹 removal or
  cleanup · ⚙️ tooling, build, or dependencies. Do not include the legend.
  Keep the wording plain here too; add technical detail only where a
  reviewer needs it.
- **Verification:** what you ran or observed on the head commit and the result,
  plus any check you did not run and why.
- **Deferred:** only work that was asked for and is not in this pull request,
  linked to its issue. Omit the section when there is none.

Add `Closes #<n>` when the pull request resolves an issue. Do not add AI
authorship credits, "Created with" or "Generated with" footers, or badges.

Write each paragraph and list item on one line: GitHub renders every newline in
a pull request body as a line break. Before submitting, check the title,
description, quotes, and attachments for secrets and private details.

## Open

1. Push with `git push -u origin <branch>`.
2. Write the body to a file in the repository's gitignored working folder, or a
   temporary file, and run
   `gh pr create --base <base> --title "<title>" --body-file <file>`. Open a real
   pull request rather than a draft so review bots run, unless the user asked
   for a draft.
3. If `gh pr create` fails because the GraphQL rate limit is used up, open it
   through REST:
   `gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@<file>`.
4. Report the URL.

Do not post a follow-up comment unless it serves the user's request; when one
is needed, use the `leaving-pr-comments` skill. If the user also asked to
babysit the pull request, continue with the `babysit-pr` skill. Merge only when
the user says to.

## Keep the Description True

When the head commit changes after review fixes or a rebase, update the
description so it still matches the pull request: rewrite the overview if the
outcome changed, and refresh the verification section. Use
`gh pr edit <n> --body-file <file>`, or
`gh api -X PATCH repos/<owner>/<repo>/pulls/<n> -F body=@<file>` when GraphQL is
used up.
