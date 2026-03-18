---
name: huge_step
description: Use when facing large-scale development tasks requiring systematic exploration of multiple modules, architecture design, and detailed implementation planning
---

## Context

This skill is designed for **large-scale development tasks** that span across multiple modules with significant code changes. These tasks have the following characteristics:
- Span across multiple modules with significant code changes
- Involve complex module dependencies
- Require systematic exploration, design, parallel analysis, and rigorous acceptance

This skill is **project-agnostic**, providing a universal methodology for large-scale development. It borrows from the distributed README pattern (each module has its own README) commonly found in well-structured projects.

## Core Principles

1. **Explore First** - Understand architecture before designing implementation
2. **Parallel Analysis** - Analyze module changes concurrently using agent teams
3. **TDD-Driven** - Follow test-driven development methodology
4. **Clear Acceptance** - Define acceptance criteria before implementation begins
5. **Team Collaboration** - Use structured agent teams for parallel work distribution

## The huge_step Workflow

### Phase 1: Architecture Exploration (Agent Team Dispatch)

**Goal**: Understand the project structure and module dependencies before designing

**Steps**:
1. **Create an agent team** using `TeamCreate` tool with a descriptive team name (e.g., "huge_step-[feature-name]")
2. **Launch multiple Explore agents IN PARALLEL** using the team's task list:
   - One agent per major top-level directory
   - Each agent reads the module's README first (if exists)
   - Each agent maps module dependencies and key components
3. **Synthesize findings** into a unified architecture overview
4. **Identify affected modules** and add them to the task list for Phase 5

**Agent Prompt Pattern** (project-agnostic):
```
Explore the [MODULE_NAME] directory to understand:
1. What this module does (read README first)
2. Key components and their responsibilities
3. Dependencies on other modules
4. Testing patterns used
5. Entry points and public APIs

Return a structured summary of findings and mark your task as completed.
```

**Team Management**:
- Use `SendMessage` to coordinate with teammates
- Check `TaskList` to track progress of all explore agents
- Use `TaskUpdate` to assign new tasks as discoveries are made

**Output**: Architecture diagram + module dependency map + affected modules list

---

### Phase 2: Requirements & Scope Analysis

**Goal**: Refine understanding of what needs to be changed

**Steps**:
1. Review the user's requirements
2. Map requirements to identified modules
3. Create initial task breakdown
4. Identify potential risks and unknowns

**Output**:
- Requirements-to-modules mapping
- Risk assessment
- Unknowns that need clarification

---

### Phase 3: Architecture Design

**Goal**: Design the implementation approach

**Steps**:
1. Propose architecture changes (data flow, component interactions)
2. Show before/after architecture diagrams
3. Identify new components needed
4. Define interfaces between modified modules

**Output**:
- Detailed architecture design
- Component interaction diagrams (mermaid)
- New/modified components list

---

### Phase 4: TDD Test Strategy

**Goal**: Define comprehensive testing approach

**Steps**:
1. Identify all test files that need modification
2. Identify new tests needed for new functionality
3. Define acceptance criteria with specific verification commands
4. Create test coverage plan

**Output**:
- Test files to modify (with line numbers if possible)
- New test files to create
- Acceptance criteria with verification commands

---

### Phase 5: Parallel Module Impact Analysis (Agent Team Execution)

**Goal**: Analyze each affected module in parallel using the agent team

**Steps**:
1. **Create tasks** in the team's task list for each affected module using `TaskCreate`
2. **Dispatch agents** to analyze modules in parallel using `Agent` tool with `team_name` and `name` parameters
3. **Each agent** performs detailed analysis:
   - Files to create
   - Files to modify
   - Breaking changes
   - Test modifications needed
4. **Collect reports** from agents via `SendMessage` or check `TaskList` for completion
5. **Consolidate findings** into a comprehensive module-by-module change plan

**Agent Prompt Pattern** (project-agnostic):
```
Based on the architecture design, analyze [MODULE_PATH] for:
1. Files that need to be created (with purpose)
2. Files that need modification (specific functions/classes)
3. Potential breaking changes
4. Test files that need updates
5. Dependencies that need to be updated

Return a structured analysis report and mark your task as completed.
```

**Team Management**:
- Use descriptive agent names (e.g., "data-collect-analyst", "models-analyst")
- Use `SendMessage` to coordinate between teammates
- Check `TaskList` to track progress and find unblocked tasks
- Use `TaskUpdate` to assign tasks and set dependencies

**Output**: Per-module change plan with specific file operations

---

### Phase 6: Final Plan Compilation

**Goal**: Create a comprehensive, executable implementation plan

**Steps**:
1. **Combine all phase outputs** from the agent team reports
2. **Organize tasks** in dependency order using `TaskUpdate` with `addBlockedBy`
3. **Add TDD cycle guidance** for each task
4. **Include verification steps** for acceptance criteria

**Team Cleanup**:
- Use `TeamDelete` to clean up team resources when work is complete
- This removes the team directory and task list

**Plan Document Header** (follow writing-plans skill format):
```markdown
# [Feature Name] Implementation Plan

> **For Claude:** Created by huge_step skill using agent team collaboration.
> Use `subagent-driven-development` skill to implement with parallel execution.

**Goal:** [One-sentence summary]

**Architecture:** [2-3 sentences describing approach]

**Tech Stack:** [Key technologies]

**Acceptance Criteria:** [Testable criteria with verification commands]

---
```

