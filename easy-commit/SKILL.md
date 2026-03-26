---
name: easy-commit
description: Fast single commit workflow - check diff, generate message, strip CoAuthor, commit
---

# Easy Commit

## Overview

Fast git commit workflow for when you want one commit with no questions asked. Runs in straight-line steps.

## When to Use

Use when:
- You want one commit for all current changes
- Changes are logically related
- You want fast, no-interaction workflow

Don't use when:
- You need multiple separate commits (use manual git workflow)
- Changes need to be split by module

## Quick Reference

```bash
/easy-commit
```

That's it - one command, does all steps automatically.

## Workflow (Straight-Line, No Questions)

**Step 1: Check Diff**
```bash
git status
git diff -- HEAD
```

**Step 2: Generate Commit Message**
- Summarize all changes
- Use conventional format: `feat:`, `fix:`, `chore:`, etc.
- First line under 50 characters

**Step 3: Review and Strip CoAuthor**
- Check message for: `Co-Authored-By`, `Co-authored-by`, `Co-authored-by:`
- If found, DELETE the footer line completely
- Message must be clean before committing

**Step 4: Commit**
```bash
git add . && git commit -m "$MESSAGE"
```

**Step 5: Verify**
```bash
git status
```

## Red Flags - STOP and Fix

| Issue | Fix |
|-------|-----|
| Co-Authored-By in message | Delete footer, regenerate if needed |
| Message over 50 chars | Shorten first line |
| Multiple unrelated changes | Use manual git workflow |

**Rule is absolute - no exceptions:**
- Don't commit with CoAuthor footer
- Don't "forget" to strip it
- **Clean message or start over**
