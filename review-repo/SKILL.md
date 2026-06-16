---
name: review-repo
description: Multi-agent repository review workflow. Use when Codex is asked to review an entire code repository or a user-specified directory for architecture/design issues, likely bugs, unit test health and coverage gaps, redundant tests, code duplication, overly complex logic, shotgun surgery, performance risks, inefficient algorithms, or prioritized code review findings. This skill splits large repositories by submodule, coordinates specialized subagents for normal scopes, then deduplicates and ranks their findings.
---

# Review Repo

## Overview

Run a whole-repository or directory-scoped review. The main agent first estimates the scoped codebase size and organization. For normal-sized scopes, launch the five specialist reviewers directly. For large scopes, split by major submodule and launch one coordinator subagent per submodule; each coordinator runs `review-repo` from that submodule directory and returns its local findings. In both cases, the main agent collects all findings, deduplicates them, and produces one priority-ordered review list.

Default scope is the current repository root. If the user names one or more paths, restrict every subagent to those paths while still allowing them to read nearby docs, tests, and call sites needed to understand the scoped code.

## Workflow

1. Confirm the review scope from the user request. Do not ask for confirmation unless the scope is ambiguous and a wrong scope would waste substantial time.
2. Do a quick local scan first: read repo instructions, list top-level files, identify test commands, note language/framework boundaries, and estimate size using fast local signals such as tracked file count, source file count, and top-level directory layout.
3. Decide the execution branch:
   - **Large scope**: if the scope has many independent top-level packages/apps/services, multiple language boundaries, or enough files that five reviewers would likely sample only one module, use the divide-and-conquer branch.
   - **Normal scope**: if the scope is compact enough for the five reviewers to cover meaningfully, use the direct specialist branch.
4. For the divide-and-conquer branch:
   - Identify major submodules from repo structure, workspace/package config, service/app directories, ownership boundaries, or build/test config. Prefer reviewable units such as `apps/*`, `packages/*`, `services/*`, `libs/*`, or language-specific package roots. Exclude generated, vendor, build, cache, and dependency directories.
   - Spawn one coordinator subagent per selected submodule in parallel. Each coordinator must work from that submodule directory, use `review-repo` for that submodule, and return already prioritized local findings plus test commands/results.
   - Keep the module list practical. If there are too many small modules, group related modules by product area, language, or shared test command.
5. For the direct specialist branch, spawn the five specialist subagents below in parallel. Use `explorer` for read-only review roles. Use `worker` only if the user explicitly asks for fixes, because this skill is primarily a review workflow.
6. While agents run, inspect high-signal files locally only when needed to understand repo shape, verify a likely cross-cutting concern, or evaluate conflicts between returned findings.
7. Wait for all subagents, then normalize their results into findings with evidence.
8. Deduplicate overlapping issues by root cause, not by file path. Merge supporting evidence from multiple agents or modules into the strongest single finding.
9. Prioritize findings and provide the final review in Chinese unless the user explicitly asks for another language. Preserve code symbols, file paths, commands, and exact error text as written.

## Subagents

Start each subagent with the shared scope, repository path, and any repo-specific instructions already visible in the conversation. Tell each subagent to return only actionable findings, with file/line references where possible, and to say clearly if it found no issues.

### Large-scope module coordinator

Purpose: own a submodule review when the repository is too large for direct whole-repo specialist review.

Prompt shape:

```text
You are the module review coordinator for a large repository review.
Repository root: <repo root>.
Module scope: <submodule path>.

Change into the module directory and use the review-repo skill to review this module. Keep the review focused on this module, but read nearby shared docs, tests, package/workspace config, and call sites when needed to understand contracts and integration points.

Return only actionable findings, already deduplicated inside this module. For each finding include:
- priority suggestion: P0/P1/P2/P3
- title
- evidence with file:line references
- why it matters
- suggested direction, without writing patches

Also return exact test commands run, pass/fail results, environment blockers, and any cross-module concerns that the main agent should reconcile with other module reports. If no issues are found, say so and mention residual risk.
```

Use the following specialist reviewers only for the normal-scope branch, or inside a module coordinator's own `review-repo` run.

### 架构分析师

Purpose: inspect architecture, module boundaries, class design, coupling, cohesion, design principle violations, and code smells.

Prompt shape:

