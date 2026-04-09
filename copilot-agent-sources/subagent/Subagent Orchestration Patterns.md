# Subagent Orchestration Patterns

## Overview

Subagent orchestration is a pattern where a manager/orchestrator agent delegates work to specialized worker subagents. This preserves the orchestrator's context window and enables parallel execution of independent tasks.

## Key Benefits

1. **Context Preservation**: Orchestrator maintains a "fresh mind" by not polluting its context with implementation details
2. **Parallel Execution**: Multiple subagents can work simultaneously on independent tasks
3. **Specialization**: Each subagent has domain-specific expertise
4. **Validation Loop**: Separate validation subagents verify work quality
5. **Retry Logic**: Failed work can be retried with fresh context and improved instructions

---

## Primary Orchestrator Patterns

### 1. RUG (Repeat Until Good)

**Philosophy**: Pure orchestration - NEVER does implementation work

**Core Principle**: Every piece of actual work MUST be delegated to a subagent

**Allowed Tools Only**:
- `runSubagent` — to delegate work
- `manage_todo_list` — to track progress

**Available Subagents**: SWE (Senior Software Engineer), QA

---

### 2. GEM Orchestrator

**Philosophy**: Phased workflow with specialized agents for each phase

**Phases**: Discuss → Research → Planning → Execution → Summary

**Available Subagents**: gem-researcher, gem-planner, gem-implementer, gem-browser-tester, gem-devops, gem-reviewer, gem-debugger, gem-critic, gem-designer, gem-documentation-writer, gem-code-simplifier

---

## Delegation Mechanisms

### RUG Delegation Protocol

#### 1. Task Decomposition

```
RULES OF THUMB:
- One file = one subagent
- One logical concern = one subagent
- Research vs. implementation = separate subagents
- Never ask a single subagent to do more than ~3 closely related things
```

#### 2. Subagent Prompt Template

```
CONTEXT: The user asked: "[original request]"

YOUR TASK: [specific decomposed task]

SCOPE:
- Files to modify: [list]
- Files to create: [list]
- Files to NOT touch: [list]

REQUIREMENTS:
- [requirement 1]
- [requirement 2]
- ...

ACCEPTANCE CRITERIA:
- [ ] [criterion 1]
- [ ] [criterion 2]
- ...

SPECIFIED TECHNOLOGIES (non-negotiable):
- The user specified: [technology/library/framework/language if any]
- You MUST use exactly these. Do NOT substitute alternatives.

CONSTRAINTS:
- Do NOT [constraint 1]
- Do NOT [constraint 2]

WHEN DONE: Report back with:
1. List of all files created/modified
2. Summary of changes made
3. Any issues or concerns encountered
4. Confirmation that each acceptance criterion is met
```

#### 3. Validation Subagent Prompt Template

```
A previous agent was asked to: [task description]

The acceptance criteria were:
- [criterion 1]
- [criterion 2]
- ...

VALIDATE the work by:
1. Reading the files that were supposedly modified/created
2. Checking that each acceptance criterion is actually met
3. SPECIFICATION COMPLIANCE CHECK: Verify the implementation uses the technologies the user specified
4. Looking for bugs, missing edge cases, or incomplete implementations
5. Running any relevant tests or type checks
6. Checking for regressions in related code

REPORT:
- SPECIFICATION COMPLIANCE: List each specified technology → confirm used, or FAIL
- For each acceptance criterion: PASS or FAIL with evidence
- List any bugs or issues found
- Overall verdict: PASS or FAIL
```

---

### GEM Orchestrator Delegation Protocol

#### 1. Phase-Based Delegation

| Phase | Subagent | Purpose |
|-------|----------|---------|
| Research | gem-researcher | Domain research and information gathering |
| Planning | gem-planner | Create implementation plans with task breakdown |
| Verification | gem-reviewer | PRD compliance, security, quality checks |
| Critique | gem-critic | Challenge assumptions, find edge cases |
| Implementation | gem-implementer | Write code and implement features |
| Mobile Implementation | gem-implementer-mobile | Mobile-specific implementation |
| Browser Testing | gem-browser-tester | End-to-end browser testing |
| DevOps | gem-devops | Infrastructure and deployment |
| Debugging | gem-debugger | Root cause analysis and diagnosis |
| Design | gem-designer | UI/UX validation for web |
| Mobile Design | gem-designer-mobile | UI/UX validation for mobile |
| Documentation | gem-documentation-writer | Generate documentation |
| Code Simplification | gem-code-simplifier | Refactor and simplify code |

#### 2. Delegation Payload Structure

