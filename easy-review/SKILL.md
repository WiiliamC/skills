---
description: Code review with subcommands for staged or all changes
---

## Usage

Choose a subcommand based on the scope of changes you want to review:

### `staged` - Review Staged Changes Only

Review only the code changes that have been staged (added to git index):

```bash
/easy-review staged
```

Use when:
- You want to review changes before committing
- You have multiple changes and want to review them one by one
- You want to verify staged changes pass tests before committing

### `all` - Review All Changes

Review all uncommitted changes (both staged and unstaged):

```bash
/easy-review all
```

Use when:
- You want a complete review of all uncommitted changes
- You're ready to submit all changes for review
- You haven't staged changes yet and want to review everything at once

## How It Works

### Git Root Detection
Before running any git commands, the skill must:
1. Run `git rev-parse --show-toplevel` to find the current git repository root
2. All git commands must be run from this directory (respects git worktrees)

### For `staged` mode:
1. Uses `git diff --cached` to get staged changes only
2. Runs related tests on staged changes
3. Reports issues found in staged changes

### For `all` mode:
1. Uses `git diff HEAD` to get all uncommitted changes
2. Runs related tests on all changes
3. Reports issues found in all changes

## Phase 1: Pre-checks (3 steps)

1. **Check for changes** - Use an agent to check if there are changes in the selected scope. If there are no changes, report this and stop.
   - Use `git rev-parse --show-toplevel` to find git root
   - Use `git diff --cached` for staged mode or `git diff HEAD` for all mode

2. **Get CLAUDE.md context** - Use an agent to retrieve file paths to all relevant CLAUDE.md files from the codebase.
   - **CRITICAL**: CLAUDE.md files must be read from the worktree root (returned by `git rev-parse --show-toplevel`), NOT from the parent repository root
   - Search for CLAUDE.md files starting from the worktree root directory

3. **Get diff summary** - Use an agent to get the diff of selected changes, and request a structured summary:
   - List of modified files
   - For each file: additions, deletions, and lines changed
   - Brief description of the change purpose

## Phase 2: Expert Agents (5 parallel agents)

4. Launch 5 parallel agents, each with a focused scope:

   **a. Code Style Expert**
   - Audit changes against CLAUDE.md requirements
   - Check: import order, f-strings usage, function length (max 80 lines), naming conventions
   - Return issues in format: `{file, line_range, problem, reason, fix_suggestion}`

   **b. Bug Locator**
   - Do a shallow scan for obvious bugs (null dereference, type mismatch, logic errors)
   - Focus on large/obvious bugs first
   - Return issues in format: `{file, line_range, problem, reason, fix_suggestion}`

   **c. Performance Analyst**
   - Check for performance pitfalls (N+1 queries, inefficient loops, memory leaks)
   - Identify optimization opportunities
   - Return issues in format: `{file, line_range, problem, reason, fix_suggestion}`

   **d. Architect**
   - Analyze architectural impact of changes
   - Discover all README.md files in the project (excluding worktree directories)
   - Check each README to determine if it needs updating based on the changes
   - Look for outdated documentation that no longer matches the code structure
   - Identify module boundary changes that should be documented
   - Return issues in format: `{file, problem, reason, fix_suggestion}`

   **e. Gatekeeper**
   - Identify test files related to changed files
   - Run relevant unit tests using: `/home/chan/miniconda3/envs/capyglan_py11/bin/python -m pytest <related_tests> -v`
   - Run modified shell scripts if any
   - **CRITICAL - Filter unrelated failures**: Only report and recommend fixes for test failures that are directly related to the changed code
   - **How to determine relevance**:
     - If test file is a direct match for a changed file (e.g., `detector.py` changed → `test_detector.py` fails), include it
     - If test file covers a module that the changed code directly uses/depends on, include it
     - If test file is unrelated to the changed code (pre-existing flaky test, unrelated module), IGNORE the failure
   - When a test fails but is unrelated, list it separately as "Ignored" in the report
   - Return: `{test_result, failed_tests[], error_output, recommended_fix}`

## Phase 3: Confidence Scoring

5. For each issue found in Phase 2 (excluding gatekeeper failures), launch parallel agents to calculate confidence scores (0-100):
   - 0: Not confident (likely a false positive)
   - 25: Somewhat confident
   - 50: Moderately confident
   - 75: Highly confident
   - 100: Absolutely certain

## Phase 4: Aggregation and Reporting

6. **Filter issues** - Keep only issues with confidence score >= 80

7. **Aggregate by category** - Group issues as:
   - Code Style Issues (sorted by priority)
   - Bug Issues (sorted by priority)
   - Performance Issues (sorted by priority)
   - Documentation Issues (architect findings)
   - Test/Script Failures (gatekeeper findings)

   **Filter unrelated test failures**: Only include test failures where the failure is caused by the changed code. If a test file fails but none of the modified files are related to that test, exclude it from the report.

8. **Deduplicate** - Merge duplicate issues found by multiple experts

9. **Generate fix plans** - For each issue, include:
   - The specific problem with file:line reference
   - Recommended fix approach
   - Files and lines to change

10. **Create issue report and fix plan** - Output review in this format:

