# Token Optimization Audit — agents/

**Date:** 2026-05-04
**Strategy:** Priority 1 (Prose→Structured, Remove Inline Examples, Narrow Toolset) + Priority 2 (Condense Stack, Simplify Dirs, Command Lists)
**Sources:** Token Optimization Strategy for AGENTS.md, Reducing Token Usage in GitHub Copilot Agents.md
**Best practices reference:** create-custom-agent.md, custom-agents-configuration.md, github-blog.txt

## Summary

| Agent | Before | After | Reduction |
|-------|--------|-------|-----------|
| plan-executor | 90 lines | 70 lines | ~22% |
| pytest-agent | 242 lines | TBD | TBD |
| readme-generator | 263 lines | TBD | TBD |
| knowledge-graph-agent | 347 lines | TBD | TBD |
| plan-reviewer | 351 lines | TBD | TBD |
| brainstormer | 321 lines | TBD | TBD |
| rug-orchestrator | 658 lines | TBD | TBD |
| **Total** | **2,272 lines** | **TBD** | **TBD** |

---

## plan-executor (90 lines → ~55 lines, ~39% reduction)

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
