# Implementing Orchestrator Agents

## Overview

This guide provides practical patterns and templates for implementing orchestrator agents that delegate work to subagents using the `runSubagent` tool.

---

## Core Tool: runSubagent

The `runSubagent` tool is the primary mechanism for delegation. It launches a subagent with a fresh context window to perform a specific task.

### Basic Syntax

```javascript
runSubagent({
  agent: "agent-name",
  prompt: "detailed task description",
  // Additional parameters vary by platform
})
```

### Key Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `agent` | Name of the subagent to invoke | Yes |
| `prompt` | Detailed task description with context | Yes |
| `context` | Additional context/data (varies by platform) | No |

---

## Pattern 1: Simple Delegation

Use for straightforward, single-step tasks.

```javascript
// Orchestrator
runSubagent({
  agent: "swe",
  prompt: `
CONTEXT: User wants to add user authentication to the app.

YOUR TASK: Implement login form with email/password validation.

SCOPE:
- Files to create: src/components/LoginForm.tsx
- Files to modify: src/App.tsx (add route)
- Files to NOT touch: Everything else

REQUIREMENTS:
- Use React Hook Form for form management
- Validate email format and password length (min 8)
- Show error messages for invalid inputs
- Call onSubmit callback with {email, password} on valid submit

ACCEPTANCE CRITERIA:
- [ ] Form renders with email and password fields
- [ ] Email validation rejects invalid formats
- [ ] Password validation rejects < 8 characters
- [ ] onSubmit called only with valid data

CONSTRAINTS:
- Do NOT add any authentication API calls
- Do NOT modify any existing components

WHEN DONE: Report back with:
1. Files created/modified
2. Summary of implementation
3. Any issues encountered
4. Confirmation of acceptance criteria
`
})
```

---

## Pattern 2: Decomposition + Parallel Delegation

Use for tasks with multiple independent parts.

```javascript
// Orchestrator
const tasks = [
  {
    id: "1",
    agent: "swe",
    task: "Create user schema with email, password, createdAt fields",
    files: ["src/models/User.ts"]
  },
  {
    id: "2",
    agent: "swe",
    task: "Create auth service with login, register, logout methods",
    files: ["src/services/authService.ts"]
  },
  {
    id: "3",
    agent: "swe",
    task: "Create auth context provider for React",
    files: ["src/contexts/AuthContext.tsx"]
  }
]

// Launch in parallel
await Promise.all(tasks.map(task =>
  runSubagent({
    agent: task.agent,
    prompt: buildPrompt(task)
  })
))
```

---

## Pattern 3: Sequential Delegation with Dependencies

Use when tasks depend on each other's output.

```javascript
// Orchestrator
async function buildFeature() {
  // Step 1: Research
  const research = await runSubagent({
    agent: "researcher",
    prompt: "Research best practices for JWT authentication in Node.js"
  })

  // Step 2: Plan (uses research output)
  const plan = await runSubagent({
    agent: "planner",
    prompt: `
Based on this research: ${research.output}

Create implementation plan for JWT auth with:
- User registration endpoint
- Login endpoint returning JWT
- Protected middleware for verifying tokens
`
  })

  // Step 3: Implement (uses plan)
  await runSubagent({
    agent: "implementer",
    prompt: `
Implement this plan: ${plan.output}

Follow the exact structure and steps outlined above.
`
  })

  // Step 4: Validate
  await runSubagent({
    agent: "qa",
    prompt: `
Validate the JWT implementation:
${plan.output}

Check for security issues, edge cases, and completeness.
`
  })
}
```

---

## Pattern 4: Retry Loop (RUG Style)

Repeat until validation passes.

```javascript
// Orchestrator
async function executeWithRetry(task, maxRetries = 3) {
  let retryCount = 0
  let lastResult = null
  let validationFailures = []

  while (retryCount < maxRetries) {
    // Do the work
    const result = await runSubagent({
      agent: "swe",
      prompt: buildPrompt(
        task,
        retryCount > 0 ? validationFailures : null
      )
    })

    // Validate the work
    const validation = await runSubagent({
      agent: "qa",
      prompt: buildValidationPrompt(task, result)
    })

    if (validation.verdict === "PASS") {
      return result
    }

    // Collect failures for retry
    validationFailures = validation.failures
    retryCount++
  }

  throw new Error(`Failed after ${maxRetries} retries`)
}
```

---

## Pattern 5: Wave-Based Execution (GEM Style)

Execute tasks in waves with integration checks.

```javascript
// Orchestrator
async function executeWaves(plan) {
  const waves = groupByWave(plan.tasks)

  for (const [waveNum, waveTasks] of Object.entries(waves)) {
    console.log(`Executing Wave ${waveNum}`)

    // Execute all tasks in wave
    const results = await Promise.all(
      waveTasks.map(task => runSubagent({
        agent: task.agent,
        prompt: buildPrompt(task)
      }))
    )

    // Integration check
    const integration = await runSubagent({
      agent: "reviewer",
      prompt: buildIntegrationPrompt(waveTasks, results)
    })

    if (integration.verdict !== "PASS") {
      // Fix and retry wave
      await fixAndRetryWave(waveTasks, integration.issues)
    }
  }
}
```

---

## Prompt Building Utilities

### Context Builder

```javascript
function buildContext(originalRequest, taskDefinition) {
  return `
CONTEXT: The user asked: "${originalRequest}"

YOUR TASK: ${taskDefinition.what}

SCOPE:
- Files to modify: ${taskDefinition.modifyFiles.join(", ")}
- Files to create: ${taskDefinition.createFiles.join(", ")}
- Files to NOT touch: ${taskDefinition.excludeFiles.join(", ")}

REQUIREMENTS:
${taskDefinition.requirements.map(r => `- ${r}`).join("\n")}
`
}
```

