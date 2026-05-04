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
| plan-reviewer | 351 lines | TBD | TBD |
| brainstormer | 321 lines | TBD | TBD |
| rug-orchestrator | 658 lines | TBD | TBD |
| **Total** | **2,272 lines** | **TBD** | **TBD** |

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
