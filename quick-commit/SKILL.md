---
name: quick-commit
description: Quickly commit current-task changes, falling back to all changes when the task scope cannot be determined, then derive a concise message and commit directly. Use for quick commit, 快速提交, 直接提交当前改动, or an explicit commit request without additional review, tests, lint, or builds.
---

# Quick Commit

The current agent reads the candidate, writes the message, stages, and commits directly with Git. Do not invoke a helper script, Codex CLI session, or subagent. Read [the commit-message prompt](references/commit-message.md) before generating the message.

## Determine the commit scope

Invocation authorizes committing the requested scope without another conversational confirmation. **Prefer changes from the current task; if that scope cannot be determined, commit all changes in the target repository.** Determine scope from the user's latest request and the relevant conversation, then identify the actual files and hunks in the diff before staging.

- “快速提交”, “提交本次改动”, or an unqualified commit request: use the task description, edits made during the task, and actual diffs to identify this task's changes. When that scope is identifiable, preserve unrelated changes even when already staged or in the same file. When it cannot be determined, include all tracked changes and non-ignored new files, including pre-existing changes, without asking for scope confirmation.
- Explicit files, directories, functionality, or exclusions: follow those boundaries. A topic or task restriction may require selecting individual hunks within a file. Include necessary related changes only when they belong to the requested task and do not violate explicit exclusions.
- “只提交已暂存改动”: commit only the existing index content; do not stage additional worktree content or new files.
- “提交全部改动”: include all tracked changes and non-ignored new files in the target repository, including pre-existing changes, subject to any explicit exclusions.

An explicit scope takes precedence over the default and its all-changes fallback. When called by review-and-commit, use its explicitly reviewed submission scope without widening it. Briefly state the selected scope before committing, including when the all-changes fallback applies. If the task scope is known and this task has no remaining changes, report that even when unrelated changes exist.

## Inspect and prepare

Resolve the absolute repository path and read applicable repository instructions. Inspect HEAD, branch, staged and unstaged diffs, and non-ignored new files to separate the requested changes from unrelated ones. Read the complete selected candidate, including selected new-file contents; use metadata for binaries. Respect repository privacy and Git LFS requirements. Missing or unreadable candidate content blocks committing; do not silently truncate the input used for the message.

Do not review correctness or separately run tests, lint, type checks, builds, formatters, or `git diff --check`. Do not edit source files. Required repository checks or missing LFS setup that cannot be satisfied within these boundaries must be reported rather than bypassed. Normal author/committer attribution is not a secret when repository rules permit it.

If there are no candidate changes, report nothing to commit. An unresolved merge/rebase/cherry-pick, conflicted index, or unexpected concurrent Git operation requires resolving the situation before using this quick workflow; do not abort, reset, or complete it implicitly.

## Stage and commit

Generate a concise message using the linked prompt and the complete selected candidate, excluding unrelated changes from the message. Existing commit rules override recent subject style. Prepare only the authorized candidate, then inspect the actual commit diff and selected new-file contents to confirm they match what was read and authorized. Compare actual content, not only filenames or status flags; no custom fingerprint or persistent snapshot protocol is required. If contents changed, inspect the new candidate and update the message before proceeding.

Choose Git operations that preserve both unrelated staged and unstaged changes:

- Use repository-wide `git add -A` only when the requested scope includes all current changes. For a staged-only request, use the existing index without staging or using `--only`, which would take worktree contents instead.
- When the selected scope includes whole files, stage only those paths. If unrelated paths are already staged, a path-scoped commit such as `git commit --only -- <selected paths>` can preserve them; inspect its actual worktree candidate first.
- When a selected file also contains unrelated hunks, do not stage or commit the whole file or use `--only` for that file. Prepare only the selected hunks, using an isolated temporary index if necessary to preserve unrelated real-index entries. After committing through a temporary index, reconcile only the committed hunks in the real index against the new HEAD, preserving unrelated entries and hunks; do not replace the whole real index. Verify that the commit excludes unrelated hunks and that their staged/unstaged state remains intact. Never reset or overwrite the user's index or worktree to simplify selection.

Do not run a blanket staged commit when the index contains changes outside the requested scope. If safe separation cannot be established, explain the specific ambiguity or limitation and ask for the missing scope decision rather than silently broadening the commit.

When called after review-and-commit, any content change beyond the reviewed candidate returns control to its review loop before committing; updating the message alone is insufficient.

Run Git through the environment's normal execution-permission mechanism. Skill invocation authorizes the action but does not bypass sandbox approval; do not unconditionally require escalation in environments where Git writes are already permitted. Use a structured message argument or a temporary message file for multiline text, avoiding shell interpolation of diff-derived text.

Execute the commit with normal hooks and signing. Do not use `--no-verify`, disable signing, amend, push, or automatically add hook-generated changes for retry. On failure inspect HEAD, index, and worktree before deciding what happened. Preserve the resulting state and report the failed step; do not claim the original index was restored. If a commit was created, report it rather than blindly retrying. If hooks changed content, inspect it before another attempt; a review-and-commit caller must re-review affected content.

## Report

Verify the resulting commit and repository state. Report its short hash and subject, and any remaining changes or hook-induced differences from the intended candidate. Do not claim correctness, review, or tests that this skill did not perform. If committed content differs from the candidate passed by review-and-commit, report that its review conclusion does not cover those differences and return control to that workflow for remediation; do not automatically amend or rewrite the commit.
