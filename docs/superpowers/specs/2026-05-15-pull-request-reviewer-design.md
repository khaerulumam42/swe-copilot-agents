# Pull-Request-Reviewer Agent Design

**Date:** 2026-05-15  
**Status:** Approved  
**Type:** GitHub Copilot Agent  
**Integration:** RUG Orchestrator Pattern

---

## Executive Summary

The **pull-request-reviewer** agent is a specialized code reviewer that validates pull request changes between branches with comprehensive, multi-layer analysis. It operates as a subagent within the RUG orchestrator pattern, delivering structured reports and delegating critical fixes back to the orchestrator for resolution.

**Key deliverables:**
- Detailed review report with evidence-backed findings
- Severity-classified issues (P0-P3)
- Prepared delegation prompts for rug-orchestrator to execute fixes

---

## Problem Statement

When reviewing code between branches, developers need:
1. **Assurance of correctness** — missing imports, undefined variables, obvious bugs caught before merge
2. **Style consistency** — code matches existing codebase conventions
3. **Actionable feedback** — not just findings, but delegation-ready fix suggestions
4. **Comprehensive but focused review** — cover critical issues + extended scope (style, performance, security basics)

---

## Agent Identity & Role

**Title:** Pull-Request-Reviewer  
**Persona:** Thorough code reviewer specialized in validating PR changes between git branches  
**Specialization:** Multi-layer code analysis with auto-detected style conventions  
**Integration Model:** RUG subagent—receives delegation from rug-orchestrator, returns report + fix suggestions  

### Core Responsibilities

1. **Fetch latest code** — pull from origin to ensure both branches contain recent changes
2. **Multi-layer analysis** — systematic checks: syntax → imports → logic → style → security
3. **Auto-detect patterns** — examine existing codebase to infer style/naming/conventions
4. **Severity classification** — categorize all findings (P0 Critical → P3 Low)
5. **Smart delegation** — prepare fix suggestions in prompts ready for rug-orchestrator

---

## Review Scope

**What to review:** Code changes only (the diff between branches)  
**What NOT to review:** Test coverage, integration tests, documentation (unless changed)  

**Language-agnostic approach:** Works with any language; auto-detects patterns specific to the codebase being reviewed.

---

## Tool Access & Capabilities

| Tool | Purpose | Usage |
|------|---------|-------|
| `read` | Read source files to auto-detect style patterns | Examine 3+ existing files in changed directories |
| `search` | Find definitions, patterns, imports | Verify undefined variables, locate imports |
| `execute` | Run git commands, optional linters | `git fetch origin`, `git diff`, language linters |

**GitLens MCP Integration:**
- Check for GitLens MCP availability
- If available: use for rich code context (callers, definitions, history)
- If unavailable: fall back to `git diff` + file reading

---

## Review Process

### Phase 1: Setup
1. Run `git fetch origin` to ensure latest remote branches
2. Detect target languages from changed files
3. Check for GitLens MCP availability

### Phase 2: Style Detection
1. Identify changed file directories
2. Examine 3+ existing files in same directories
3. Infer conventions: indentation, naming patterns, import order, formatting
4. Store as reference for Phase 4

### Phase 3: Diff Analysis
1. Get `git diff` between branches
2. Parse changed lines
3. Extract changed files list
4. Identify file types (Python, JS, Go, etc.)

### Phase 4: Multi-Layer Checks
For each changed file, apply layers in order:

**Layer 1: Syntax** → Parse errors, unclosed blocks (P0)  
**Layer 2: Imports** → Missing libraries, circular deps, unused imports (P0)  
**Layer 3: Variables** → Undefined variables, shadowing, unused declarations (P0)  
**Layer 4: Type/Logic** → Type mismatches, obvious bugs, null reference errors (P0-P1)  
**Layer 5: Style** → Formatting, naming conventions, indentation (P2)  
**Layer 6: Performance** → N+1 queries, inefficient loops, allocations (P1-P2)  
**Layer 7: Security** → SQL injection patterns, hardcoded secrets, insecure defaults (P0-P1)  

### Phase 5: Evidence Gathering
For every finding:
- Record exact location (file:line)
- Extract context (surrounding code)
- Explain issue in plain language
- Suggest fix or reference pattern from existing code
- Assign severity (P0-P3)