```text
You are the architecture analyst for a repository review.
Scope: <repo root or user paths>.

Review the scoped code for architecture/design defects, class responsibility problems, boundary violations, hidden side effects, brittle condition chains, feature envy, long methods/classes, duplicated abstractions, and shotgun-surgery risks.

Return findings only when they are actionable and supported by evidence. For each finding include:
- priority suggestion: P0/P1/P2/P3
- title
- evidence with file:line references
- why it matters
- suggested direction, without writing patches
If no issues are found, say so and mention residual risk.
```

### bug digger

Purpose: read documentation first, then compare implementation behavior against documented behavior and likely runtime expectations.

Prompt shape:

```text
You are the bug digger for a repository review.
Scope: <repo root or user paths>.

First read relevant documentation such as README files, adjacent docs, comments describing contracts, configuration, and usage examples. Then inspect implementation and tests for mismatches, edge cases, data validation gaps, error handling problems, resource leaks, concurrency/state bugs, path handling bugs, and compatibility issues.

Return only plausible bugs with concrete evidence. For each finding include:
- priority suggestion: P0/P1/P2/P3
- title
- documented or expected behavior
- actual code behavior with file:line references
- reproduction idea or failing scenario
- suggested direction, without writing patches
If no issues are found, say so and mention what docs/code areas were checked.
```

### 测试工程师

Purpose: run the canonical unit test command and review test quality.

Prompt shape:

```text
You are the test engineer for a repository review.
Scope: <repo root or user paths>.

Identify canonical test commands from repo instructions and scripts. Run full unit tests unless the user explicitly limited runtime or the environment blocks execution. Also inspect tests related to the scope for missing important coverage, weak assertions, flaky patterns, over-specified tests, redundant duplicated tests, and fixtures that obscure behavior.

Return:
- exact commands run and pass/fail result
- any environment blockers
- actionable test findings with priority suggestion P0/P1/P2/P3, file:line references, why it matters, and suggested direction
If tests pass and no test-quality issues are found, say so and mention residual risk.
```

### code simplifier

Purpose: look for simpler code shapes and consolidation opportunities without promoting broad rewrites.

Prompt shape:

```text
You are the code simplifier for a repository review.
Scope: <repo root or user paths>.

Review the scoped code for unnecessary complexity, duplicated logic, repeated code, excessive branching, redundant abstractions, scattered changes that should be centralized, and names or APIs that force callers to know implementation details.

Prefer small, local simplifications that reduce real maintenance cost. Do not recommend cosmetic churn or broad rewrites. For each finding include:
- priority suggestion: P0/P1/P2/P3
- title
- evidence with file:line references
- simpler direction
- why this is worth changing
If no issues are found, say so and mention residual risk.
```

### 效率优化工程师

Purpose: inspect performance risks and speed-critical implementation choices.

Prompt shape:

```text
You are the performance optimization engineer for a repository review.
Scope: <repo root or user paths>.

Review the scoped code for inefficient algorithms, accidental quadratic or worse behavior, repeated expensive I/O, unnecessary serialization/deserialization, excessive memory copies, avoidable allocations, slow loops in hot paths, missed batching/vectorization/caching opportunities, inefficient database/network/API usage, concurrency bottlenecks, and performance regressions hidden behind abstractions.

Pursue code speed aggressively, but keep findings evidence-based. Do not recommend speculative micro-optimizations unless the code is plausibly hot or the cost is clearly high. For each finding include:
- priority suggestion: P0/P1/P2/P3
- title
- evidence with file:line references
- suspected complexity or cost
- faster direction
- benchmark or profiling idea when practical
If no issues are found, say so and mention residual risk.
```

## Priority Rules

Use these priorities in the final list:

- `P0`: confirmed critical correctness, data loss, security, or release-blocking test failure.
- `P1`: likely user-visible bug, broken documented behavior, serious maintainability risk in active/shared code, or full test suite failure.
- `P2`: meaningful design/test/simplification issue that can cause future defects or recurring maintenance cost.
- `P3`: low-risk cleanup, local clarity issue, minor redundant test, or improvement with limited blast radius.

When subagents disagree, assign the higher priority only if the evidence supports real impact. Downgrade speculative findings or convert them to questions.

## Final Review Format

Lead with findings, ordered by priority. Keep each finding concise and evidence-based:

```text
- [P1] Title
  Evidence: path/to/file.py:123 ...
  Problem: ...
  Recommendation: ...
```

After findings, include:

- `测试结果`: commands run and outcomes, especially full UT status.
- `去重说明`: brief note for major merged duplicates if useful.
- `开放问题`: only questions that materially affect assessment.

If there are no findings, state that clearly, then report test results and remaining review limits.
