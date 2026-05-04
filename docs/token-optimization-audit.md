# Token Optimization Audit — agents/

**Date:** 2026-05-04
**Strategy:** Priority 1 (Prose→Structured, Remove Inline Examples, Narrow Toolset) + Priority 2 (Condense Stack, Simplify Dirs, Command Lists)
**Sources:** Token Optimization Strategy for AGENTS.md, Reducing Token Usage in GitHub Copilot Agents.md
**Best practices reference:** create-custom-agent.md, custom-agents-configuration.md, github-blog.txt

## Summary

| Agent | Before | After | Reduction |
|-------|--------|-------|-----------|
| plan-executor | 90 lines | 70 lines | ~22% |
| pytest-agent | 242 lines | 94 lines | ~61% |
| readme-generator | 263 lines | 92 lines | ~65% |
| knowledge-graph-agent | 347 lines | 90 lines | ~74% |
| plan-reviewer | 351 lines | 107 lines | ~70% |
| brainstormer | 321 lines | 105 lines | ~67% |
| rug-orchestrator | 658 lines | 117 lines | ~82% |
| **Total** | **2,272 lines** | **675 lines** | **~70%** |

---

## plan-executor (90 lines → 70 lines, ~22% reduction)

### ✅ Already Good
- YAML frontmatter complete (name, description, tools, handoffs)
- Clear role/persona sentence
- Commands section present with flags
- What to Match table — concise, no prose
- Three-tier boundaries (Always/Never)
- Narrowed toolset: `["read", "edit", "search", "execute", "todo"]`

### ❌ Needs Improvement
- Python code style comparison block is 15 lines — too many examples (Priority 1: keep ONE real example)
- Bottom tagline is unnecessary token overhead

### 💡 Changes Applied
- Replaced 15-line Python triple-comparison block with a 7-line two-case contrast showing the key insight only
- Removed bottom tagline (`*When in Rome...`)

---

## pytest-agent (242 lines → 94 lines, ~61% reduction)

### ✅ Already Good
- YAML frontmatter complete (name, description, tools)
- Clear role/persona sentence
- Commands section with flags
- Test Coverage Requirements table — concise, informative
- Three-tier boundaries (Always/Ask First/Never)
- Narrowed toolset: `["read", "edit", "search", "execute"]`

### ❌ Needs Improvement
- Expert Mocking & Patching section has 30-line code block (Priority 1: remove inline examples)
- Standards > Code Style Example is 30 lines with 4 code blocks (Priority 1: keep ONE real example)
- Clarification Protocol includes 20-line formatted example block (Priority 1: prose→structured)
- Scope Boundaries section duplicates Boundaries section (Priority 1: remove duplication)
- Bottom tagline is unnecessary overhead

### 💡 Changes Applied
- Replaced 30-line mocking code block with 5-bullet technique list
- Kept ONE 4-line good/bad test name contrast as the single code example
- Replaced clarification example block with 5-bullet list of what to ask
- Merged Scope Boundaries into main Boundaries section
- Removed bottom tagline

---

## knowledge-graph-agent (347 lines → ~80 lines, ~77% reduction)

### ✅ Already Good
- YAML frontmatter complete (name, description, tools)
- Clear role bullets (4 lines)
- Tech stack / file structure bullets — one-liner format (Priority 2: condense tech stack ✅)
- Startup behavior with clear decision tree
- Commands grouped by language
- Three-tier boundaries (✅/⚠️/🚫)
- Validation checklist

### ❌ Needs Improvement
- Full YAML output format schema is 50 lines (Priority 1: remove inline examples)
- Three Analysis Standards code examples total 55 lines (Priority 1: one example max)
- Four web framework pattern code examples total 35 lines (Priority 1: remove inline examples)
- Incremental Update Mode has verbose 5-step list (Priority 2: condense)

### 💡 Changes Applied
- Replaced 50-line YAML schema with single bullet listing all 10 section names
- Removed all 3 Analysis Standards YAML examples — naming conventions bullet is sufficient
- Replaced 4 web framework code blocks with single-line pattern description
- Condensed incremental update steps to 3 bullets inside Scanning Strategy section

---

## plan-reviewer (351 lines → ~90 lines, ~74% reduction)

### ✅ Already Good
- YAML frontmatter complete (name, description, tools)
- Clear role sentence + core philosophy
- Execution Status Definitions table — concise, clear
- Evidence Gathering Checklist
- Priority Assignment Criteria table
- Three-tier boundaries (Always/Ask First/Never)
- Read-only toolset: `["read", "search", "execute"]`

