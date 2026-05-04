# Rug-Orchestrator Knowledge Graph Reading Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enhance rug-orchestrator agent to read knowledge-graph.yaml and pass dependency context to @plan-executor

**Architecture:** Add mandatory reading step to Phase 0.5, extract direct dependencies, include them in Phase 3 @plan-executor delegation prompts. Single-file update with four distinct sections.

**Tech Stack:** Markdown (agent configuration file)

---

## File Structure

**Modified:**
- `agents/rug-orchestrator.agent.md` - Four sections updated:
  - Phase 0.5 (lines 105-146): Add reading step after verification/update
  - Phase 3 template (lines 209-241): Add DEPENDENCIES section  
  - Boundaries - Always Do (around line 449): Add knowledge-graph reading requirement
  - Boundaries - Never Do (around line 472): Add prohibition against skipping

---

### Task 1: Update Phase 0.5 - Add Knowledge Graph Reading Step

**Files:**
- Modify: `agents/rug-orchestrator.agent.md:105-146`

- [ ] **Step 1: Read current Phase 0.5 section**

Read lines 105-146 to understand current structure.

Expected: Phase 0.5 ends with "YOU: 'Knowledge graph check complete. Proceeding to Phase 3.'"

- [ ] **Step 2: Add reading step after verification**

After line 143 (where @knowledge-graph-agent confirms graph is up-to-date), insert the following content before the final "Knowledge graph check complete" message:

```markdown
[After @knowledge-graph-agent completes or confirms graph is up-to-date]

YOU: "Knowledge graph verified. Reading dependency relationships..."

[Use the read tool to read knowledge-graph.yaml]

YOU: "Dependency graph loaded. Found relationships for [N] functions across [M] files.
Key dependencies for planned work:
- [File/function from plan] → calls [dependencies]
- [File/function from plan] → called by [dependents]

Knowledge graph check complete. Proceeding to Phase 3."
```

The exact edit location is after the existing knowledge-graph-agent delegation completes, replacing the simple "Knowledge graph check complete" message with the enhanced version that includes reading.

- [ ] **Step 3: Add error handling for read failures**

After the reading step added in Step 2, insert error handling guidance:

```markdown

**If reading knowledge-graph.yaml fails:**

```
[If the read tool fails or file is corrupted]

YOU: "Warning: Could not read knowledge-graph.yaml successfully.
Error: [error message]

Attempting to regenerate via @knowledge-graph-agent..."

[Delegate to @knowledge-graph-agent to recreate the file]

[If regeneration succeeds]
YOU: "Knowledge graph regenerated successfully. Proceeding with Phase 3."

[If regeneration also fails]
YOU: "Unable to load dependency graph after regeneration attempt.
Proceeding WITHOUT dependency context - @plan-executor will work without this information.
Manual review recommended after implementation."
```
```

- [ ] **Step 4: Verify Phase 0.5 update**

Read the updated Phase 0.5 section and confirm:
- Reading step appears after verification/update
- Error handling is included
- Flow still ends with "Proceeding to Phase 3"

- [ ] **Step 5: Commit Phase 0.5 changes**

```bash
git add agents/rug-orchestrator.agent.md
git commit -m "feat(rug-orchestrator): add knowledge-graph.yaml reading to Phase 0.5"
```

---

### Task 2: Update Phase 3 Template - Add DEPENDENCIES Section

**Files:**
- Modify: `agents/rug-orchestrator.agent.md:209-241`

- [ ] **Step 1: Read current Phase 3 template**

Read lines 209-241 to locate the @plan-executor delegation prompt template.

Expected: Template has SCOPE section followed by REQUIREMENTS section.

- [ ] **Step 2: Insert DEPENDENCIES section**

Between the SCOPE section and REQUIREMENTS section, add:

```markdown
DEPENDENCIES (from knowledge-graph.yaml):
[If dependencies exist for files in scope:]
For files/functions in this task:
- function_name in file.py
  → Calls: [functions this calls]
  → Called by: [functions that call this]

[If no dependencies:]
No tracked dependencies for files in this task scope.
```

The exact location is after:
```
SCOPE:
- Files to modify: [list]
- Files to create: [list]
- Files to NOT touch: [everything else]
```

And before:
```
REQUIREMENTS:
- [Requirement 1 from plan]
- [Requirement 2 from plan]
```

- [ ] **Step 3: Verify template structure**

