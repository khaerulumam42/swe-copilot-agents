# Agent Evaluation Report

**Date:** 2026-04-20
**Purpose:** Evaluation of all `.agent.md` files against GitHub Copilot agent best practices

## Evaluation Criteria

Based on the best practices from `copilot-agent-sources/`, each agent was evaluated against:

| Criterion | Description | Example |
|-----------|-------------|---------|
| Clear persona | Specific role definition (not vague "helpful assistant") | ✅ "senior Python QA engineer who writes pytest tests"<br>❌ "I am a helpful coding assistant" |
| Commands early with flags | Executable commands placed early, with flags/options | ✅ `pytest -v --tb=short`<br>✅ `npm run build -- --production`<br>❌ "run the tests" |
| Code examples over explanations | Real code snippets showing good output style | ✅ Show actual test structure with fixtures<br>❌ "Write tests that use fixtures" |
| Clear boundaries | Always Do / Ask First / Never Do sections | ✅ **Always:** Run `pytest -v` before editing<br>✅ **Never:** Skip edge case tests<br>❌ "Be careful with tests" |
| Tech stack with versions | Specific technologies with version numbers | ✅ "Python 3.8+, pytest 7.0+, Django 4.2+"<br>❌ "Python and Django" |
| Concise/value dense | Under ~400-500 lines (30k chars), focused content | ✅ 230 lines of focused instructions<br>❌ 492 lines with excessive templates |

## Agent Evaluations

### ✅ plan-executor.agent.md — GOOD

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "senior **Python 3.8+** engineer who executes plans by **blending seamlessly** with existing codebases" |
| Commands early with flags | ✅ | Lines 66-76: `find src/ -name "*.py"`, `cat src/models/*.py`, `pytest tests/ -v`, `python -m py_compile` |
| Code examples over explanations | ✅ | Lines 33-47: Shows matching vs non-matching style with concrete `get_usr()` example |
| Clear boundaries | ✅ | Lines 49-62: Always/Never sections with specific rules |
| Tech stack with versions | ✅ | "Python 3.8+" specified on line 7 |
| Concise/value dense | ✅ | 90 lines, focused on single responsibility |
| Unique features | ✅ | `todo` tool for plan item tracking; Handoff to @plan-reviewer |

**Status:** GOOD — Clear, focused agent with excellent style-matching examples. Added `todo` tool for progress tracking and handoff support for review workflow.

---

### ✅ plan-reviewer.agent.md — GOOD

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "senior code reviewer and quality assurance engineer who rigorously audits implementation completeness" |
| Commands early with flags | ✅ | Lines 136-169: Multi-language commands (`pytest -v --tb=short`, `npm test`, `cargo test`, `go test ./...`, `yq`) |
| Code examples over explanations | ✅ | Lines 59-132: Brittleness analysis examples with concrete bash commands and YAML tables |
| Clear boundaries | ✅ | Lines 315-342: Always Do / Ask First / Never Do sections |
| Tech stack with versions | ⚠️ | Generic multi-language (pytest, npm, cargo, go) - no specific versions |
| Concise/value dense | ✅ | 346 lines (was 492) - streamlined |

**Status:** GOOD — Streamlined from 492 to 346 lines. Excellent brittleness analysis integration with knowledge graph. Could add specific versions for each language.

---

### ✅ pytest-agent.agent.md — GOOD

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "senior **Python 3.8+** QA engineer specializing in pytest with expert-level knowledge of mocking" |
| Commands early with flags | ✅ | Lines 29-62: Comprehensive pytest commands with flags (`--cov=src`, `--lf`, `-k "test_payment"`, `-n auto`) |
| Code examples over explanations | ✅ | Lines 94-121: Expert mocking examples with real code patterns; Lines 134-167: Good vs Bad test style |
| Clear boundaries | ✅ | Lines 209-233: Always Do / Ask First / Never Do sections |
| Tech stack with versions | ✅ | "Python 3.8+" specified on line 7 |
| Concise/value dense | ✅ | 237 lines, focused on testing scope |

**Status:** GOOD — Comprehensive test coverage guidance with excellent mocking examples. Unique clarification protocol is valuable.

---

### ✅ knowledge-graph-agent.agent.md — EXCELLENT

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "expert code analysis specialist who builds knowledge-base graphs from codebases" |
| Commands early with flags | ✅ | Lines 107-164: Multi-language commands with specific tools (`ast`, `tsc --noEmit`, `go list -json`, `yq`) |
| Code examples over explanations | ✅ | Lines 168-224: Complete YAML entry examples with bidirectional references |
| Clear boundaries | ✅ | Lines 301-333: Always Do / Ask First / Never Do with checkboxes |
| Tech stack with versions | ✅ | "Python 3.8+, JavaScript/TypeScript ES6+, Go 1.19+, Java 17+, Rust" |
| Concise/value dense | ✅ | 347 lines, comprehensive for complex multi-language task |
| Unique features | ✅ | Startup behavior with commit hash checking and incremental update mode |

**Status:** EXCELLENT — Best practices exemplified: specific versions, comprehensive examples, clear boundaries, unique startup behavior for incremental updates. No changes needed.

---

### ✅ brainstormer.agent.md — EXCELLENT

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "curious brainstorming specialist who transforms vague ideas into crystal-clear specifications through thoughtful questioning" |
| Commands early with flags | ✅ | Lines 265-294: Knowledge graph queries (`yq`, `grep`, `find`) with specific flags |
| Code examples over explanations | ✅ | Lines 82-161: Complete plan document template; Lines 161-255: Decision Helper Mode with full example; Lines 217-238: Good vs Bad question examples |
| Clear boundaries | ✅ | Lines 277-301: Always Do / Ask First / Never Do sections |
| Tech stack with versions | ⚠️ | Not applicable (planning agent - no code execution) |
| Concise/value dense | ✅ | 321 lines - justified for complex planning + decision helper workflow |
| Unique features | ✅ | Knowledge Graph integration, Multi-round questioning (1-10 rounds), Decision Helper Mode with structured options/comparison/recommendation, Handoff support to @plan-executor and @dev-orchestrator |

