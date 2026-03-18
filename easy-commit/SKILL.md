---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*)
description: Git commit helper with subcommands for different commit strategies
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff -- HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Usage

Choose a subcommand based on your commit needs:

### `single` - Single Commit (Default)
Combine all related changes into one commit.

```bash
/easy-commit single
```

Use when:
- Changes are logically related
- The change is small and self-contained

### `multiple` - Multiple Commits by Module
Create separate commits for different functional modules.

```bash
/easy-commit multiple
```

Use when:
- Working on different functional modules independently
- Each commit should have a clear, focused purpose

### `combine` - Combined Feature Commit
Combine two related features into one commit.

```bash
/easy-commit combine
```

Use when:
- Features are interdependent
- They share common changes (e.g., API + tests)

## Workflow

1. Check git status and diff
2. Choose the appropriate subcommand
3. Stage files with `git add`
4. Create commit(s) with concise messages
5. **MANDATORY: Remove Co-Authored-By** - After generating the commit message, check if it contains `Co-Authored-By`, `Co-authored-by`, or any similar footer. If found, **remove it completely** before committing.
6. Verify with `git status`

## ⚠️ Important: No Co-Authored-By - Zero Tolerance Policy

**NEVER** include any Co-Authored-By, Co-authored-by, or similar footer in commit messages.

**Rule is absolute - no exceptions:**
- Don't include it even once
- Don't "forget" to remove it
- Don't assume it was already removed
- Don't keep it "just this once"
- **Remove it or start over**

### How to Check

After generating a commit message, search for these patterns:
- `Co-Authored-By`
- `Co-authored-by`
- `Co-authored-by:`

If any pattern is found, **delete the entire footer line** before committing.

### Commit Message Format

Follow the project's convention (see CLAUDE.md):
- First line under 50 characters
- Prefixes: `feat:`, `fix:`, `chore:`, `refactor:`, etc.
- Example: `feat: add skip_confirm option to skip config confirmation`

## Red Flags - STOP and Fix

If you notice any of these, **STOP and remove the Co-Authored-By footer**:

| Excuse | Why It's Wrong |
|--------|----------------|
| "I'll remember to remove it later" | You won't. Remove it now. |
| "It's just a footer" | The whole message must be clean. |
| "Claude added it automatically" | That's not an excuse - check and remove. |
| "I forgot this time" | There is no "this time" - rule is absolute. |
| "It's already in the message" | Delete it and start over. |

**Violating the letter of the rules is violating the spirit of the rules.**
