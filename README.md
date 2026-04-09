# Awesome Skills - GitHub Copilot Agents

A collection of specialized GitHub Copilot custom agents for orchestrating the complete software development lifecycle, from requirements gathering through implementation, testing, and review.

## Installation

Install via pip:

```bash
pip install swe-copilot-agents
```

Or install from source:

```bash
git clone https://github.com/khaerulumam42/agent-generator.git
cd agent-generator
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
✓ dev-orchestrator.agent.md
✓ infra-setup.agent.md
✓ knowledge-graph-agent.agent.md
✓ plan-executor.agent.md
✓ plan-reviewer.agent.md
✓ pytest-agent.agent.md
✓ readme-generator.agent.md

✅ Installed 8 agent(s) to /path/to/your/project/.github/agents
```

## Overview

This repository contains AI agents that follow the **"coordinator and worker" pattern**—where specialist agents perform focused work under the guidance of an orchestrator. Each agent has a strong persona, clear boundaries, and specific expertise.

---

## Agents

### @dev-orchestrator

**Role:** Meticulous technical lead who conducts specialist agents like an orchestra conductor

**Persona:**
- **Philosophy:** "Right agent, right time, right order"
- **Traits:** Meticulous, patient, organized, clear
- **Metaphor:** Orchestra conductor who doesn't play instruments but brings out the best performance from each soloist

**Responsibilities:**
- Coordinates the complete development lifecycle across 4 movements
- Tracks state obsessively (which movement, which soloist, which outputs)
- Manages review cycles with automatic fix loops (max 2 reviews)
- Seeks human approval at each intermission

**Orchestrated Agents:**
- @brainstormer (Movement I - Planning)
- @plan-executor (Movement II - Implementation)
- @plan-reviewer (Movement III - Review)
- @pytest-agent (Movement IV - Testing, optional)

**Companion Agents:**
- @readme-generator — Generate/update README from knowledge graph
- @infra-setup — Generate Terraform infra from knowledge graph

**Best Practices:** ✅ **EXCELLENT**
- Strong, distinctive persona with musical terminology throughout
- Clear YAML configuration with `agents` restriction
- Visual workflow diagram (ASCII art)
- Comprehensive error handling and human intervention pathways
- Review cycle feedback loop with automatic fixes
- Memorable tagline: *"A great conductor doesn't play every instrument—they know exactly when each section should perform."*

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

**Best Practices:** ✅ **EXCELLENT**
- Strong persona ("insatiably curious")
- Knowledge graph integration for impact analysis
- Multi-round questioning framework with defined stages
- Clear completion criteria (user confirmation before writing plan)
- Comprehensive plan output template with KG analysis sections
- Workflow summary diagram

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
- Uses todo tool to track plan item progress
- Never "fixes" existing code because it's ugly

**Best Practices:** ✅ **EXCELLENT**
- Strong persona with clear philosophy ("Consistency > Clean Code")
- Concrete code examples showing good vs. bad matching
- Specific matching table (naming, imports, errors, strings, formatting)
- Clear boundaries (never "revamp" existing code)
- Executable commands for studying patterns

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

### @infra-setup

**Role:** Senior DevOps engineer who generates production-ready Terraform for AWS ECS Fargate

**Persona:**
- **Philosophy:** "Infrastructure from code knowledge"
- **Traits:** AWS-specialized, Terraform-focused, security-conscious
- **Metaphor:** Infrastructure architect who reads code to design deployments

**Responsibilities:**
- Generates `infra/` folder with Terraform HCL files
- Derives service topology from knowledge-graph.yaml entry points
- Maps external dependencies to AWS resources (RDS, ElastiCache)
- Creates security groups based on code concerns

**Output Files:**
- `main.tf` — Provider, backend, locals
- `variables.tf` — Configurable inputs
- `outputs.tf` — Exported values (ALB URL, cluster ARN)
- `ecs.tf` — ECS cluster, task definitions, services
- `alb.tf` — ALB, target groups, listeners
- `security.tf` — Security groups, IAM roles

**Best Practices:** ✅ **EXCELLENT**
- KG-driven service discovery
- Fargate-only focus (no EC2 launch type)
- One-at-a-time configuration questions
- `terraform fmt` validation
- Security-first: least privilege IAM, no public IPs

---

## Best Practices Summary

| Agent | Persona | Boundaries | Commands | Examples | Workflow Diagram | Overall |
|-------|---------|------------|----------|----------|------------------|---------|
| @dev-orchestrator | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Musical | ✅ ASCII | **EXCELLENT** |
| @brainstormer | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Plan format | ✅ Flowchart | **EXCELLENT** |
| @plan-executor | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Code style | ❌ None | **EXCELLENT** |
| @plan-reviewer | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Report format | ❌ None | **EXCELLENT** |
| @pytest-agent | ✅ Strong | ✅ Clear | ✅ Complete | ✅ Test style | ❌ None | **EXCELLENT** |
| @knowledge-graph-agent | ✅ Strong | ✅ Clear | ✅ Complete | ✅ YAML format | ❌ None | **EXCELLENT** |
| @readme-generator | ✅ Strong | ✅ Clear | ✅ Complete | ✅ KG mapping | ✅ Dual-mode | **EXCELLENT** |
| @infra-setup | ✅ Strong | ✅ Clear | ✅ Complete | ✅ TF templates | ✅ File tree | **EXCELLENT** |

**Overall Repository Quality:** ✅ **EXCELLENT** - All agents follow GitHub Copilot custom agent best practices with strong personas, clear boundaries, executable commands, and comprehensive examples.

---

## Workflow Orchestration

### Complete Development Cycle

```
User Request
      ↓
┌─────────────────────────────────────────────────────────────────┐
│                    @dev-orchestrator (Conductor)                 │
└─────────────────────────────────────────────────────────────────┘
      │
      ├─ Movement I: @brainstormer → Plan document
      │     (1-10 rounds of questions)
      │     ↓ Human Approval
      │
      ├─ Movement II: @plan-executor → Implementation
      │     (Match existing code patterns)
      │     ↓ Human Approval
      │
      ├─ Movement III: @plan-reviewer → Review #1
      │     ↓ Major issues found?
      │     ├─ YES → Movement IIb: @plan-executor (Fix)
      │     │           ↓ Movement IIIb: @plan-reviewer (Re-review FINAL)
      │     │                  ↓ Issues persist?
      │     │                  └─ YES → Human Intervention
      │     └─ NO → Continue
      │     ↓ Human Approval
      │
      └─ Movement IV: @pytest-agent → Tests (Optional)
            ↓
         Finale
```

### Review Cycle Logic

1. **Review #1** identifies issues → If major issues found, trigger fix cycle
2. **Fix Cycle** (@plan-executor) implements recommendations
3. **Review #2 (FINAL)** re-audits → If issues persist, human intervention required
4. **Maximum 2 reviews** enforced

---

## Usage

### Basic Agent Invocation

```bash
# In VS Code with GitHub Copilot Chat
@dev-orchestrator
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