Read the updated Phase 3 template and confirm the order is:
1. CONTEXT
2. YOUR TASK
3. SCOPE
4. **DEPENDENCIES** (new)
5. REQUIREMENTS
6. ACCEPTANCE CRITERIA
7. SPECIFIED TECHNOLOGIES
8. CONSTRAINTS
9. WHEN DONE

- [ ] **Step 4: Commit Phase 3 template changes**

```bash
git add agents/rug-orchestrator.agent.md
git commit -m "feat(rug-orchestrator): add DEPENDENCIES section to Phase 3 template"
```

---

### Task 3: Update Boundaries - Add New Requirements

**Files:**
- Modify: `agents/rug-orchestrator.agent.md:445-477`

- [ ] **Step 1: Read current Boundaries section**

Read the "Boundaries" section starting around line 445.

Expected: Two subsections - "Always Do" and "Never Do"

- [ ] **Step 2: Add to "Always Do" list**

In the "Always Do (RUG Principles)" subsection (around line 449), add this item after the existing knowledge-graph check item:

```markdown
- **Read knowledge-graph.yaml in Phase 0.5** — extract dependencies for delegation context
```

Insert it after the existing line:
```markdown
- **Check knowledge-graph.yaml before Phase 3** — ensure codebase map is current (delegate to @knowledge-graph-agent)
```

- [ ] **Step 3: Add to "Never Do" list**

In the "Never Do (Breaking RUG Pattern)" subsection (around line 472), add this item after the existing knowledge-graph check item:

```markdown
- **Skip reading knowledge-graph.yaml** — always attempt to read it after verification/update
```

Insert it after the existing line:
```markdown
- **Skip knowledge-graph check** — always verify/update before Phase 3 implementation
```

- [ ] **Step 4: Verify boundaries updates**

Read both subsections and confirm:
- "Always Do" includes reading knowledge-graph.yaml
- "Never Do" includes prohibition against skipping the read
- Items are in logical positions near related boundaries

- [ ] **Step 5: Commit boundaries changes**

```bash
git add agents/rug-orchestrator.agent.md
git commit -m "feat(rug-orchestrator): add knowledge-graph reading to boundaries"
```

---

### Task 4: Final Verification and Documentation

**Files:**
- Read: `agents/rug-orchestrator.agent.md` (full file)
- Read: `docs/superpowers/specs/2026-05-04-rug-orchestrator-knowledge-graph-reading-design.md`

- [ ] **Step 1: Verify all spec requirements**

Check each requirement from the spec:
- ✅ Phase 0.5 includes mandatory reading of knowledge-graph.yaml
- ✅ Dependency information is extracted and available for delegation
- ✅ Phase 3 @plan-executor prompts include DEPENDENCIES section
- ✅ Error handling gracefully degrades if reading fails
- ✅ Boundaries section reflects new requirements

- [ ] **Step 2: Check for consistency**

Read the full agent file and verify:
- Phase 0.5 reading step matches Phase 3 DEPENDENCIES section format
- Error handling is complete and matches fail-safe principle
- No contradictions between sections
- Terminology is consistent throughout

- [ ] **Step 3: Verify no placeholders**

Search for common placeholders in the updated sections:
- No "TBD" or "TODO" markers
- Template placeholders ([N], [list], etc.) are intentional and documented
- All instructions are complete and actionable

- [ ] **Step 4: Create final commit**

```bash
git add agents/rug-orchestrator.agent.md
git commit -m "feat(rug-orchestrator): implement mandatory knowledge-graph reading

- Add reading step to Phase 0.5 after verification/update
- Extract dependency relationships for delegation context
- Include DEPENDENCIES section in Phase 3 @plan-executor prompts
- Add error handling with graceful degradation
- Update boundaries to reflect new requirements

Implements: docs/superpowers/specs/2026-05-04-rug-orchestrator-knowledge-graph-reading-design.md

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

- [ ] **Step 5: Verify git history**

```bash
git log --oneline -5
```

Expected: See all 4 commits from this implementation:
1. Phase 0.5 update
2. Phase 3 template update
3. Boundaries update
4. Final consolidated commit (if previous commits were squashed)

---

## Success Criteria

All tasks completed when:
- [ ] Phase 0.5 reads knowledge-graph.yaml after verification/update
- [ ] Error handling degrades gracefully if reading fails
- [ ] Phase 3 template includes DEPENDENCIES section between SCOPE and REQUIREMENTS
- [ ] Boundaries section includes reading requirement in "Always Do"
- [ ] Boundaries section includes skip prohibition in "Never Do"
- [ ] All changes committed with clear messages
- [ ] No placeholders or incomplete sections remain
