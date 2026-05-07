# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Objective

This repository generates GitHub Copilot agents from source materials. Agents are defined in `.agent.md` files with YAML frontmatter and custom instructions that define the agent's persona, tech stack, project structure, workflows, commands, and boundaries.

### Workflow

1. **Read source** from `copilot-agent-sources/` folder (contains source materials like blog posts, documentation)
2. **Generate agents** and save to `agents/` folder
3. **Human-in-the-loop**: Humans review and improve `agent.md` files based on real-world usage experience

### Key Concepts from Source Material

Effective agent.md files are **specific**, not vague. The best agents have:
- **Clear persona**: "QA software engineer who writes tests" not "helpful assistant"
- **Executable commands**: Put commands early with flags (`pytest -v`, `npm run build`)
- **Code examples**: Show good output style, don't just describe it
- **Clear boundaries**: What to always do, ask first, never do
- **Specific stack**: "React 18, TypeScript, Vite, Tailwind" not "React project"

### Agent File Structure

GitHub Copilot agents use the `.agent.md` file extension with YAML frontmatter:

```yaml
---
name: agent-name              # Optional: defaults to filename
description: Required description of agent's purpose
target: vscode | github-copilot  # Optional: defaults to both
tools: ["read", "edit", "search"]  # Optional: omit for all tools
disable-model-invocation: false   # Optional: manual selection only
---
```

#### YAML Frontmatter Properties

| Property | Type | Required | Purpose |
|----------|------|----------|---------|
| `name` | string | No | Display name (defaults to filename) |
| `description` | string | **Yes** | Agent's purpose and capabilities |
| `target` | string | No | `vscode` or `github-copilot` (both if omitted) |
| `tools` | list | No | Tool names to enable (all if omitted) |
| `disable-model-invocation` | boolean | No | Require manual selection if `true` |
| `mcp-servers` | object | No | MCP server configs (org/enterprise only) |
| `metadata` | object | No | Key-value annotation pairs |

#### Tool Aliases

| Primary | Compatible aliases | Purpose |
|---------|-------------------|---------|
| `execute` | `shell`, `Bash`, `powershell` | Run shell commands |
| `read` | `Read`, `NotebookRead` | Read file contents |
| `edit` | `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | Edit files |
| `search` | `Grep`, `Glob` | Search files/text |
| `agent` | `custom-agent`, `Task` | Invoke other agents |
| `web` | `WebSearch`, `WebFetch` | Web search/fetch |
| `todo` | `TodoWrite` | Manage task lists |

### Agent Naming

- Filename (without `.agent.md`) used as default `name` if not specified
- Only these characters allowed: `.`, `-`, `_`, `a-z`, `A-Z`, `0-9`
- For org/enterprise: place in root `agents/` directory (not `.github/agents/`)

### Agent Versioning

- Based on Git commit SHAs of the agent profile file
- Branches/tags can have different agent versions
- PRs use consistent agent version throughout

## Folder Structure

```
copilot-agent-sources/  # Source materials (blog posts, docs)
  ├── github-blog.txt              # Original patterns source
  ├── create-custom-agent.md       # How to create agents
  └── custom-agents-configuration.md  # YAML configuration reference

agents/                  # Generated .agent.md files
  └── [agent-name].agent.md   # Individual agent definitions

skills/                  # Additional tools
```

## Creating a New Agent

When creating an agent from source materials:

1. Read the relevant source file from `copilot-agent-sources/`
2. Extract the agent persona, commands, and best practices
3. Create a new agent file in `agents/[agent-name].agent.md` with this structure:

```markdown
---
name: agent-name
description: One-sentence description of agent's purpose and capabilities
---

You are an expert [role] for this project.

## Persona
- You specialize in [specific task]
- Your output: [what you produce]

## Project knowledge
- **Tech Stack:** [technologies with versions]
- **File Structure:**
  - `src/` – [description]
  - `tests/` – [description]

## Tools you can use
- **Build:** `command` (description)
- **Test:** `command` (description)

## Standards
[Code style examples, naming conventions]

## Boundaries
- ✅ **Always:** [what to do]
- ⚠️ **Ask first:** [what requires approval]
- 🚫 **Never:** [what to avoid]
```

4. Have a human review and refine based on actual usage

## Human-in-the-Loop Process

After using an agent:
1. Note what worked well and what didn't
2. Update the agent.md file with:
   - Missing commands that were needed
   - New boundaries based on mistakes
   - Better examples from successful interactions
3. The agent.md file evolves through real-world iteration

## PyPI Release Workflow

When releasing a new version to PyPI:

```bash
# 1. Check the latest version from git tags
git fetch --tags
git tag --list | tail -1

# 2. Bump the minor version (e.g., 0.1.5 -> 0.1.6)
# Update pyproject.toml version field

# 3. Commit the version bump
git add pyproject.toml
git commit -m "Bump version to 0.1.6 for PyPI release"

# 4. Push to master
git push origin master

# 5. Create and push tag
git tag v0.1.6 -m "Bump version to 0.1.6 for PyPI release"
git push origin v0.1.6

# 6. Build the wheel
rm -rf dist/ build/
python3 -m build

# 7. Upload to PyPI
python3 -m twine upload dist/swe_copilot_agents-*.whl
```

**Important Notes:**
- Always check if the version already exists on PyPI before uploading
- Use `python3 -m twine check dist/*` to validate package metadata
- PyPI rejects duplicate versions (400 Bad Request)
- The wheel file includes all agent files from the current source code

## Common Agent Types

- **@docs-agent** - Writes documentation from code
- **@test-agent** - Writes unit/integration/tests
- **@lint-agent** - Fixes code style and formatting
- **@api-agent** - Builds API endpoints
- **@security-agent** - Analyzes code for security issues
- **@deploy-agent** - Handles builds and deployments
- **@planner-agent** - Creates implementation plans (read/search/edit only)

## Additional Resources

- [awesome-copilot community collection](https://github.com/github/awesome-copilot/tree/main/agents)
- [Custom agents tutorials](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
