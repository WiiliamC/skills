---
name: resolve-merge-conflicts
description: Intent-aware merge conflict analysis and resolution planning. Use only when the user explicitly invokes $resolve-merge-conflicts or explicitly asks to use the resolve-merge-conflicts skill for conflicted files, branches, patches, rebases, cherry-picks, or merge conflict markers. Do not use implicitly for ordinary conflict fixing requests.
---

# Resolve Merge Conflicts

## Overview

Produce a conflict resolution plan after understanding both sides' development intent. Do not directly edit files, stage changes, continue a rebase, or mark conflicts resolved unless the user separately asks for implementation after reviewing the plan.

The goal is not to pick one side or mechanically combine conflict blocks. The goal is to preserve the compatible intent from both sides, detect places where one side unknowingly violates the other side's new names, contracts, conventions, invariants, or architecture, and stop for user decision when the intents genuinely conflict.

## Hard Boundaries

- Stay read-only. Do not modify files, run formatters that write, use `git add`, `git commit`, `git merge --continue`, `git rebase --continue`, or similar state-changing commands.
- If user asks to "resolve" while invoking this skill, interpret that as "analyze and provide a resolution plan" unless they explicitly ask for implementation after the plan.
- If either side's intent is ambiguous and the ambiguity materially affects the plan, state the uncertainty instead of guessing.
- If the two sides contain conflicting product, API, schema, security, data migration, or architectural decisions, stop and report the decision needed from the user.

## Workflow

1. Establish conflict scope.
   - Identify conflicted files with `git status --short`, `git diff --name-only --diff-filter=U`, or the user's supplied files.
   - Read conflict blocks, but also read surrounding code, nearby tests, docs, and call sites needed to understand behavior.
   - Identify the merge base and both sides when available. Use read-only commands such as `git diff`, `git show`, `git log`, and `git merge-base`.

2. Reconstruct each side's development intent.
   - For side A and side B, summarize what changed and why: feature addition, bug fix, refactor, rename, API contract change, convention change, test expectation, migration, dependency update, or behavior change.
   - Use commit messages, branch names, PR notes visible in the repo, tests, docs, and adjacent code as evidence.
   - Distinguish explicit intent from inference. Mark inference as inference.

3. Cross-check for missed intent.
   - Check whether one side added code that should have followed the other side's new names, types, interfaces, validation rules, style conventions, ownership boundaries, feature flags, migrations, or test patterns.
   - Look beyond the immediate conflict hunk. Search for renamed symbols, moved modules, updated schemas, changed constants, new helper APIs, and revised tests.
   - Treat "B added code using an old API that A renamed or constrained" as a planning issue even when Git only reports a small textual conflict.

4. Classify relationships between intents.
   - Compatible: both intents can be preserved with a combined resolution.
   - Compatible with adaptation: one side's content should be rewritten to obey the other side's newer contract or convention.
   - Redundant: both sides implement the same goal differently; choose the implementation direction only if evidence clearly favors it.
   - Conflicting: both sides make incompatible decisions. Stop and ask the user to choose.

5. Build a resolution plan.
   - Explain the intended final behavior, not just text edits.
   - List file-by-file changes needed to preserve both compatible intents.
   - Include tests or checks that should prove the merge preserves behavior.
   - Call out any follow-up migrations, docs, or callers that must be updated.

## Evidence Checklist

Before writing the final plan, check:

- What did each side intend to accomplish?
- Did either side introduce a rename, module move, new abstraction, contract, invariant, or convention that the other side's additions must follow?
- Are tests from either side now obsolete, duplicated, or missing assertions for the combined behavior?
- Are docs, configs, generated files, migrations, lockfiles, or public API surfaces involved?
- Would a naive resolution compile but violate one side's intended model?
- Is any decision product- or architecture-level rather than implementation-level?

## Stop Conditions

Stop and ask the user for a decision when:

- The sides encode incompatible user-visible behavior, API shape, schema meaning, security posture, or data migration direction.
- Keeping both intents would create duplicate ownership, two sources of truth, or incompatible lifecycle rules.
- Evidence is insufficient to determine whether a rename/refactor should supersede the other side's added code.
- The correct resolution depends on business, product, release, or compatibility priorities not present in the repo.

When stopped, do not provide a pseudo-resolution. Provide the smallest concrete decision request with options and evidence.

## Final Output

Return the analysis in this shape:

```text
Conflict scope:
- <files and conflict groups>

Side A intent:
- <intent, evidence>

Side B intent:
- <intent, evidence>

Cross-intent checks:
- <missed rename/contract/convention/test/API/migration issues>

Decision needed:
- <only if stop condition applies; include options and consequences>

Resolution plan:
- <ordered, file-by-file plan; no patches unless the user separately asks>

Verification plan:
- <tests, builds, static checks, or manual checks>
```

If there is a stop condition, omit the resolution plan or limit it to the parts that are independent of the user's decision.