### Acceptance Criteria Builder

```javascript
function buildAcceptanceCriteria(criteria) {
  return `
ACCEPTANCE CRITERIA:
${criteria.map(c => `- [ ] ${c}`).join("\n")}

You MUST confirm each criterion is met in your report.
`
}
```

### Specification Builder

```javascript
function buildSpecifications(specs) {
  return `
SPECIFIED TECHNOLOGIES (non-negotiable):
${specs.map(s => `- The user specified: ${s}`).join("\n")}
- You MUST use exactly these. Do NOT substitute alternatives.

CONSTRAINTS:
${specs.map(s => `- Do NOT use any alternative to ${s}`).join("\n")}
`
}
```

### Validation Prompt Builder

```javascript
function buildValidationPrompt(task, workResult) {
  return `
A previous agent was asked to: ${task.description}

The acceptance criteria were:
${task.acceptanceCriteria.map(c => `- ${c}`).join("\n")}

VALIDATE the work by:
1. Reading the files that were supposedly modified/created
2. Checking that each acceptance criterion is actually met
3. SPECIFICATION COMPLIANCE CHECK: Verify the implementation uses ${task.specifications.join(", ")}
4. Looking for bugs, missing edge cases, or incomplete implementations
5. Running any relevant tests or type checks

REPORT:
- SPECIFICATION COMPLIANCE: For each specified technology, confirm it is used or FAIL
- For each acceptance criterion: PASS or FAIL with evidence
- List any bugs or issues found
- Overall verdict: PASS or FAIL
`
}
```

---

## Result Routing Pattern

```javascript
// Orchestrator
function routeResult(result) {
  switch (result.status) {
    case "completed":
      if (result.extra?.test_results?.failed > 0) {
        return "needs_revision"
      }
      return "done"

    case "needs_revision":
      return diagnoseAndRetry(result)

    case "failed":
      if (result.failure_type === "escalate") {
        return "escalate"
      }
      if (result.failure_type === "needs_replan") {
        return "replan"
      }
      return diagnoseAndRetry(result)

    case "needs_approval":
      return presentToUser(result)

    default:
      return "unknown"
  }
}

async function diagnoseAndRetry(failedResult) {
  const diagnosis = await runSubagent({
    agent: "debugger",
    prompt: buildDiagnosisPrompt(failedResult)
  })

  if (diagnosis.confidence < 0.7) {
    return "escalate"
  }

  // Retry with diagnosis
  const fixAgent = diagnosis.fix_type === "code" ? "implementer" : "original"
  await runSubagent({
    agent: fixAgent,
    prompt: buildFixPrompt(failedResult, diagnosis)
  })

  return "retrying"
}
```

---

## Todo List Management

```javascript
// Orchestrator
async function executeWithTracking(tasks) {
  // Create initial todo list
  const todoList = tasks.map(task => ({
    id: task.id,
    description: task.description,
    status: "pending"
  }))

  for (const task of tasks) {
    // Mark in-progress
    updateTodo(todoList, task.id, "in_progress")

    // Execute
    const result = await runSubagent({
      agent: task.agent,
      prompt: buildPrompt(task)
    })

    // Validate
    const validation = await runSubagent({
      agent: "qa",
      prompt: buildValidationPrompt(task, result)
    })

    // Mark complete or retry
    if (validation.verdict === "PASS") {
      updateTodo(todoList, task.id, "completed")
    } else {
      updateTodo(todoList, task.id, "retrying")
      // Retry logic...
    }
  }
}
```

---

## Anti-Patterns to Avoid

### Don't: Do Work Yourself

```javascript
// BAD
const fileContent = await readFile("src/app.ts")
const analysis = analyzeFile(fileContent)

// GOOD
const analysis = await runSubagent({
  agent: "analyzer",
  prompt: "Read src/app.ts and report its structure and exports"
})
```

### Don't: Skip Validation

```javascript
// BAD
const result = await runSubagent({ agent: "swe", prompt: task })
if (result.status === "completed") {
  markDone()
}

// GOOD
const result = await runSubagent({ agent: "swe", prompt: task })
const validation = await runSubagent({
  agent: "qa",
  prompt: buildValidationPrompt(task, result)
})
if (validation.verdict === "PASS") {
  markDone()
}
```

### Don't: Give Up After One Failure

```javascript
// BAD
try {
  await runSubagent({ agent: "swe", prompt: task })
} catch (e) {
  return { status: "failed", message: "Task failed" }
}

// GOOD
let attempts = 0
while (attempts < 3) {
  const result = await runSubagent({ agent: "swe", prompt: task })
  const validation = await runSubagent({
    agent: "qa",
    prompt: buildValidationPrompt(task, result)
  })

  if (validation.verdict === "PASS") break

  // Improve prompt for retry
  task.prompt = addFailureContext(task.prompt, validation.failures)
  attempts++
}
```

---

## Checklist: Building an Orchestrator

- [ ] Define clear subagent roles and capabilities
- [ ] Implement task decomposition logic
- [ ] Build prompt templates with all required sections
- [ ] Add validation subagent for every work subagent
- [ ] Implement retry loop with failure context injection
- [ ] Add todo list management for tracking
- [ ] Handle specification adherence (negative constraints)
- [ ] Implement result routing based on status
- [ ] Add escalation logic for unrecoverable failures
- [ ] Test with various task complexities

---

## Related Files

- `Subagent Orchestration Patterns.md` — Pattern reference
- `RUG - Deep Dive.md` — RUG orchestrator details
- `source/awesome-copilot/agents/rug-orchestrator.agent.md` — RUG implementation
- `source/awesome-copilot/agents/gem-orchestrator.agent.md` — GEM implementation
