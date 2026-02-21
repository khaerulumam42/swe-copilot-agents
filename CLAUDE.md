# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Objective

This repository generates GitHub Copilot agents from source materials. Agents are defined in `agents.md` files with YAML frontmatter and custom instructions that define the agent's persona, tech stack, project structure, workflows, commands, and boundaries.

### Workflow

1. **Read source** from `copilot-agent-sources/` folder (contains source materials like blog posts, documentation)
2. **Generate agents** and save to `agents/` folder
3. **Human-in-the-loop**: Humans review and improve `agent.md` files based on real-world usage experience

### Key Concepts from Source Material

Effective agents.md files are **specific**, not vague. The best agents have:
- **Clear persona**: "QA software engineer who writes tests" not "helpful assistant"
- **Executable commands**: Put commands early with flags (`pytest -v`, `npm run build`)
- **Code examples**: Show good output style, don't just describe it
- **Clear boundaries**: What to always do, ask first, never do
- **Specific stack**: "React 18, TypeScript, Vite, Tailwind" not "React project"

### Six Core Areas for Every Agent

1. **Commands** - Executable commands with flags/options
2. **Testing** - How to run and validate tests
3. **Project structure** - Where files live and what they do
4. **Code style** - Examples showing good output
5. **Git workflow** - Commit patterns, branch strategies
6. **Boundaries** - Always do / Ask first / Never do

## Folder Structure

```
copilot-agent-sources/  # Source materials (blog posts, docs)
  └── github-blog.txt   # Source content about agents.md patterns

agents/                  # Generated agent.md files (create if doesn't exist)
  └── [agent-name].md   # Individual agent definitions

skills/                  # Additional tools (includes pdf-slides skill)
```

## Creating a New Agent

When creating an agent from source materials:

1. Read the relevant source file from `copilot-agent-sources/`
2. Extract the agent persona, commands, and best practices
3. Create a new agent file in `agents/[agent-name].md` with this structure:

```markdown
---
name: agent-name
description: One-sentence description
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

## Common Agent Types

- **@docs-agent** - Writes documentation from code
- **@test-agent** - Writes unit/integration tests
- **@lint-agent** - Fixes code style and formatting
- **@api-agent** - Builds API endpoints
- **@security-agent** - Analyzes code for security issues
- **@deploy-agent** - Handles builds and deployments

## Skills: PDF Slides Generator

The `skills/pdf-slides/` folder contains a separate skill for generating PDF slide decks from JSON outlines. This is independent of the agent generation workflow.

```bash
# Generate PDF from JSON outline
python skills/pdf-slides/skill.py outline.json -o output.pdf
```