**Status:** EXCELLENT — Decision Helper Mode adds structured comparison/recommendation capability. Handoff support enables seamless workflow transitions. Knowledge graph integration and multi-round questioning remain key differentiators.

---

### ✅ dev-orchestrator.agent.md — EXCELLENT

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "meticulous technical lead who conducts AI agents like an orchestra conductor" |
| Commands early with flags | ✅ | Movement-based workflow with specific agent invocation commands, `find docs/plan/`, `cat` commands |
| Code examples over explanations | ✅ | ASCII workflow diagram showing 4 movements, state tracking format, completion messages |
| Clear boundaries | ✅ | Always Do / Ask First / Never Do sections with specific rules per movement |
| Tech stack with versions | ⚠️ | Coordination agent — delegates to specialists, no direct code execution |
| Concise/value dense | ✅ | 560 lines — justified by complex 4-movement orchestration with review cycles |
| Unique features | ✅ | Musical metaphor throughout (movements, interludes, finale), review cycle feedback loop (max 2 reviews), human approval gates, state tracking |

**Status:** EXCELLENT — Distinctive conductor persona with comprehensive lifecycle management. Review cycle feedback loop and human approval gates ensure quality. Musical terminology creates memorable, cohesive identity.

---

### ✅ readme-generator.agent.md — EXCELLENT

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "technical writer who transforms code knowledge into clear, accurate README documentation" |
| Commands early with flags | ✅ | `yq` queries for KG sections, `grep "<!-- KG:"`, `cat README.md \| head -50` |
| Code examples over explanations | ✅ | Complete README template, KG-to-README mapping examples, dual-mode behavior |
| Clear boundaries | ✅ | Always Do / Ask First / Never Do — strict about preserving manual content |
| Tech stack with versions | ⚠️ | Documentation agent — reads KG data, no specific tech stack required |
| Concise/value dense | ✅ | 263 lines, focused on README generation and update workflows |
| Unique features | ✅ | Dual-mode behavior (generate new vs. update existing), `<!-- KG:SECTION -->` markers for safe updates, section mapping table, KG handoff |

**Status:** EXCELLENT — Unique dual-mode design solves a real problem (updating READMEs without losing manual content). KG section markers are an elegant solution for mixed human/AI documentation.

---

### ✅ infra-setup.agent.md — EXCELLENT

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "senior DevOps engineer who generates production-ready Terraform configurations for AWS ECS Fargate" |
| Commands early with flags | ✅ | `yq` queries for KG parsing, `terraform fmt -check`, `terraform validate` |
| Code examples over explanations | ✅ | Complete Terraform HCL templates (main.tf, variables.tf, outputs.tf, ecs.tf, alb.tf, security.tf) |
| Clear boundaries | ✅ | Always Do / Ask First / Never Do — strict about no `terraform apply`, no secrets, Fargate only |
| Tech stack with versions | ✅ | AWS ECS Fargate, Terraform >= 1.0, AWS provider ~> 5.0 |
| Concise/value dense | ✅ | 351 lines — justified by complete infrastructure generation with 6 output files |
| Unique features | ✅ | KG-driven service discovery (entry_points → ECS services, dependencies → resources, concerns → security groups), one-at-a-time configuration questions |

**Status:** EXCELLENT — KG-driven infrastructure generation is a unique and valuable approach. Maps code architecture directly to AWS resources. Security-first IAM policies and Fargate-only constraint are well-defined.

---

## Summary Table

| Agent | Status | Lines | Key Strengths | Notes |
|-------|--------|-------|---------------|-------|
| dev-orchestrator | ✅ EXCELLENT | 560 | Orchestra conductor persona, review cycles | Manages full lifecycle |
| brainstormer | ✅ EXCELLENT | 321 | Decision Helper Mode, KG integration | Handoff to executor/orchestrator |
| plan-executor | ✅ GOOD | 90 | Excellent style-matching examples | Added `todo` tool, handoff to reviewer |
| plan-reviewer | ✅ GOOD | 351 | Brittleness analysis integration | Streamlined from 492 lines |
| pytest-agent | ✅ GOOD | 242 | Expert mocking examples | Unique clarification protocol |
| knowledge-graph-agent | ✅ EXCELLENT | 347 | All criteria met perfectly | Best practices exemplified |
| readme-generator | ✅ EXCELLENT | 263 | Dual-mode (generate/update), KG markers | Preserves manual content |
| infra-setup | ✅ EXCELLENT | 351 | KG-driven Terraform, Fargate-focused | Security-first IAM |

## Best Practices Reference

Based on analysis of 2,500+ agent files:

1. **Be concise, specific, and value dense** — Shorter, focused files outperform verbose ones
2. **Commands early** — Put executable commands with flags at the beginning
3. **Code examples over explanations** — One real snippet beats three paragraphs
4. **Clear boundaries** — Always Do / Ask First / Never Do sections prevent mistakes
5. **Specific tech stack** — Include versions (e.g., "Python 3.8+" not just "Python")
6. **Cover six core areas:** Commands, testing, project structure, code style, git workflow, boundaries

## Hard Limit

The prompt (markdown content below YAML frontmatter) has a maximum of **30,000 characters**.

All current agents are well under this limit.