```
---

### Code Review Summary

Found N high-confidence issues across 5 categories:

#### 1. Code Style Issues (M/X)
- Issue 1: [Brief description]
- Issue 2: [Brief description]

#### 2. Bug Issues (M/Y)
- Issue 1: [Brief description]
- Issue 2: [Brief description]

#### 3. Performance Issues (M/Z)
- Issue 1: [Brief description]

#### 4. Documentation Issues (Architect)
- Issue 1: [Brief description - which README needs update]
- Issue 2: [Brief description - what should be updated]

#### 5. Test/Script Failures (N failures)
- test_file.py: failure description
- script.sh: failure description

---

### Detailed Fix Plans

#### Code Style Fixes

1. **Problem**: [Description]
   - **Files**: file.py#L10-L15
   - **Fix**: [Specific fix approach]
   - **Confidence**: 85-100

2. ...

#### Bug Fixes

...

#### Documentation Fixes

1. **Problem**: [Description - which README needs update]
   - **Files**: README.md#L10-L15
   - **Fix**: [Specific documentation update approach]
   - **Architect Finding**: [Architect-specific observation]

2. ...

---

### Execution Plan

This review has generated a plan to fix the identified issues.

**Do you want to execute these fixes automatically?**

- If yes, I will apply all fix plans using the Edit tool.
- If no, I will leave the changes as-is.

**Note**: This report is created in plan mode. Use `/exit-plan-mode accept` to confirm and proceed with fixes.

---

### Related Test Failures (Ignored)

The following test failures were detected but are unrelated to the current changes. They have been ignored:

- test_file.py: reason for ignoring
- another_test.py: reason for ignoring

**Note**: Only test failures directly related to the changed code are included in the fix plans.
---
```

11. **Call ExitPlanMode** - After generating the report, call ExitPlanMode to transition from planning to execution mode, allowing the user to review the plan before any files are modified.

12. **Apply fixes** - Only after user confirmation, use the Edit tool to apply all fix plans.

13. **Verify fixes** - After applying fixes, run relevant tests to verify the changes work correctly.

---

## Notes

### Plan Mode Workflow

This skill operates in **plan mode** by default:

1. **Phase 1-3**: Analysis and issue detection
2. **Phase 4 (step 10)**: Generate issue report and fix plan
3. **Phase 4 (step 11)**: Call `ExitPlanMode` to show the plan to user
4. **User confirmation**: User reviews the plan and decides whether to execute
5. **Fix execution**: Only after confirmation, apply changes

### Git Worktree Support

This skill properly supports git worktrees:

1. **Git root detection**: Always run `git rev-parse --show-toplevel` first to find the correct git repository root
2. **Worktree-aware**: The command automatically detects the worktree root, not the parent repository
3. **All git commands**: Run all `git diff`, `git log`, and other git commands from the directory returned by `--show-toplevel`

**Why this matters**: In a git worktree, `git rev-parse --show-toplevel` returns the worktree directory (e.g., `/path/to/project/.git/worktrees/feature`) rather than the main repository root, ensuring all operations target the correct changes.

### Reading Project Files (CLAUDE.md, README.md, etc.)

**CRITICAL**: When reading project documentation files:

1. **Always use the worktree root** - The path returned by `git rev-parse --show-toplevel` is the correct base directory
2. **Never assume the parent repository root** - The worktree may be in a completely different location (e.g., `~/.git/worktrees/feature` vs `~/project`)
3. **Verify file paths** - All file paths should be relative to the worktree root, not the parent repository

**Common mistake**: Assuming `~/develop/capyglan_headware` is the project root when it's actually the parent repository. The worktree root is `~/develop/capyglan_headware/.git/worktrees/enhance_cleaner_log`.

### General Guidelines

- Use `git diff --cached` for staged mode to get only staged changes
- Use `git diff HEAD` for all mode to get all uncommitted changes
- Generate specific, actionable fix plans that can be executed with the Edit tool
- When linking to code, use format: `file.py#L10-L15` with file path and line numbers
- Gatekeeper should run **only related tests**, not the full test suite
- Test selection strategy:
  - If changed file has a matching test file (e.g., `detector.py` → `test_detector.py`), run that
  - If changed file is in `dataset/`, run tests in `test_dataset/*/` that match modified modules
  - If changed file is in `model/`, run tests in `test_model/*/` that match modified modules
  - For shell scripts, run the script directly with bash

### Test Failure Relevance

**Related failures** (include in report):
- Test file directly corresponds to a changed file
- Test covers a function/module that the changed code directly calls or depends on
- Test failure stack trace points to lines in the changed code

**Unrelated failures** (ignore, list in "Ignored" section):
- Test file is in a different module area
- Test failure is a pre-existing flaky test (e.g., timing-dependent, race conditions)
- Test was already failing before the changes (check git history if unsure)
- Test covers unrelated functionality that just happens to be in the same test file

### Documentation Update Guidelines

**The Architect should:**
1. Discover all README.md files in the project (excluding worktree directories)
2. For each README found, evaluate whether the changes affect:
   - Architecture overview or high-level design
   - Module structure or module responsibilities
   - Getting started or installation instructions
   - Usage examples or API documentation
   - Configuration options or environment variables
3. Report which README files need updates and what sections should be changed
