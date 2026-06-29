---
name: fix-bug-root
description: Root-cause bug analysis workflow for the diagnostic phase. Use when Codex is explicitly asked to analyze why a defect occurs, find its root cause, investigate or reproduce a bug, diagnose failure modes, or separate symptoms from design-level causes. Do not use for code-change execution after a remedy has already been selected unless the user also asks for root-cause analysis.
---

# Fix Bug Root

## Principle

Treat patch-style bug fixes as a design smell. Identify the system defect that allowed the bug to exist, not only the input, line, branch, or test that exposed it.

Prefer a small design-correct remedy over a smaller local workaround. The right remediation direction should improve the model, ownership, contract, invariant, lifecycle, or boundary that was wrong.

## Workflow

1. Define the bug precisely.
   - State the observed behavior, expected behavior, reproduction path, and affected surface.
   - If reproduction is not possible, identify the strongest available evidence and the remaining uncertainty.
   - Do not edit code before the failure mode is concrete enough to explain.

2. Separate symptom, proximate cause, and root cause.
   - Symptom: the visible error, failing test, user-visible breakage, or bad output.
   - Proximate cause: the immediate code path or state transition that triggers the symptom.
   - Root cause: the incorrect design assumption, misplaced responsibility, broken invariant, ambiguous ownership, leaky boundary, duplicated state, lifecycle mismatch, or contract violation that made the proximate cause possible.

3. Inspect the design before choosing the remediation direction.
   - Read the owning abstraction, adjacent callers, tests, interfaces, and documentation.
   - Identify which class, module, or layer should own the behavior.
   - Check whether similar logic is duplicated elsewhere and whether the same defect can appear through other paths.
   - Prefer centralizing the invariant at the source of truth over adding guards at consumers.

4. Reject workaround directions unless explicitly temporary.
   - Do not add one-off conditionals for a single failing case when the abstraction is wrong.
   - Do not swallow exceptions, silently default values, add sleeps, add blind retries, or alter tests to match broken behavior.
   - Do not scatter null checks or defensive guards across callers when the producer contract should be fixed.
   - Do not mock away the failure in tests unless the mock represents a real contract boundary.

5. Design the root remediation direction.
   - Recommend the smallest change that restores the correct responsibility, invariant, lifecycle, or contract.
   - Keep the direction global enough that all equivalent paths become correct.
   - Preserve public APIs unless changing the API is the root-correct solution; if so, update all affected callers and tests deliberately.
   - Remove obsolete workaround code when the new design makes it unnecessary.

6. Define how to prove the remedy.
   - Identify the regression test that should fail for the original defect and pass for the root remedy.
   - Include adjacent scenarios that prove the repaired invariant or contract, not only the reported input.
   - Run focused verification first, then broader tests when the changed abstraction is shared.

## Root-Cause Checklist

Before recommending or finalizing a bug remedy, be able to answer:

- What invariant, contract, ownership rule, or lifecycle assumption was broken?
- Why did the existing design allow the bad state or behavior to exist?
- Which abstraction should prevent this class of bug?
- Does the remedy address every equivalent path, or only the reported path?
- Did the tests prove the repaired behavior at the right level?
- Did the change remove or avoid patch logic rather than adding more?

## Reporting

When reporting the outcome, include:

- Root cause: the design-level defect, with file and behavior evidence.
- Remediation direction: why the chosen change belongs at the right owner level.
- Anti-patch rationale: why local guards or special cases were not used, or why any temporary guard is explicitly constrained.
- Verification: tests or commands run, plus any residual risk.
