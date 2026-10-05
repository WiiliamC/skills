---
name: quick-commit
description: Quickly commit all current Git working-tree changes by deriving a concise commit message from the diff and committing immediately. Use when the user asks to quick commit, 快速提交, 直接提交当前改动, or explicitly wants a commit without separately invoking tests, lint, builds, code review, or correctness checks.
---

# Quick Commit

Use [scripts/commit_by_codex.sh](scripts/commit_by_codex.sh) to commit all tracked changes and non-ignored new files, including existing working-tree changes. Invocation authorizes staging and committing this complete scope. If the user permits only specific files, stop to align the scope: the tool does not support a file whitelist.

## Workflow

Resolve the target repository from the user's path or current working directory with `git rev-parse --show-toplevel`, then pass its absolute path to the script:

```bash
bash /path/to/quick-commit/scripts/commit_by_codex.sh --repo /path/to/repository -y
```

Replace `/path/to/quick-commit` with this SKILL.md's directory. Run through `exec_command` with `sandbox_permissions: "require_escalated"` and a justification explaining that Git metadata writes and committing require escalation. Do not first attempt the commit in the sandbox. Skill invocation authorizes the commit but does not bypass execution permissions; `-y` avoids a second conversational confirmation.

The script owns candidate snapshotting, commit-message generation, consistency checks, staging and committing. Do not duplicate its diff inspection or generate a separate message in the calling agent. Its read-only Codex session uses `gpt-6-luna` by default; pass `--model MODEL` only when requested. Repository commit and privacy rules take precedence over recent subject style.

Do not review correctness or separately run tests, lint, type checks, builds, formatters, or `git diff --check`. Git hooks and signing run normally. Do not modify source files, amend, push, bypass hooks, or claim the code is correct or tested.

Report the resulting short hash and subject. If the script reports no changes, report that there is nothing to commit. On failure, report the failed step and inspect repository state when needed. A failed commit preserves the original staging area; a failure after Git creates the commit must be reported as a created commit with a synchronization failure, rather than retried automatically.

## Shared implementation

Dependencies: Bash, Git, Python 3, Codex CLI, and the repository's existing hooks/signing environment. This skill has no dependency on review skills.

- `commit_by_codex.sh` constructs the complete candidate in a temporary index, supplies its diff and recent subjects to read-only Codex, verifies repository consistency, commits, and synchronizes the real index.
- `worktree_fingerprint.sh` provides the shared content identity used by review checkpoints and the optional `--reviewed-snapshot VERSION:HASH` commit guard.

`review-and-commit` depends on these scripts and supplies the reviewed snapshot after review passes. Both skills use this single commit implementation; quick commits do not require a review snapshot.
