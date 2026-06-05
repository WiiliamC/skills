---
name: develop_by_subagent
description: Explicit-only workflow for implementing an approved plan through a single subagent using focused test-driven development, followed by main-agent acceptance review. Use only when the user explicitly invokes $develop_by_subagent.
---

# Develop By Subagent

Use this skill only after the user explicitly invokes `$develop_by_subagent`, typically after a proposed implementation plan has been agreed.

## Workflow

1. Extract the current implementation plan into a concise task brief.
   - Include the goal, acceptance criteria, expected edit scope, and verification commands.
   - Include only the minimum file paths, APIs, and constraints the subagent needs.
   - Do not pass the full conversation or broad repo context.

2. Start exactly one subagent for implementation.
   - Instruct it to use test-driven development: write or update the smallest meaningful failing test first, implement the change, then run focused verification.
   - Tell it not to add redundant tests. Tests should cover changed behavior, regressions, or risky edge cases only.
   - Tell it not to spawn additional subagents or delegate the task further.
   - Tell it to edit files directly in its workspace and report changed paths plus commands run.

3. While the subagent works, do not duplicate its implementation.
   - You may inspect non-overlapping context needed for acceptance review.
   - Avoid changing the same files unless the subagent result requires integration or repair.

4. When the subagent finishes, perform acceptance review yourself.
   - Inspect the changed files and verify they match the plan.
   - Check that tests are focused and not redundant.
   - Run the appropriate focused tests or repo scripts when practical.
   - Fix only necessary integration issues, then rerun relevant verification.

5. Report the outcome.
   - Summarize implementation changes, tests/commands run, and any remaining risk.
   - Mention if any planned verification could not be run.

## Subagent Prompt Template

Use a brief like this, adapted to the current plan:

```text
Implement the approved plan using test-driven development.

Task:
<short goal and acceptance criteria>

Relevant context:
<minimal file paths, APIs, constraints, and commands>

Requirements:
- Write or update the smallest meaningful failing test first.
- Do not add redundant tests; cover only changed behavior, regressions, or risky edge cases.
- Do not spawn subagents or delegate further.
- Edit files directly in your workspace.
- Run focused verification where practical.
- Final response must list changed paths and commands run.
```