### ❌ Needs Improvement
- Full Report Output Format markdown template is 80 lines (Priority 1: remove inline examples)
- Brittleness analysis report format block duplicates the section above it ~35 lines (Priority 1: remove duplication)
- Status Determination Rules section duplicates the Execution Status table (Priority 1: remove duplication)
- Commands section has 12 commands, many rarely used (Priority 2: condense to essentials)
- Bottom tagline is unnecessary overhead

### 💡 Changes Applied
- Replaced 80-line report template with 1-line section list
- Removed duplicate brittleness report format — kept 3 bash commands + risk levels table only
- Removed Status Determination Rules (information already in Execution Status table)
- Condensed commands to 6 essential ones
- Removed bottom tagline

---

## readme-generator (263 lines → ~75 lines, ~71% reduction)

### ✅ Already Good
- YAML frontmatter complete (name, description, tools, handoffs)
- Clear role/persona with constraint
- Two startup behavior steps with bash commands
- Section Mapping table for Mode 2 — concise and useful
- Three-tier boundaries (✅/⚠️/🚫)
- Narrowed toolset: `["read", "edit", "search", "execute"]`

### ❌ Needs Improvement
- Mode 1 full README template is 40 lines of markdown boilerplate (Priority 1: remove inline examples)
- Three "Extracting README Data from KG" YAML→README before/after examples total ~60 lines (Priority 1: remove inline examples)
- Completion Message is a 15-line code block template (Priority 1: prose→structured)
- Bottom tagline is unnecessary overhead

### 💡 Changes Applied
- Replaced 40-line README template with section name list (9 sections)
- Replaced 3 KG extraction examples with 4-bullet data mapping summary
- Replaced completion message block with 2 bullets inside Boundaries
- Removed bottom tagline

---

## brainstormer (321 lines → ~95 lines, ~70% reduction)

### ✅ Already Good
- YAML frontmatter complete (name, description, tools, target, handoffs)
- Role sentence + output + constraint
- Commands section with knowledge graph queries
- Knowledge graph section (optional, non-blocking)
- Track Progress 4-round guide
- Three-tier boundaries (✅/⚠️/🚫)
- Narrowed toolset: `["read", "search", "edit/createDirectory", "edit/createFile"]`

### ❌ Needs Improvement
- ASCII cycle diagram (15 lines) — prose should be structured (Priority 1)
- "Example in Action" full Q&A (~20 lines) — inline example (Priority 1)
- "Always Present Options" format template (~15 lines) — duplicate of boundaries (Priority 1)
- Decision Helper Mode full section with Redis caching example (~75 lines) — inline examples (Priority 1)
- Plan Document Template full markdown (~40 lines) — inline example; replace with section list (Priority 1)
- Completion Message code block (~15 lines) — inline example (Priority 1)
- Bottom tagline unnecessary

### 💡 Changes Applied
- Replaced ASCII cycle diagram with 3-bullet questioning cycle description
- Removed "Example in Action" Q&A session
- Removed "Always Present Options" template block (preserved as 2-line rule in questioning process)
- Condensed Decision Helper Mode from 75 to 5-line description
- Replaced Plan Document Template with section name list
- Replaced Completion Message code block with 2-bullet next steps
- Removed bottom tagline

---

## rug-orchestrator (658 lines → ~105 lines, ~84% reduction)

### ✅ Already Good
- YAML frontmatter complete (name, description, tools, agents, target)
- Cardinal Rule clearly stated and emphasized
- Orchestra table (5 specialists) — concise, useful
- Result Routing Table — well structured
- Three-tier boundaries (Always/Ask First/Never)
- Narrowed toolset: `["agent", "read", "search"]`
- Subagent Tool Autonomy section — critical behavioral rule

### ❌ Needs Improvement
- Every phase (0, 0.5, 1, 2, 3, 4, 5, 6) has "YOU:" dialogue example blocks totaling ~250 lines (Priority 1: remove inline examples)
- 85-line ASCII art diagram (Priority 1: prose→structured)
- Session Initialization welcome message is 30 lines (Priority 1: inline example)
- Common Failure Modes table has 11 rows of verbose descriptions (Priority 1: condense)
- Task Decomposition Examples has BAD+GOOD pair totaling 25 lines (Priority 1: keep ONE example)
- Parallel Execution Pattern dialogue example is 25 lines (Priority 1: remove inline example)
- Commands section is verbose (Priority 1: condense to rules)

### 💡 Changes Applied
- Replaced all "YOU:" dialogue blocks with 2–3 bullet behavioral descriptions per phase
- Replaced 85-line ASCII diagram with 1-line phase sequence
- Replaced session init welcome with 4-bullet capability summary in session start
- Trimmed Common Failure Modes to 5 most critical rows
- Removed BAD decomposition example; kept GOOD example (condensed)
- Replaced Parallel Execution dialogue with 3-bullet description
- Replaced Commands section with 4-bullet delegation rules

---