**Output Format**:
```
# [Feature Name] Implementation Plan

## Overview
- Goal
- Architecture
- Tech Stack
- Acceptance Criteria

## Phase 1: Architecture Exploration Summary
[Findings from parallel explore agents]

## Phase 2: Architecture Design
[Before/after diagrams, component changes]

## Phase 3: TDD Test Strategy
[Test files, coverage plan, acceptance commands]

## Phase 4: Module-by-Module Changes
[Per-module: files to create, modify, tests]

## Phase 5: Implementation Tasks
[Ordered tasks with TDD cycles]

## Verification
[How to verify acceptance criteria]
```

---

## Integration with Existing Skills

| Skill | Role in huge_step workflow |
|-------|---------------------------|
| **superpowers:writing-plans** | huge_step OUTPUT follows this format |
| **superpowers:test-driven-development** | huge_step incorporates TDD cycles |
| **superpowers:subagent-driven-development** | huge_step uses agent teams for parallel analysis and implementation |
| **superpowers:verification-before-completion** | huge_step includes verification steps |
| **superpowers:dispatching-parallel-agents** | huge_step uses this for Phase 1 and Phase 5 parallel work |
| **superpowers:using-git-worktrees** | huge_step RECOMMENDS worktree setup for isolation |

## Agent Team Workflow

The huge_step skill uses a structured agent team approach for parallel development:

```
1. TeamCreate(team_name="huge_step-[feature]")
   └─ Creates team and task list

2. Phase 1: Parallel Exploration
   ├─ Agent "data-collect-analyst" → Explore [data-collect/]
   ├─ Agent "models-analyst" → Explore [models/]
   └─ Agent "calibration-analyst" → Explore [calibration/]

3. Phase 5: Parallel Module Analysis
   ├─ Agent "data-collect-impl" → Analyze [data-collect/]
   ├─ Agent "models-impl" → Analyze [models/]
   └─ Agent "calibration-impl" → Analyze [calibration/]

4. TeamDelete()
   └─ Clean up team resources
```

**Team Management Tools**:
- `TeamCreate` - Create a new team with shared task list
- `TaskCreate` - Add tasks to the team's task list
- `TaskList` - View all tasks and their status
- `TaskUpdate` - Assign tasks, set dependencies, update status
- `SendMessage` - Communicate with teammates
- `TeamDelete` - Clean up team resources when done

---

## Key Differentiators

| Aspect | Existing Skills | huge_step |
|--------|----------------|-----------|
| Scope | Single feature/bug fix | Large-scale, multi-module |
| Approach | Sequential execution | Parallel exploration first |
| Architecture | Implied or minimal | Explicit diagrams required |
| Testing | Per-file focus | Full test strategy |
| Acceptance | Implicit | Explicit criteria FIRST |
| Output | Code/changes | DETAILED IMPLEMENTATION PLAN |

---

## What huge_step DOES NOT Do

1. **Does NOT execute the plan** - Only outputs the plan document
2. **Does NOT modify files** - All file operations in the plan are for the implementer
3. **Does NOT use project-specific paths** - All examples are generic (e.g., `[module-name]/`)
4. **Does NOT make implementation decisions** - Decisions are presented for user approval

---

## Complete Agent Team Workflow Example

```
User: "I need to refactor the data collection system to support new sensor types"

huge_step:
"I'm using the huge_step skill to plan this large-scale refactoring.

[Team Creation]
TeamCreate(team_name="huge_step-data-refactor", description="Refactor data collection for new sensor support")

[Phase 1: Architecture Exploration - Parallel Agent Dispatch]
TaskCreate(subject="Explore data-collect module", description="Analyze data-collect directory structure and dependencies")
TaskCreate(subject="Explore models module", description="Analyze models directory structure and dependencies")
TaskCreate(subject="Explore calibration module", description="Analyze calibration directory structure and dependencies")

Agent(team_name="huge_step-data-refactor", name="data-collect-analyst", ...)
  → Explores [dataset/collect/], reads README, maps dependencies

Agent(team_name="huge_step-data-refactor", name="models-analyst", ...)
  → Explores [model/], reads README, maps dependencies

Agent(team_name="huge_step-data-refactor", name="calibration-analyst", ...)
  → Explores [calibration/], reads README, maps dependencies

TaskList → Check all exploration tasks completed
SendMessage(to="*", message="All exploration agents completed. Synthesizing findings...")

[Phase 2: Requirements Mapping]
- New sensor support requires...
- Affected modules: dataset/collect, model, calibration

[Phase 3: Architecture Design]
[Before/After diagrams]

[Phase 4: TDD Test Strategy]
- Test files to modify...
- Acceptance: Run `scripts/test.sh` and verify...

[Phase 5: Parallel Module Impact Analysis]
TaskCreate(subject="Analyze data-collect changes", ...)
TaskCreate(subject="Analyze models changes", ...)
TaskCreate(subject="Analyze calibration changes", ...)

Agent(team_name="huge_step-data-refactor", name="data-collect-impl", ...)
  → Analyzes files to create/modify for data-collect

Agent(team_name="huge_step-data-refactor", name="models-impl", ...)
  → Analyzes files to create/modify for models

Agent(team_name="huge_step-data-refactor", name="calibration-impl", ...)
  → Analyzes files to create/modify for calibration

[Phase 6: Final Plan Compilation]
- Combine all reports
- Organize tasks in dependency order
- Add TDD cycle guidance

TeamDelete()  # Clean up team resources

[Final Plan Output]
Plan saved to docs/plans/2026-03-18-refactor-data-collect.md

Ready to implement? Use subagent-driven-development skill to execute the plan."
```

