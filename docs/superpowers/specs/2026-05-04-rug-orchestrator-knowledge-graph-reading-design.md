# Rug-Orchestrator: Mandatory Knowledge Graph Reading

**Date:** 2026-05-04  
**Status:** Approved  
**Author:** Design session with user

## Overview

Enhance Phase 0.5 of the rug-orchestrator to make reading `knowledge-graph.yaml` a mandatory step. After verifying the knowledge graph exists and is current, the orchestrator will read it to extract function dependency relationships and pass relevant context to @plan-executor.

### Why This Matters

The knowledge-graph.yaml contains critical information about which functions call which other functions. By reading this upfront, the orchestrator can provide @plan-executor with dependency context, helping it understand the impact of changes (e.g., "Function X is called by Functions Y and Z").

### Key Principle

Keep Phase 0.5 workflow intact (check existence → create/update if needed → **NEW: read dependencies** → proceed to Phase 3). The orchestrator uses its `read` tool directly—no additional delegation needed.

## Phase 0.5 Enhancement

### Current Phase 0.5 Workflow

1. Check if knowledge-graph.yaml exists
2. If not: delegate to @knowledge-graph-agent to create it
3. If yes: check commit hash and update if stale
4. Proceed to Phase 3

### Enhanced Phase 0.5 Workflow

1. Check if knowledge-graph.yaml exists
2. If not: delegate to @knowledge-graph-agent to create it
3. If yes: check commit hash and update if stale
4. **NEW: Read knowledge-graph.yaml using the `read` tool**
5. **NEW: Extract and store dependency information for files in the plan**
6. Proceed to Phase 3 (with dependency context available)

### Specific Changes to Agent Instructions

After the existing knowledge-graph check completes, add:

```
[After @knowledge-graph-agent completes or confirms graph is up-to-date]

YOU: "Knowledge graph verified. Reading dependency relationships..."

[Use the read tool to read knowledge-graph.yaml]

YOU: "Dependency graph loaded. Found relationships for [N] functions across [M] files.
Key dependencies for planned work:
- [File/function from plan] → calls [dependencies]
- [File/function from plan] → called by [dependents]

Knowledge graph check complete. Proceeding to Phase 3."
```

The orchestrator will maintain awareness of dependencies relevant to the plan's scope, ready to include in task delegation prompts.

## Dependency Context Format

### What Gets Passed to @plan-executor

When delegating a task to @plan-executor, the orchestrator will include a new "DEPENDENCIES" section in the prompt with direct dependencies only:

```
[Use the agent tool to invoke plan-executor with this prompt:]

"CONTEXT: The user asked: '[original request from plan]'

YOUR TASK: [specific decomposed task]

SCOPE:
- Files to modify: [list]
- Files to create: [list]
- Files to NOT touch: [everything else]

DEPENDENCIES (from knowledge-graph.yaml):
For files/functions in this task:
- function_name in file.py
  → Calls: [list of functions this function calls]
  → Called by: [list of functions that call this function]
- another_function in other_file.py
  → Calls: [list]
  → Called by: [list]

REQUIREMENTS:
- [Requirement 1 from plan]
...
```

### Filtering Logic

- Only include dependencies for files explicitly mentioned in the task scope
- Show direct calls (one level deep) - not the full chain
- If a file has no dependencies in the graph, note: "No dependencies tracked for this file"

## Updated Phase 3 Delegation Template

The existing Phase 3 template (lines 209-241 in the current agent) will be enhanced with the DEPENDENCIES section:

```
YOU: "Task N/[total]: [task description]

Cueing @plan-executor for implementation..."

[Use the agent tool to invoke plan-executor with this prompt:]

"CONTEXT: The user asked: '[original request from plan]'

YOUR TASK: [specific decomposed task]

SCOPE:
- Files to modify: [list]
- Files to create: [list]
- Files to NOT touch: [everything else]

DEPENDENCIES (from knowledge-graph.yaml):
[If dependencies exist for files in scope:]
For files/functions in this task:
- function_name in file.py
  → Calls: [functions this calls]
  → Called by: [functions that call this]

[If no dependencies:]
No tracked dependencies for files in this task scope.

REQUIREMENTS:
- [Requirement 1 from plan]
- [Requirement 2 from plan]

ACCEPTANCE CRITERIA:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

SPECIFIED TECHNOLOGIES (non-negotiable):
- The user specified: [technology/library/framework from plan]
- You MUST use exactly these. Do NOT substitute alternatives.

CONSTRAINTS:
- Do NOT [constraint 1]
- Do NOT [constraint 2]

WHEN DONE: Report back with:
1. List of all files created/modified
2. Summary of changes made
3. Any issues or concerns
4. Confirmation that each acceptance criterion is met"
```

**Location of change:** Insert DEPENDENCIES section after SCOPE, before REQUIREMENTS.

## Error Handling

### What Happens If Reading knowledge-graph.yaml Fails

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

### Fail-Safe Principle

If the knowledge graph cannot be read, warn the user but continue orchestration. Dependencies are helpful context, not a blocker to implementation.

## Updated Boundaries

### Add to "Always Do" List

- ✅ **Read knowledge-graph.yaml in Phase 0.5** — extract dependencies for delegation context

### Add to "Never Do" List

- 🚫 **Skip reading knowledge-graph.yaml** — always attempt to read it after verification/update

## Implementation Changes

The following sections of `agents/rug-orchestrator.agent.md` need updates:

1. **Phase 0.5 (lines 105-146)**: Add reading step after verification/update
2. **Phase 3 template (lines 209-241)**: Add DEPENDENCIES section
3. **Boundaries - Always Do (line 449)**: Add knowledge-graph reading requirement
4. **Boundaries - Never Do (line 472)**: Add prohibition against skipping the read

## Success Criteria

- [ ] Phase 0.5 includes mandatory reading of knowledge-graph.yaml
- [ ] Dependency information is extracted and available for delegation
- [ ] Phase 3 @plan-executor prompts include DEPENDENCIES section
- [ ] Error handling gracefully degrades if reading fails
- [ ] Boundaries section reflects new requirements
- [ ] Agent behavior remains unchanged for projects without knowledge graphs