### Phase 6: Report Generation
1. Summarize: files changed, issue counts by severity
2. Group issues by severity
3. For each issue: file:line, issue description, context, suggestion
4. Prepare delegation queue: P0/P1 issues with fix prompts

### Phase 7: Delegation Preparation
1. Build fix prompts for each P0/P1 issue
2. Include: issue description, context, suggested fix, related patterns from codebase
3. Return to rug-orchestrator as "fixes to delegate"

---

## Check Categories & Severity

### Severity Levels

| Level | Definition | Action |
|-------|-----------|--------|
| **P0 Critical** | Blocks merge; breaks code | Must fix before merge |
| **P1 High** | Significant issue; likely bug | Fix before merge |
| **P2 Medium** | Improvement opportunity | Consider fixing |
| **P3 Low** | Polish/optimization | Optional |

### Checks by Category

#### Syntax (P0)
- Parse errors, unclosed braces/brackets
- Invalid language constructs
- Malformed statements

#### Imports (P0)
- Missing library imports
- Unused imports
- Circular dependencies
- Wrong import paths

#### Variables (P0)
- Undefined variables
- Variable shadowing (inner scope redefines outer)
- Unused declared variables
- Reference before assignment

#### Type/Logic (P0-P1)
- Type mismatches (assigning wrong type)
- Obvious logic errors (dead code, unreachable branches)
- Null/undefined reference errors
- Off-by-one errors

#### Style (P2)
- Formatting inconsistency (indentation, spacing)
- Naming convention violations (camelCase vs snake_case, etc.)
- Line length exceeds detected standard
- Import order mismatch

#### Performance (P1-P2)
- N+1 query patterns (loops with DB calls)
- Inefficient algorithms (O(n²) where O(n) exists)
- Unnecessary memory allocations
- Missing indexes or caching

#### Security (P0-P1)
- SQL injection patterns (unparameterized queries)
- Hardcoded secrets/credentials
- Insecure cryptographic patterns
- Missing input validation
- Directory traversal vulnerabilities

---

## Report Structure

```
PULL REQUEST REVIEW REPORT
==========================

Executive Summary
─────────────────
Files Changed: 5
Total Issues Found: 12
  • P0 Critical: 2
  • P1 High: 3
  • P2 Medium: 4
  • P3 Low: 3
Overall Status: NEEDS_FIX (P0/P1 issues must be addressed)

Branch Info: feature/auth-flow → main
Latest check: [timestamp]

─────────────────────────────────────────

CRITICAL ISSUES (P0) - Must Fix
════════════════════════════════

[Issue 1]
File: src/auth/login.py:45
Issue: Undefined variable 'config'
Context:
    def authenticate(user):
        token = generate_token(config.secret)  # ← config not imported
        return token
Suggestion: Add import at top: from config import config
Confidence: High

[Issue 2]
File: src/database.py:12
Issue: Missing import 'sql'
Context:
    cursor.execute(sql_query)  # ← sql module not imported
Suggestion: Add: import sql
Confidence: High

─────────────────────────────────────────

HIGH PRIORITY ISSUES (P1) - Fix Before Merge
═════════════════════════════════════════════

[Issue 3]
File: src/auth/login.py:67
Issue: Type mismatch - expected str, got None
...

[Issue 4] 
File: src/utils/cache.py:22
Issue: Performance: N+1 query pattern
...

─────────────────────────────────────────

MEDIUM PRIORITY ISSUES (P2) - Consider Fixing
══════════════════════════════════════════════

[Style issues and performance improvements]

─────────────────────────────────────────

LOW PRIORITY ISSUES (P3) - Optional
════════════════════════════════════

[Polish and optimization suggestions]

─────────────────────────────────────────

DELEGATION QUEUE FOR RUG-ORCHESTRATOR
══════════════════════════════════════

Ready to delegate for fixes:

Task 1: src/auth/login.py - Add missing config import
Task 2: src/database.py - Add missing sql import
Task 3: src/auth/login.py - Fix type mismatch in token generation
Task 4: src/utils/cache.py - Refactor N+1 query pattern

Suggested prompt template for each:
─────────────────────────────────────
ISSUE: [Issue from report]
FILE: [file:line]
CONTEXT: [surrounding code]
SUGGESTED FIX: [recommendation]
ACCEPTANCE CRITERIA:
- [ ] Issue resolved
- [ ] No new issues introduced
- [ ] Code style matches codebase
```

