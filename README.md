# Awesome Skills - GitHub Copilot Agents

A collection of specialized GitHub Copilot custom agents for orchestrating the complete software development lifecycle, from requirements gathering through implementation, testing, and review.

## Installation

Install via pip:

```bash
pip install swe-copilot-agents
```

Or install from source:

```bash
git clone https://github.com/khaerulumam42/swe-copilot-agents.git
cd swe-copilot-agents
pip install -e .
```

### Install Agents to Your Project

After installing the package, navigate to your project directory and run:

```bash
cd /path/to/your/project
swe-copilot-agents
```

This will copy the agents to `.github/agents/` in your current directory:

```bash
✓ brainstormer.agent.md
✓ knowledge-graph-agent.agent.md
✓ plan-executor.agent.md
✓ plan-reviewer.agent.md
✓ pytest-agent.agent.md
✓ readme-generator.agent.md
✓ rug-orchestrator.agent.md

✅ Installed 7 agent(s) to /path/to/your/project/.github/agents
```

## Overview

This repository contains AI agents that follow the **"coordinator and worker" pattern**—where specialist agents perform focused work under the guidance of an orchestrator. Each agent has a strong persona, clear boundaries, and specific expertise.

---

## Agents

### @rug-orchestrator

**Role:** Pure delegation orchestrator following the RUG pattern (Repeat Until Good) — NEVER implements, only delegates

**Persona:**
- **Philosophy:** "Repeat Until Good" — every task validated, failed tasks retried
- **Traits:** Pure delegator, context-preserving, validation-obsessed
- **Constraint:** Only uses `agent`, `read`, `search` tools — NEVER `edit` or `execute`

**Responsibilities:**
- Delegates ALL implementation work to specialist subagents (preserves context window)
- Decomposes plans into granular tasks (one file = one subagent task)
- Validates EVERY task via separate @plan-reviewer (mandatory, not optional)
- Retries failed tasks with improved instructions (up to 3 times, then escalates)
- Supports parallel execution for independent tasks

**Orchestrated Agents:**
- @brainstormer (Phase 1 - Planning, if no plan exists)
- @plan-executor (Phase 3 - Implementation per decomposed task)
- @plan-reviewer (Phase 4 - Mandatory validation for every task)
- @pytest-agent (Phase 6 - Testing, optional)

**RUG Loop:** Implement → Validate → If FAIL, retry (up to 3x) → If still FAIL, escalate to human

**Best Practices:** ✅ **EXCELLENT**
- Distinctive RUG pattern with pure-delegation approach
- Task decomposition rules prevent monolithic delegation
- Mandatory per-task validation ensures quality
- Common failure modes table teaches anti-patterns
- Parallel execution pattern for efficiency
- Result routing table clarifies all state transitions

---

### @brainstormer

**Role:** Curious planning agent who asks clarifying questions to crystallize requirements

**Persona:**
- **Philosophy:** Uncertainty triggers questions, not assumptions
- **Traits:** Insatiably curious, thorough, multi-round questioner (1-10 rounds)
- **Metaphor:** Exploratory researcher who never assumes

**Responsibilities:**
- Asks 1-10 rounds of clarifying questions before writing plans
- Queries knowledge graph for impact analysis (downstream, cycles, bottlenecks, test seams)
- Creates detailed markdown plan documents in `docs/plan/YYYY-MM-DD-*.md`
- Integrates knowledge graph findings into every plan
- **Decision Helper mode:** Presents 2-4 options with pros/cons, comparison table, and one clear recommendation with reasoning
- **Handoff support:** Offers direct handoff to @plan-executor or orchestrated execution via @rug-orchestrator

**Best Practices:** ✅ **EXCELLENT**
- Strong persona ("insatiably curious")
- Knowledge graph integration for impact analysis
- Multi-round questioning framework with defined stages
- Decision Helper mode with structured options, comparison tables, and recommendations
- Clear completion criteria (user confirmation before writing plan)
- Comprehensive plan output template with KG analysis sections
- Handoff support to @plan-executor or @rug-orchestrator

---

### @plan-executor

**Role:** Senior Python engineer who executes plans by blending seamlessly with existing codebases

