# VS Code Setup for Orchestrator Agents

## Overview

This guide shows how to set up and use orchestrator agents (like RUG and GEM) in VS Code with GitHub Copilot.

## Prerequisites

1. **GitHub Copilot in VS Code**
   - Install the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
   - Sign in with your GitHub account
   - Ensure you have Copilot access

2. **GitHub Copilot CLI** (for agent development)
   ```bash
   # Install via npm
   npm install -g @githubcopilot/copilot-cli

   # Or via homebrew (macOS)
   brew install github/copilot-cli/copilot-cli
   ```

---

## Understanding the Agent System

### Agent File Structure

Every agent file (`*.agent.md`) has this structure:

```markdown
---
name: 'AgentName'
description: 'What this agent does'
tools: ['tool1', 'tool2', 'runSubagent']
agents: ['Subagent1', 'Subagent2']  # Available subagents
model: 'claude-opus-4-6'  # Optional: specify model
---

# Agent instructions here...
```

### Key Fields for Orchestration

| Field | Purpose |
|-------|---------|
| `agents` | Lists which subagents this orchestrator can call |
| `tools` | Must include `runSubagent` for delegation |
| `name` | Used when invoking via `/agent` command |

---

## Setup Options

### Option 1: Use Existing Awesome-Copilot Agents

1. **Clone the repository**
   ```bash
   git clone https://github.com/github/awesome-copilot.git
   cd awesome-copilot
   ```

2. **Install dependencies**
   ```bash
   npm ci
   npm run build
   ```

3. **Register the marketplace** (one-time)
   ```bash
   copilot plugin marketplace add github/awesome-copilot
   ```

4. **Install a plugin containing orchestrator agents**
   ```bash
   # List available plugins
   copilot plugin search --marketplace github/awesome-copilot

   # Install a plugin
   copilot plugin install <plugin-name>@awesome-copilot
   ```

5. **Use in VS Code**
   - Open Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Type: "Copilot: Start Agent Chat"
   - Select the agent you want to use

---

### Option 2: Create Custom Orchestrator Agent

1. **Create agent file in your project**

   Create `.github/agents/my-orchestrator.agent.md`:

   ```markdown
   ---
   name: 'my-orchestrator'
   description: 'My custom orchestrator that delegates to subagents'
   tools: ['runSubagent', 'manage_todo_list']
   agents: ['swe', 'qa']
   ---

   # My Orchestrator

   You are a pure orchestrator. NEVER do implementation work yourself.

   ## Cardinal Rule

   EVERY piece of work MUST be delegated to a subagent using `runSubagent`.

   ## Workflow

   1. Decompose the user's request into tasks
   2. For each task:
      - Launch work subagent with detailed prompt
      - Launch validation subagent to verify
      - If validation fails, retry with failure context
   3. Return results when all tasks pass validation
   ```

2. **Create subagent files**

   `.github/agents/swe.agent.md`:
   ```markdown
   ---
   name: 'swe'
   description: 'Senior software engineer for implementation'
   tools: ['edit', 'read', 'search', 'execute']
   ---

   You are a senior software engineer. Implement the task according to specifications.
   ```

   `.github/agents/qa.agent.md`:
   ```markdown
   ---
   name: 'qa'
   description: 'QA engineer for validation'
   tools: ['read', 'search', 'execute']
   ---

   You are a QA engineer. Validate that work meets all acceptance criteria.
   ```

3. **Restart VS Code** to load the new agents

4. **Use your orchestrator**
   - Command Palette → "Copilot: Start Agent Chat"
   - Select "my-orchestrator"
   - Give it a task

---

## Using Agents in VS Code

### Method 1: Command Palette

1. `Cmd+Shift+P` → "Copilot: Start Agent Chat"
2. Select your agent
3. Type your request

### Method 2: Inline Chat

1. Right-click in code editor
2. Select "Copilot: Start Agent Chat"
3. Select your agent
4. Type your request

### Method 3: Quick Chat

1. `Cmd+Shift+A` (Mac) or `Ctrl+Shift+A` (Windows/Linux)
2. Type `/agent <agent-name>` to switch to a specific agent
3. Type your request

---

## Project Structure for Custom Agents

```
your-project/
├── .github/
│   └── agents/
│       ├── my-orchestrator.agent.md
│       ├── swe.agent.md
│       └── qa.agent.md
├── .vscode/
│   └── settings.json
└── src/
```

---

## VS Code Settings

Add to `.vscode/settings.json` for better agent development:

```json
{
  "files.associations": {
    "*.agent.md": "chatagent"
  },
  "github.copilot.enable": {
    "*": true
  }
}
```

---

## Testing Your Orchestrator

1. **Create a simple test task**

   Ask your orchestrator: "Create a function that adds two numbers"

2. **Verify delegation**

   The orchestrator should:
   - NOT write the code itself
   - Launch the `swe` subagent
   - Launch the `qa` subagent to validate
   - Return results only after validation passes

3. **Check the Copilot panel**

   - Open the Copilot Chat panel
   - You should see the delegation chain:
     ```
     [my-orchestrator] Launching subagent: swe
     [swe] Creating add function...
     [my-orchestrator] Launching subagent: qa
     [qa] Validating implementation...
     [my-orchestrator] Task completed successfully
     ```

---

## Troubleshooting

### Agent Not Showing Up

1. Check file location: Must be in `.github/agents/`
2. Check file name: Must end in `.agent.md`
3. Check frontmatter: Must have `name` and `description`
4. Restart VS Code

### Subagent Not Found

1. Check `agents` field in orchestrator frontmatter
2. Verify subagent file exists in `.github/agents/`
3. Check subagent file name matches (case-insensitive)

### Delegation Not Working

1. Verify `runSubagent` is in `tools` field
2. Check that subagent names match exactly
3. Look for error messages in Copilot output panel

---

## Advanced: MCP Servers

Orchestrators can integrate with MCP (Model Context Protocol) servers for additional capabilities:

### Example MCP Configuration

`.vscode/mcp.json`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

### Using MCP in Agents

Add MCP tools to agent frontmatter:
```markdown
---
tools: ['runSubagent', 'filesystem/read_file', 'github/search_repos']
---
```

---

## Quick Reference: Agent Frontmatter

```markdown
---
name: 'agent-name'              # Required: How you invoke the agent
description: 'What it does'     # Required: Short description
tools: ['runSubagent']           # Required: Tools this agent can use
agents: ['subagent1', 'sub2']   # For orchestrators: Available subagents
model: 'claude-opus-4-6'        # Optional: Which model to use
user-invocable: true            # Optional: Can users invoke directly?
---
```

---

## Related Resources

- [GitHub Copilot Agents Documentation](https://docs.github.com/en/copilot)
- [Awesome Copilot Website](https://awesome-copilot.github.com)
- [Agent Documentation](../Subagent%20Orchestration%20Patterns.md)
- [RUG Deep Dive](../RUG%20-%20Deep%20Dive.md)
- [Implementing Orchestrators](../Implementing%20Orchestrator%20Agents.md)
