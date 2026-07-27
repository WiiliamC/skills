---
name: quick-commit
description: Quickly commit all current Git working-tree changes by deriving a concise commit message from the diff and committing immediately. Use when the user asks to quick commit, 快速提交, 直接提交当前改动, or explicitly wants a commit without separately invoking tests, lint, builds, code review, or correctness checks.
---

# Quick Commit

Commit the repository's current changes with minimal ceremony. Treat invocation of this skill as authorization to stage and commit all current changes.

## Workflow

1. Confirm the current directory belongs to a Git worktree with `git rev-parse --show-toplevel`.
2. Inspect only the information needed to understand and summarize the changes:
   - `git status --short`
   - `git diff --stat`
   - `git diff --cached --stat`
   - `git diff`
   - `git diff --cached`
   - untracked file contents only when needed to describe them
   - a short recent subject history such as `git log -5 --pretty=%s`
3. Do not review the changes for correctness. Do not separately invoke tests, UT, lint, type checks, builds, formatters, validation commands, or `git diff --check`. Allow any Git hooks triggered by the commit to run normally.
4. If `git status --short` shows no changes, stop and report that there is nothing to commit.
5. Generate one concise commit subject that reflects all current changes and follows the language and style of recent commit subjects when practical. Prefer the user's explicit commit-message instructions when provided.
6. Stage and commit in exactly one shell command:

   ```bash
   git add -A && git commit -m "<subject>"
   ```

   Do not run `git add` as a separate command. Safely quote the generated subject. Never add `--no-verify`; allow all configured Git hooks to execute. Do not ask for confirmation.
7. Report the resulting short commit hash and subject.

## Boundaries

- Do not modify source files.
- Do not omit selected current changes unless the user explicitly limits the scope.
- Do not amend an existing commit unless explicitly requested.
- Do not push the commit.
- Do not bypass Git hooks.
- Do not claim that the committed code is correct or tested.
- If staging or committing fails, report the exact failure and resulting repository state. Do not undo a successful staging step when the commit step fails.