**Persona:**
- **Philosophy:** "Consistency > Clean Code"
- **Traits:** Chameleon-like, adaptive, pattern-matching
- **Metaphor:** Code chameleon who becomes indistinguishable from existing code

**Responsibilities:**
- Reads 3-5 existing files to understand patterns before writing
- Matches existing style exactly (naming, imports, error handling, formatting)
- Implements requirements from plan documents
- Uses `todo` tool to track plan item progress
- Never "fixes" existing code because it's ugly

**Best Practices:** ✅ **EXCELLENT**
- Strong persona with clear philosophy ("Consistency > Clean Code")
- Concrete code examples showing good vs. bad matching
- Specific matching table (naming, imports, errors, strings, formatting)
- Clear boundaries (never "revamp" existing code)
- Executable commands for studying patterns
- `todo` tool integration for plan item tracking
- Handoff support to @plan-reviewer

---

### @plan-reviewer

**Role:** Senior code reviewer and quality assurance engineer who rigorously audits implementation against plans

**Persona:**
- **Philosophy:** "Evidence over assumptions"
- **Traits:** Ruthlessly thorough, evidence-driven, uncompromising
- **Metaphor:** Auditor who proves everything through code inspection

**Responsibilities:**
- Extracts all requirements from plan documents
- Searches codebase for concrete evidence of each requirement
- Categorizes execution status (Fully/Partially/Not Executed)
- Performs brittleness analysis via knowledge graph (high centrality, excessive dependencies, deep chains)
- Provides prioritized remediation recommendations

**Best Practices:** ✅ **EXCELLENT**
- Strong persona ("ruthlessly thorough")
- Clear execution status definitions with evidence gathering checklist
- Knowledge graph brittleness analysis with risk levels
- Comprehensive report output format
- Priority assignment criteria (P0-P3)
- Status determination rules with specific conditions

---

### @pytest-agent

**Role:** Senior Python QA engineer specializing in pytest with expert-level mocking and patching

**Persona:**
- **Philosophy:** "Depth over breadth"
- **Traits:** Exhaustive, comprehensive, edge-case obsessed
- **Metaphor:** Test surgeon who operates at every code path

**Responsibilities:**
- Writes exhaustive test suites (happy path, edge cases, errors, state, integration)
- Expert-level mocking and patching (Mock, MagicMock, patch, PropertyMock)
- Targets >80% coverage for new code
- Tests only newly implemented code (respects scope boundaries)

**Best Practices:** ✅ **EXCELLENT**
- Strong persona ("depth over breadth")
- Comprehensive test coverage requirements table
- Expert mocking examples with all patterns
- Clarification protocol for ambiguous behavior
- Clear scope boundaries (only test new code)
- Code style examples (good vs. bad)

---

### @knowledge-graph-agent

**Role:** Expert code analysis specialist who builds knowledge-base graphs from codebases

**Persona:**
- **Philosophy:** Static analysis reveals code architecture
- **Traits:** Multi-lingual, systematic, incremental
- **Metaphor:** Code cartographer who maps relationships

**Responsibilities:**
- Scans codebases and generates `knowledge-graph.yaml` in project root
- Tracks relationships: files, functions, classes, imports, call chains, concerns
- Supports incremental updates (only changed files)
- Version tracking via git commit hashes
- Multi-language support (Python, JS/TS, Go, Java, Rust)

**Best Practices:** ✅ **EXCELLENT**
- Clear startup behavior with git hash comparison
- Incremental update mode to avoid full rescans
- Comprehensive YAML output format specification
- Complete analysis standards with good/bad examples
- Web framework pattern recognition (Flask, FastAPI, Express, Gin)
- Validation checklist before completion

---

### @readme-generator

**Role:** Technical writer who transforms code knowledge into clear, accurate README documentation

**Persona:**
- **Philosophy:** "Data-driven documentation"
- **Traits:** Meticulous, factual, preservation-focused
- **Metaphor:** Documentarian who only writes what the code proves

**Responsibilities:**
- Auto-generates README.md from knowledge-graph.yaml data
- Updates existing READMEs by syncing KG-derived sections (marked with `<!-- KG:SECTION -->` comments)
- Preserves all manual content when updating
- Extracts tech stack, file structure, entry points, and dependencies from KG

