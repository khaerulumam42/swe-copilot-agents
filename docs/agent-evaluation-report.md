# Agent Evaluation Report

**Date:** 2026-02-22
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
| Concise/value dense | ✅ | 80 lines, focused on single responsibility |

**Status:** GOOD — Clear, focused agent with excellent style-matching examples

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

### ✅ brainstormer.agent.md — GOOD

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear persona | ✅ | "curious brainstorming specialist who transforms vague ideas into crystal-clear specifications through thoughtful questioning" |
| Commands early with flags | ✅ | Lines 265-294: Knowledge graph queries (`yq`, `grep`, `find`) with specific flags |
| Code examples over explanations | ✅ | Lines 82-161: Complete plan document template; Lines 217-238: Good vs Bad question examples |
| Clear boundaries | ✅ | Lines 296-319: Always Do / Ask First / Never Do sections |
| Tech stack with versions | ⚠️ | Not applicable (planning agent - no code execution) |
| Concise/value dense | ✅ | 377 lines - longer but justified for complex planning workflow |
| Unique features | ✅ | Knowledge Graph integration (4 critical analyses), Multi-round questioning framework (1-10 rounds) |

**Status:** GOOD — Unique purpose with well-structured questioning framework and valuable knowledge graph integration. Longer length is justified by complex planning workflow.

---

## Summary Table

| Agent | Status | Lines | Key Strengths | Notes |
|-------|--------|-------|---------------|-------|
| plan-executor | ✅ GOOD | 80 | Excellent style-matching examples | Clear, focused |
| plan-reviewer | ✅ GOOD | 346 | Brittleness analysis integration | Streamlined from 492 lines |
| pytest-agent | ✅ GOOD | 237 | Expert mocking examples | Unique clarification protocol |
| knowledge-graph-agent | ✅ EXCELLENT | 347 | All criteria met perfectly | Best practices exemplified |
| brainstormer | ✅ GOOD | 377 | Knowledge Graph integration | Longer length justified |

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