```jsonc
{
  "gem-researcher": {
    "plan_id": "string",
    "objective": "string",
    "focus_area": "string (optional)",
    "complexity": "simple|medium|complex",
    "task_clarifications": "array of {question, answer}"
  },

  "gem-planner": {
    "plan_id": "string",
    "variant": "a | b | c (for multi-plan)",
    "objective": "string",
    "complexity": "simple|medium|complex",
    "task_clarifications": "array of {question, answer}"
  },

  "gem-implementer": {
    "task_id": "string",
    "plan_id": "string",
    "plan_path": "string",
    "task_definition": "object"
  },

  "gem-reviewer": {
    "review_scope": "plan | task | wave",
    "task_id": "string",
    "plan_id": "string",
    "wave_tasks": "array of task_ids",
    "review_depth": "full|standard|lightweight",
    "review_security_sensitive": "boolean"
  },

  "gem-debugger": {
    "task_id": "string",
    "error_context": {
      "error_message": "string",
      "stack_trace": "string (optional)",
      "failing_test": "string (optional)",
      "reproduction_steps": "array (optional)"
    }
  }
}
```

#### 3. Result Routing

| Result Status | Agent Type | Extra Check | Next Action |
|:--------------|:-----------|:------------|:------------|
| completed | gem-reviewer (plan) | - | Present plan to user |
| completed | gem-reviewer (wave) | - | Continue to next wave |
| needs_revision | gem-reviewer | - | Re-delegate with findings |
| completed | gem-critic | verdict=pass | Aggregate findings |
| completed | gem-critic | verdict=blocking | Route to gem-planner for fixes |
| completed | gem-debugger | - | IF code: gem-implementer, IF config: original agent |
| needs_approval | gem-devops | - | Present to user for approval |

---

## Common Failure Modes

### RUG Anti-Patterns

1. **"Let me just quickly..." syndrome** — Reading a file yourself instead of delegating
2. **Monolithic delegation** — One giant subagent task that hits context limits
3. **Trusting self-reported completion** — Not validating with separate subagent
4. **Giving up after one failure** — Not retrying with better instructions
5. **Doing orchestration logic yourself** — Writing "glue code" instead of delegating

### GEM Orchestrator Anti-Patterns

1. **Executing tasks instead of delegating** — Doing implementation work
2. **Skipping workflow phases** — Jumping straight to execution
3. **Missing status updates** — Not reporting progress
4. **Routing without phase detection** — Not determining correct phase first

---

## Retry and Error Handling

### RUG Retry Loop

```
1. Work subagent completes
2. Validation subagent verifies
3. IF validation FAILS:
   a. Launch NEW work subagent with:
      - Original task prompt
      - Validation failure report
      - Specific fix instructions
   b. Re-validate
4. Repeat until good (max iterations not specified, but "RUG" implies persistence)
```

### GEM Retry Logic

```
1. Subagent returns status=failed or needs_revision
2. Delegate to gem-debugger for diagnosis
3. Validate confidence: IF < 0.7, escalate to user
4. Inject diagnosis into retry task_definition
5. IF code fix → gem-implementer
6. IF infra/config → original agent
7. After fix → re-delegate to original agent to re-verify
8. Max 3 retries per wave
```

---

## Comparison: RUG vs GEM

| Aspect | RUG | GEM |
|--------|-----|-----|
| **Philosophy** | Pure delegation manager | Phased workflow orchestrator |
| **Does Implementation?** | NEVER | NEVER |
| **Subagents** | 2 (SWE, QA) | 12+ specialized agents |
| **Workflow** | Decompose → Delegate → Validate → Repeat | Discuss → Research → Plan → Execute → Summary |
| **Validation** | Separate validation subagent for every task | gem-reviewer for waves, gem-critic for approach |
| **Best For** | When you want zero implementation, heavy validation | Complex projects requiring research and planning |
| **Task Granularity** | Very fine-grained (1 file = 1 subagent) | Wave-based with multiple tasks per wave |

---

## Implementation Guidelines

### When to Use Orchestrator Pattern

- **Large tasks** that would exceed a single context window
- **Multi-domain work** requiring different expertise
- **High reliability requirements** needing validation loops
- **Parallelizable work** with independent components

### When NOT to Use

- **Simple tasks** that can be done in one shot
- **Tightly coupled work** where subtasks have heavy dependencies
- **Real-time requirements** where subagent overhead is unacceptable

---

## Related Files

- `source/awesome-copilot/agents/rug-orchestrator.agent.md` — RUG orchestrator definition
- `source/awesome-copilot/agents/gem-orchestrator.agent.md` — GEM orchestrator definition
- `source/awesome-copilot/agents/swe-subagent.agent.md` — SWE subagent definition
- `source/awesome-copilot/agents/qa-subagent.agent.md` — QA subagent definition