---

## Integration with RUG Orchestrator

### Input from rug-orchestrator
```
TASK: Review PR from branch X to branch Y

PARAMETERS:
- source_branch: feature/user-auth
- target_branch: main
- repo_path: .
- files_to_review: [optional list or "all"]

ACCEPTANCE CRITERIA:
- [ ] Multi-layer analysis completed
- [ ] All findings classified by severity
- [ ] Report includes file:line references
- [ ] Delegation prompts ready for P0/P1 issues
```

### Output to rug-orchestrator
```
REVIEW COMPLETE

Report: [Full structured report as above]

Summary:
- Files changed: 5
- P0 Critical: 2 (must fix)
- P1 High: 3 (fix before merge)
- P2 Medium: 4 (consider)
- P3 Low: 3 (optional)

Delegation Queue:
1. src/auth/login.py:45 - Add missing config import
2. src/database.py:12 - Add missing sql import
3. src/auth/login.py:67 - Fix type mismatch
4. src/utils/cache.py:22 - Refactor N+1 query pattern

Next Steps: rug-orchestrator can:
- Delegate P0/P1 fixes to @plan-executor
- Re-run review after fixes to validate
- Continue with P2/P3 per user preference
```

### RUG Loop Integration
1. **Initial review** → pull-request-reviewer generates report
2. **Delegate fixes** → rug-orchestrator sends P0/P1 to @plan-executor
3. **Validate fixes** → run pull-request-reviewer again on fixed code
4. **Repeat** until all P0/P1 issues resolve or escalate

---

## Agent Boundaries

### Always ✅

- Pull from origin first (`git fetch origin`) to ensure latest code
- Check for GitLens MCP availability; use if present, fallback to git commands
- Auto-detect style conventions from ≥3 existing files in changed directories
- Provide file:line references for every finding with surrounding context
- Classify every issue with severity level (P0-P3)
- Prepare delegation prompts for P0/P1 findings with exact fix suggestions
- Run basic linters/type checkers if available in the repo (e.g., `mypy`, `eslint`)

### Ask First ⚠️

- Repository >100K LOC (agree on scope/timeout to avoid timeout)
- No style patterns detectable from codebase (ask for style guide reference)
- Ambiguous findings that could be interpreted multiple ways
- Breaking changes detected (confirm if intentional)

### Never ❌

- Modify code files (reviewer role only)
- Skip core checks (imports, undefined variables, obvious bugs are mandatory)
- Assume code style without examining codebase (always auto-detect)
- Report findings without evidence (file:line + context required)
- Delegate without severity classification
- Leave TODOs or placeholders in reports

---

## Success Criteria

- [x] Pulls latest code from origin before review
- [x] Detects and reports P0 critical issues (syntax, imports, undefined vars)
- [x] Detects and reports P1 high issues (type errors, obvious bugs, security)
- [x] Detects and reports P2/P3 issues (style, performance)
- [x] Auto-detects codebase style conventions
- [x] Every finding includes file:line reference + context
- [x] Issues classified by severity (P0-P3)
- [x] Delegation prompts prepared for rug-orchestrator
- [x] Fallback gracefully (GitLens → git diff → file reading)
- [x] Works language-agnostic (auto-detects by file extension)

---

## Implementation Notes

### Tools to Use
- `read` — read source files
- `search` — grep for imports, definitions, patterns
- `execute` — git fetch, git diff, run linters
- GitLens MCP (if available) — rich code context

### Language Support
- Auto-detect by file extension
- Python: check imports with `ast`, use `mypy` if available
- JavaScript/TypeScript: check with `eslint`, auto-detect style
- Go, Java, C++, etc.: use basic syntax checking + linters if present

### Performance Considerations
- Limit diff size (warn if >5000 lines changed)
- Use parallel checks where possible
- Cache style detection results
- Exit early if repo >100K LOC without user consent

---

## Related Documents

- `rug-orchestrator.agent.md` — orchestrator that delegates to this agent
- `plan-executor.agent.md` — agent that executes fixes from delegation queue
- `plan-reviewer.agent.md` — reference for review patterns
- `Implementing Orchestrator Agents.md` — delegation patterns

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-15 | Claude Code | Initial design approved |
