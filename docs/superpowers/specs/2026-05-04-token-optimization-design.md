# Design: Token Optimization for agents/ Files

**Date:** 2026-05-04
**Status:** Approved
**Author:** @brainstormer

## Overview

All 7 agent files in `agents/` are significantly over-sized relative to best practices. Each token in an agent file is multiplied across every agent invocation, making verbose files expensive at scale. This design specifies a single-pass optimization (Priority 1 and 2 from the Token Optimization Strategy) that reduces token usage 50–75% per agent while preserving output quality and maintaining all best practices from official GitHub Copilot documentation.

## Goals

1. **Reduce token usage** via Priority 1 (prose→structured, remove inline examples, narrow toolset) and Priority 2 (condense tech stack, simplify directories, command lists) changes only.
2. **Maintain agent output** — same behavior, same output format, same boundaries.
3. **Produce an audit doc** at `docs/token-optimization-audit.md` documenting what each agent already does well, what was improved, and estimated line savings.
4. **Comply with best practices** from `create-custom-agent.md`, `custom-agents-configuration.md`, and `github-blog.txt`.

## Non-Negotiable Preservations (Official Best Practices)

Every optimized agent MUST retain:

| Element | Reason |
|---|---|
| YAML frontmatter (`name`, `description`, `tools`, `target`, `handoffs`, `agents`) | Required by spec; machine-parsed |
| Role/persona (1-2 sentences) | Core identity; defines agent behavior |
| Commands section early with flags | github-blog.txt: "Put commands early" |
| ONE real code/output example | github-blog.txt: "Code examples over explanations" |
| Three-tier boundaries (✅/⚠️/🚫) | github-blog.txt: "Three-tier boundaries" |
| Specific file structure (essential paths only) | github-blog.txt: "Be specific about your stack" |

## Audit Doc Structure

**File:** `docs/token-optimization-audit.md`

Each agent gets a section:
```
## [agent-name] (Before: X lines → After: Y lines, ~Z% reduction)

### ✅ Already Good
- [practices already following best practices]

### ❌ Needs Improvement
- [violations of Priority 1/2 rules]

### 💡 Changes Applied
- [specific removals/condensations with rationale]
```

## Per-Agent Trimming Specification

### brainstormer (322 lines → ~80 lines, moderate trimming)

**Remove:**
- ASCII cycle diagram (`User Request → Read Context → ...`) → replace with 3-bullet description
- "Example in Action" full Q&A session (Redis/search feature, ~20 lines)
- "Always Present Options with Pros/Cons" full format template block
- "Decision Helper Mode" full section including structure template, rules list, and Redis caching example (~70 lines) → condense to 3-bullet mention
- Completion Message code block template (~15 lines) → 2-bullet summary
- Bottom tagline (`*Your curiosity is your strength...`)

**Keep:**
- YAML frontmatter (name, description, tools, target, handoffs)
- Role sentence + Output + Constraint bullets
- Commands section — keep top 4 KG queries + read context + create plan commands
- Questioning cycle as bullet list (no diagram)
- Track Progress 4-round summary (keep as-is, already concise)
- Knowledge Graph section (condensed to 4 bullets)
- Plan Document Template — section names as list only (not full markdown template)
- Boundaries (✅/⚠️/🚫) — keep as-is

### knowledge-graph-agent (348 lines → ~80 lines, aggressive)

**Remove:**
- Full YAML output format schema (~50 lines) → replace with "10 sections: metadata, entry_points, files, relationships, data_flow, concerns, tests, external_dependencies, imports, inheritance" as single bullet
- Three "Analysis Standards" YAML code examples (Function Entry, Class Relationship Entry, Call Chain Entry, ~55 lines) → remove entirely (naming conventions bullet is sufficient)
- Four "Web Framework Patterns" code examples (Flask, FastAPI, Express, Gin, ~35 lines) → replace with "Detect entry points from framework decorators: Flask @app.route, FastAPI @get/@post, Express app.get/post, Gin router.GET/POST"
- Incremental Update Mode detailed 5-step list → condense to 3 bullets

**Keep:**
- YAML frontmatter
- Role bullets (4 lines)
- Startup Behavior: Step 1-3 condensed as bullet steps
- Project Knowledge: tech stack bullets (keep as-is, already concise)
- File Structure section (keep as-is)
- Commands section — keep all (already grouped by language, necessary)
- Scanning Strategy: Full Scan 4-phase as bullets
- Boundaries (✅/⚠️/🚫) — keep as-is
- Validation Checklist — keep as-is

### plan-executor (91 lines → ~45 lines, light)

**Remove:**
- Python code style comparison block (15 lines, `get_usr`/`get_post`/`get_user_by_identifier`) → replace with inline 2-line contrast showing the key point
- Bottom tagline

**Keep:**
- YAML frontmatter (name, description, tools, handoffs)
- Role sentence + Core Philosophy
- Workflow numbered list (5 steps)
- What to Match table (already concise)
- Boundaries (Always/Never bullets) — keep as-is
- Commands section

### plan-reviewer (352 lines → ~80 lines, aggressive)

