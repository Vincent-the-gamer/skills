# AGENTS.md

## Scope

Work confined to this repository. Reads, writes, and commands all stay inside the project root; anything above it is off-limits, and reaching outside it is something to ask about first.

Scratch lives in `.tmp/` at the project root — one directory, already gitignored. Every temporary artifact (drafts, generated output, debug logs, probe scripts) goes there, so the worktree ends up exactly as the user left it. Files that are part of the change itself go to their real home in the tree, not to `.tmp/`.

## Git

The user owns git. Your job is to edit files and report what changed; committing, branching, and message-writing happen after the user reviews.

Read-only inspection — `git log`, `git diff`, `git status`, `git show` — is fair game for understanding history and pending work. Everything that writes is a hand-off: `add`, `commit`, `push`, `pull`, `switch`/`checkout`, `restore`, `reset`, `stash`, `merge`, `rebase`, `tag`, `cherry-pick`, `worktree`, and config or hook edits. For those, put the exact command you would run in your final message and let the user run it.

A dirty tree, an unresolved conflict, or a surprising diff is reported, not repaired in git — say what you see and what you would run, then stop there.