**Best Practices:** ✅ **EXCELLENT**
- Dual-mode behavior (generate new vs. update existing)
- KG section markers for safe updates
- Clear section mapping table
- Knowledge graph handoff when KG is missing
- Data extraction examples from KG to README

---

## Best Practices Summary

| Agent | Persona | Boundaries | Commands | Examples | Workflow Diagram | Overall |
|-------|---------|------------|----------|----------|------------------|---------|
| @rug-orchestrator | ✅ Strong | ✅ RUG | ✅ Complete | ✅ Decomposition | ✅ ASCII Flow | **EXCELLENT** |
| @brainstormer | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Plan format | ✅ Decision Helper | **EXCELLENT** |
| @plan-executor | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Code style | ❌ None | **EXCELLENT** |
| @plan-reviewer | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Report format | ❌ None | **EXCELLENT** |
| @pytest-agent | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Test style | ❌ None | **EXCELLENT** |
| @knowledge-graph-agent | ✅ Strong | ✅ Clear | ✅ Complete | ✅ YAML format | ❌ None | **EXCELLENT** |
| @readme-generator | ✅ Strong | ✅ Clear | ✅ Complete | ✅ KG mapping | ✅ Dual-mode | **EXCELLENT** |

**Overall Repository Quality:** ✅ **EXCELLENT** - All 7 agents follow GitHub Copilot custom agent best practices with strong personas, clear boundaries, executable commands, and token-optimized instructions.

---

## Workflow Orchestration

### Complete Development Cycle (RUG Pattern)

```
User Request
      ↓
┌─────────────────────────────────────────────────────────────────┐
│                    @rug-orchestrator (Pure Delegator)            │
└─────────────────────────────────────────────────────────────────┘
      │
      ├─ Phase 1: @brainstormer → Plan document
      │     (clarifying questions → plan in docs/plan/)
      │     ↓ Human Approval
      │
      ├─ Phase 2: @plan-executor → Implementation (per task)
      │     (one file = one subagent task)
      │
      ├─ Phase 3: @plan-reviewer → Mandatory validation
      │     ↓ PASS or FAIL?
      │     ├─ FAIL → Retry @plan-executor (up to 3×)
      │     │           └─ Still FAIL → Escalate to Human
      │     └─ PASS → Continue
      │
      └─ Phase 4: @pytest-agent → Tests (Optional)
            ↓
         Done
```

### RUG Loop Logic

1. Each task delegated to @plan-executor individually (preserves context window)
2. @plan-reviewer validates **every** task — never skipped
3. Failed tasks retried up to 3× with improved instructions
4. After 3 failures, escalate to human with full context

---

## Usage

### Basic Agent Invocation

```bash
# In VS Code with GitHub Copilot Chat — start with the orchestrator
@rug-orchestrator
I want to add a user authentication system with JWT tokens

# Or invoke a specific agent directly
@brainstormer
I need to add a search feature to my application

@plan-reviewer
Review the implementation against docs/plan/2025-03-02-auth.md
```

### File Locations

- **Agents:** `agents/*.agent.md`
- **Plans:** `docs/plan/YYYY-MM-DD-*.md`
- **Knowledge Graph:** `knowledge-graph.yaml` (project root)

---

## Agent File Structure

All agents follow this structure:

```yaml
---
name: agent-name
description: Brief description of purpose
tools: ["tool1", "tool2"]
agents: ["agent1", "agent2"]  # For orchestrators only
target: vscode | github-copilot
---

# Persona description
## Core Philosophy
## Your Role
## [Specific sections per agent]
## Boundaries (Always Do / Ask First / Never Do)
## Commands
```

---

## Contributing

When adding new agents:

1. **Follow the persona pattern** - Give each agent a distinctive personality
2. **Define clear boundaries** - What they always do, ask first, never do
3. **Include executable commands** - Concrete bash commands they can run
4. **Provide examples** - Good vs. bad outputs
5. **Add visual workflow** - ASCII diagrams for complex agents
6. **Document best practices** - Mark if agent follows Copilot best practices

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Inspiration

Based on patterns from:
- [GitHub Custom Agents Documentation](https://docs.github.com/en/copilot/customizing-custom-agents)
- [awesome-copilot community collection](https://github.com/github/awesome-copilot)
- Subagent orchestration patterns in VS Code
