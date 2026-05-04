## Token Optimization Strategy for AGENTS.md

Based on research into GitHub Copilot token usage patterns, here's the optimization roadmap ordered by efficiency:

### Priority 1: High-Impact Changes (60%+ savings)

**1. Prose → Structured Format** (Estimated: 60% reduction)
- Convert narrative paragraphs to bullet lists
- Add YAML frontmatter: `name`, `description`
- Use three-tier structure: "Always do / Ask first / Never do"
- Example: 170 tokens → 70 tokens (real case study)

**2. Remove Inline Code Examples** (Estimated: 30-50% per prompt)
- Replace embedded scripts with command references
- Remove duplicate code snippets
- Link to docs instead of copying content
- Keep ONE real example maximum

**3. Narrow Toolset** (Estimated: 2-3K tokens/turn per tool removed)
- Load only required tools (`[issues]` not `[default]`)
- Disable unused MCP tools
- Use CLI proxies (`gh api`) for simple operations

### Priority 2: Medium-Impact Changes (20-30% savings)

**4. Condense Tech Stack** (Estimated: 20-30%)
- One-line bullet format: `**Stack:** React 18, TypeScript, Vite`
- Remove version details for non-critical dependencies
- Skip obvious framework inclusions

**5. Simplify Directory Trees** (Estimated: 10-20%)
- Essential paths only: `**Dirs:** frontend/ (JS), backend/ (Python), tests/`
- No full directory trees or file listings

**6. Command Lists** (Estimated: 15-25%)
- List shell commands early, with flags
- Format: `**Commands:** npm run build, pytest -q`
- Remove setup narratives

### Priority 3: Polish (10-15% savings)

**7. Consolidate Boundaries** (Estimated: 10-15%)
- Use emoji markers: ✅ Always / 🚫 Never
- Remove redundant "must not" statements
- One boundary section maximum

**8. Target File Length** (Target: <20-30 lines total)
- Every line counts on every agent turn
- Trim until quality drops, then stop
- Monitor token usage before/after changes

### Validation Methodology

After each optimization:
1. **Measure tokens**: Use `/context` or token usage logs
2. **A/B test**: Run same task with old vs new prompt
3. **Quality check**: Verify output meets requirements
4. **Iterate**: Rollback if accuracy drops

### Trade-offs to Monitor

- **Information loss**: May cause hallucinations if over-trimmed
- **Model choice**: Smaller models save tokens but may need more retries
- **Quality vs cost**: Reserve rich context for high-risk tasks, minimal for routine work

**Golden Rule**: Treat `agents.md` like high-cost configuration — every word is multiplied by every agent invocation.