**Remove:**
- Full Report Output Format markdown template (~80 lines) → replace with "Report sections: Executive Summary, Requirements Breakdown (status per requirement with evidence + gap analysis), Priority Action Items table (P0–P3), Statistics table, Brittleness Analysis (if KG available), Next Steps"
- Duplicate brittleness analysis report format block inside "Knowledge Graph Brittleness Analysis" section (~35 lines) → keep only the 3 bash commands + Brittleness Risk Levels table
- "Status Determination Rules" section (duplicates the status definitions table above it)
- Bottom tagline

**Keep:**
- YAML frontmatter
- Role bullets (4 lines)
- Core Philosophy sentence
- Workflow numbered list (condensed to 9 steps)
- Execution Status Definitions table
- Evidence Gathering Checklist
- Knowledge Graph Brittleness Analysis: keep 3 bash commands + Risk Levels table only
- Priority Assignment Criteria table
- Commands section — condense to 6 essential commands
- Boundaries (Always/Ask First/Never) — keep as-is

### pytest-agent (243 lines → ~70 lines, aggressive)

**Remove:**
- Expert Mocking & Patching large code block (~30 lines) → replace with 5-bullet technique list: "configure return_value/side_effect; patch at point of use; use spec= for strict mocking; mock property with PropertyMock; async with @patch"
- Standards > Code Style Example (~30 lines) → keep ONLY the 2-line good/bad test name contrast as the ONE real example
- Clarification Protocol full formatted example block (~20 lines) → replace with 5-bullet list of what to ask about
- Scope Boundaries section → merge into Boundaries (✅/⚠️/🚫)
- Bottom tagline

**Keep:**
- YAML frontmatter
- Role + Core Philosophy
- Workflow (5 steps)
- Commands section — condense to 8 key commands with flags
- Test Coverage Requirements table
- ONE code example (2-line good/bad name contrast)
- Assertion Style bullets (4 lines)
- Mock Style bullets (3 lines)
- Clarification Protocol as 5 bullets (no example block)
- Boundaries (Always/Ask First/Never) — keep as-is

### readme-generator (264 lines → ~70 lines, aggressive)

**Remove:**
- Mode 1 full README template (~40 lines) → replace with section list: "Sections: project name, Overview, Tech Stack, Project Structure, Getting Started (Prerequisites + Installation + Running), Architecture, API Reference, Testing, License"
- Three "Extracting README Data from KG" YAML→README before/after examples (~60 lines) → replace with "Extract tech stack from metadata.languages; running commands from entry_points; project structure from files keys; dependencies from external_dependencies"
- Completion Message code block template → replace with 2-bullet summary
- Bottom tagline

**Keep:**
- YAML frontmatter (name, description, tools, handoffs)
- Role bullets (3 lines)
- Core Philosophy sentence
- Startup Behavior: 2 steps condensed as bullets
- Commands section — condense to 6 essential commands
- Section Mapping table (Mode 2) — keep as-is
- Mode 2 Update Rules (4 numbered rules) — keep as-is
- Boundaries (✅/⚠️/🚫) — keep as-is

### rug-orchestrator (659 lines → ~100 lines, aggressive)

**Remove:**
- All "YOU:" dialogue example blocks per phase (Phase 0, 0.5, 1, 2, 3, 4, 5, 6) → replace each phase with 2-3 bullet behavioral description
- 85-line ASCII art orchestration diagram → replace with "Phase order: 0 Plan Check → 0.5 KG Check → 1 Planning (if needed) → 2 Task Decomp → 3 Implementation → 4 Validation → 5 RUG Loop → 6 Testing (optional)"
- Session Initialization long welcome message (~30 lines) → 4-bullet capability summary
- Common Failure Modes table (11 rows) → keep top 5 most critical rows only
- Task Decomposition Examples "BAD" example → keep only GOOD example (condensed)
- Parallel Execution Pattern full dialogue example → replace with 3-bullet description
- "Commands You Can Use" verbose section → replace with 4-bullet rule (delegate everything)

**Keep:**
- YAML frontmatter (name, description, tools, agents, target)
- Core Philosophy + Cardinal Rule (keep the emphasized quotes)
- How to Delegate key paragraph + delegation prompt template (ONE, condensed)
- Subagent Tool Autonomy bullet list (6 bullets, keep as-is — critical for correct behavior)
- Orchestra table (5 specialists)
- Phase descriptions as condensed bullet behavioral rules (not dialogue)
- Result Routing Table — keep as-is
- Boundaries (Always/Ask First/Never) — keep but condense Always list from 12 to 7 most critical

## Execution Plan (Approach C: Single Pass)

For each agent, in this order:
1. Read current file
2. Write audit section (✅/❌/💡) to `docs/token-optimization-audit.md`
3. Apply trims per specification above
4. Write optimized agent file

**Order:** plan-executor (lightest, warm up) → pytest-agent → readme-generator → knowledge-graph-agent → plan-reviewer → brainstormer → rug-orchestrator (heaviest, last)

## Success Criteria

- [ ] All 7 agent files updated
- [ ] `docs/token-optimization-audit.md` created with per-agent sections
- [ ] Every agent retains: YAML frontmatter, role/persona, commands with flags, ONE code example (where applicable), three-tier boundaries, file structure
- [ ] No agent exceeds 110 lines
- [ ] All agents remain valid `.agent.md` files (valid YAML frontmatter)
- [ ] Git committed with descriptive message
