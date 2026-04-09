# Agent Generator - Documentation Index

## Overview

This folder contains documentation on subagent orchestration patterns and how to build orchestrator agents that delegate work to specialized subagents.

## Quick Reference

### What is Subagent Orchestration?

A pattern where a **manager/orchestrator agent** delegates work to specialized **worker subagents**. This preserves the orchestrator's context window and enables parallel execution.

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Context Preservation** | Orchestrator maintains "fresh mind" by not doing implementation |
| **Parallel Execution** | Multiple subagents work simultaneously on independent tasks |
| **Specialization** | Each subagent has domain-specific expertise |
| **Validation Loop** | Separate validation subagents verify work quality |
| **Retry Logic** | Failed work retried with fresh context and improved instructions |

---

## Documentation Files

### 0. [VS Code Setup Guide](./VS%20Code%20Setup%20Guide.md)

**How to set up and use orchestrator agents in VS Code**

Contents:
- Prerequisites (GitHub Copilot setup)
- Understanding agent file structure
- Setup options (existing plugins vs custom agents)
- Using agents in VS Code (3 methods)
- Project structure for custom agents
- VS Code settings
- Testing your orchestrator
- Troubleshooting
- MCP server integration

**Best for:** Getting started with agents in VS Code

---

### 1. [Subagent Orchestration Patterns](./Subagent%20Orchestration%20Patterns.md)

**Comprehensive overview of orchestration patterns**

Contents:
- Key benefits of orchestration
- RUG vs GEM orchestrator comparison
- Delegation mechanisms for both patterns
- Result routing tables
- Common failure modes
- Retry and error handling
- When to use/not use orchestrator pattern

**Best for:** Understanding the landscape and choosing the right pattern

---

### 2. [RUG - Deep Dive](./RUG%20-%20Deep%20Dive.md)

**Detailed documentation of the RUG orchestrator**

Contents:
- The Cardinal Rule (never do implementation yourself)
- Complete RUG protocol
- Task decomposition rules
- Subagent prompt templates
- Validation subagent prompts
- Anti-laziness measures
- Specification adherence
- All 7 common failure modes to avoid
- Termination criteria

**Best for:** Implementing a pure delegation orchestrator

---

### 3. [Implementing Orchestrator Agents](./Implementing%20Orchestrator%20Agents.md)

**Practical implementation guide with code examples**

Contents:
- Core tool: runSubagent syntax
- Pattern 1: Simple delegation
- Pattern 2: Parallel delegation
- Pattern 3: Sequential with dependencies
- Pattern 4: Retry loop (RUG style)
- Pattern 5: Wave-based execution (GEM style)
- Prompt building utilities
- Result routing pattern
- Todo list management
- Anti-patterns to avoid
- Implementation checklist

**Best for:** Writing actual orchestrator code

---

## Quick Comparison: RUG vs GEM

| Aspect | RUG | GEM |
|--------|-----|-----|
| **Philosophy** | Pure delegation manager | Phased workflow orchestrator |
| **Subagents** | 2 (SWE, QA) | 12+ specialized agents |
| **Workflow** | Decompose → Delegate → Validate → Repeat | Discuss → Research → Plan → Execute → Summary |
| **Validation** | Separate validation for EVERY task | gem-reviewer for waves, gem-critic for approach |
| **Best For** | Zero implementation, heavy validation | Complex projects needing research/planning |
| **Granularity** | Very fine (1 file = 1 subagent) | Wave-based with multiple tasks per wave |

---

## Core Concepts

### The Cardinal Rule (RUG)

> **NEVER do implementation work yourself.**

Every piece of actual work — writing code, editing files, running commands, reading files, searching codebases — MUST be delegated to a subagent.

### Why This Matters

Your context window is limited. Every token you spend doing work yourself makes you dumber and less capable of orchestrating. Subagents get fresh context windows — that's your superpower.

### Allowed Tools Only

- `runSubagent` — to delegate work
- `manage_todo_list` — to track progress

---

## Task Decomposition Rules

| Rule | Example |
|------|---------|
| One file = one subagent | Creating 5 files → 5 subagents |
| One logical concern = one subagent | "Add validation" separate from "add tests" |
| Research vs implementation = separate | First research, then implement |
| Never ~3+ things per subagent | Break down larger tasks |

---

## Essential Prompt Template

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

ACCEPTANCE CRITERIA:
- [ ] [criterion 1]
- [ ] [criterion 2]

SPECIFIED TECHNOLOGIES (non-negotiable):
- The user specified: [technology/library/framework]
- You MUST use exactly these. Do NOT substitute alternatives.

CONSTRAINTS:
- Do NOT [constraint 1]
- Do NOT [constraint 2]

WHEN DONE: Report back with:
1. List of all files created/modified
2. Summary of changes made
3. Any issues or concerns
4. Confirmation that each acceptance criterion is met
```

---

## Common Failure Modes

| Failure Mode | What Happens | Fix |
|--------------|--------------|-----|
| "Let me just quickly..." | You read a file yourself | Delegate to subagent |
| Monolithic delegation | One giant task hits context limits | Break into smaller pieces |
| Trusting self-reported completion | Subagent says "done" but isn't | Use separate validation subagent |
| Giving up after one failure | Validation fails, you escalate | Retry with better instructions |
| Doing orchestration logic yourself | You write "glue code" | Delegate to subagent |

---

## Source Files

The following source files contain the actual agent definitions:

- `source/awesome-copilot/agents/rug-orchestrator.agent.md` — RUG orchestrator
- `source/awesome-copilot/agents/gem-orchestrator.agent.md` — GEM orchestrator
- `source/awesome-copilot/agents/swe-subagent.agent.md` — SWE subagent
- `source/awesome-copilot/agents/qa-subagent.agent.md` — QA subagent

---

## Getting Started

1. **New to orchestration?** Start with [Subagent Orchestration Patterns](./Subagent%20Orchestration%20Patterns.md)
2. **Want to implement RUG?** Read [RUG - Deep Dive](./RUG%20-%20Deep%20Dive.md)
3. **Ready to code?** See [Implementing Orchestrator Agents](./Implementing%20Orchestrator%20Agents.md)

---

## Related Areas

- [Agent Generator.md](../Agent%20Generator.md) — Original task list and ideas
