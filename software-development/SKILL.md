---
name: software-development
description: Apply shared software development constraints when implementing features, fixing bugs, refactoring, changing tests or configuration, or maintaining code-related documentation. Complements project instructions and specialized workflows; does not turn read-only questions or reviews into implementation tasks.
---

# Software Development

Apply this baseline within the user's requested scope. Project instructions supply
concrete architecture, commands, environments, and contracts. Preserve explicit
user choices and applicable authorization, review, and acceptance requirements.
Use specialized workflows when applicable without replacing them with this skill.
This baseline does not itself require planning artifacts, delegation, a full test
suite, development logs, commits, or publication.

## Scope and decisions

- Own requirements interpretation, design, implementation, verification, and
  maintainability of the affected area. Make routine implementation decisions
  independently. Infer acceptance goals from usage scenarios and distinguish
  observed facts from assumptions.
- If an approach fails to address the underlying need, explain the evidence and
  recommend an alternative. Ask for a decision when unresolved choices change
  requirement semantics, public contracts, or significant costs; do not ask the
  user to design routine implementation details.
- Address structural problems necessary to complete the task correctly. Report
  unrelated maintenance issues with evidence and impact without expanding the
  assignment. A read-only request remains read-only.

## Repository fit and design

- Read the applicable repository and module instructions, then the nearest usage
  documentation and relevant implementation/tests. Prefer existing execution
  scripts, shared utilities, fixtures, and local conventions.
- Verify apparent documentation/code mismatches against actual behavior and the
  intended contract. Do not legitimize a defect merely because it exists in code.
  Preserve valid local patterns; fix stale guidance or make the smallest safe
  implementation change rather than mass-normalizing unrelated code.
- Keep responsibilities cohesive and public contracts explicit. Prefer a small
  local refactor when the change would otherwise introduce duplication, hidden
  side effects, brittle branching, or unnecessary caller knowledge. Avoid
  speculative abstractions. When changes must span modules, identify and verify
  the shared contract.
- Put reusable domain logic in the appropriate shared module, independent of
  specific applications, datasets, and experiment runners. Entry points parse
  and dispatch; configuration selects and composes. Shared services own common
  validation and lifecycle behavior across entry points.
- Avoid business I/O, environment mutation, and task startup during imports.
  Load optional heavy dependencies when their capabilities are selected; do not
  require unrelated resources for an otherwise independent operation. Respect
  intentional framework registration conventions.
- Keep read-only APIs free of implicit management writes or migrations. Route
  state-changing operations through the project's established validation,
  ownership, locking, and recovery boundaries where they exist.

## Verification

- Test stable behavior and contracts rather than incidental structure, release
  versions, or changing defaults. Use controlled inputs for override and
  propagation tests; assert exact production values only when they are contracts.
- Classify tests by the behavior exercised: isolated logic/contracts versus real
  component collaboration and end-to-end operations. File types, temporary
  directories, and GPU use alone do not determine classification. Follow the
  repository's test layout and keep shared helpers separate from test cases.
- Preserve shared fixture inputs unless their modification is part of the task.
  Write generated outputs to temporary or designated run directories.
- Run checks proportionate to the change and any required project checks. Add
  meaningful coverage for changed behavior where warranted, not tests that merely
  mirror implementation. Distinguish passing isolated tests, imports, smoke runs,
  and actual end-to-end verification.

## Documentation and history

- Keep lasting maintenance rules in the nearest applicable instruction file;
  current usage and contracts in module READMEs or linked design documents;
  historical implementation and experimental evidence in the appropriate records.
  Follow existing destinations rather than imposing a new documentation layout.
- Update affected navigation and usage when responsibilities, entry points, or
  structure change. Keep general rules at their shared scope instead of copying
  them into each submodule. Keep volatile defaults and performance figures out of
  stable architecture overviews.
- Preserve historical versions, provenance, conditions, metrics, and limitations.
  Record corrections with evidence and their effect on the original conclusion;
  explicitly mark unknown information. Do not substitute current defaults for
  historical facts or describe unavailable local artifacts as universally available.
- When removing a capability with reuse value, preserve a concise recovery trail
  in the project's established records: purpose, reason, replacement, verified
  source revision/paths, and dependencies or resources needed to restore it. Do
  not invent commit references or initiate a commit solely to create that trail.
  Ordinary duplicate-code cleanup does not require a removal report.
- Keep production code independent of explicitly temporary experimental code.
  Promote reusable capabilities into maintained modules when needed. Do not
  extend production maintenance to unrelated experiments or overwrite historical
  outputs; honor any project-specific compatibility commitments.

## Completion

Explain the resulting behavior, material design choices, verification actually
performed, and remaining uncertainty. Do not equate source availability or a
successful import with operational readiness, or test success with evidence for
an algorithmic or performance claim. Do not claim checks that were not run.
