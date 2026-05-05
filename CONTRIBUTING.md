# Contributing to Awesome Skills

Thank you for your interest in contributing! This project is maintained by [@khaerulumam42](https://github.com/khaerulumam42). All contributions go through pull requests — direct pushes to `master` are restricted to the maintainer.

## How to Contribute

### 1. Fork and Clone

```bash
# Fork via GitHub UI, then clone your fork
git clone https://github.com/<your-username>/agent-generator.git
cd agent-generator
pip install -e .
```

### 2. Create a Branch

```bash
git checkout -b feat/your-agent-name
```

### 3. Make Your Changes

See the sections below for what types of contributions are welcome.

### 4. Open a Pull Request

Push to your fork and open a PR against `master`. Describe:
- What the agent/change does
- Why it's useful
- Any usage example or screenshot

---

## Types of Contributions

### Adding a New Agent

New agents must follow the standard `.agent.md` structure. Place your file in `agents/`:

```markdown
---
name: agent-name
description: One-sentence description of agent's purpose and capabilities
tools: ["read", "edit", "search"]
---

You are an expert [role] for this project.

## Persona
- You specialize in [specific task]
- Your output: [what you produce]

## Project Knowledge
- **Tech Stack:** [technologies with versions]

## Commands
- **Build:** `command --flag` (description)

## Boundaries
- ✅ **Always:** [what to always do]
- ⚠️ **Ask first:** [what requires approval]
- 🚫 **Never:** [what to avoid]
```

**Checklist before submitting an agent PR:**

- [ ] Has a clear, specific persona (not "helpful assistant")
- [ ] Includes executable commands with flags
- [ ] Has explicit boundaries (always / ask first / never)
- [ ] `description` field is one sentence and specific
- [ ] Tested in VS Code GitHub Copilot Chat at least once

### Improving an Existing Agent

If you found a gap, a missing command, or a boundary violation while using an agent in production — that feedback is the most valuable contribution. Open a PR with:

- What went wrong or was missing
- The specific change to the `.agent.md` file

### Bug Reports

Open a [GitHub Issue](https://github.com/khaerulumam42/agent-generator/issues) with:

- Which agent you were using
- What you asked it to do
- What it did instead
- Your VS Code + GitHub Copilot version

---

## Agent Quality Standards

| Criteria | Requirement |
|----------|-------------|
| Persona | Distinctive role and philosophy |
| Commands | Concrete bash commands, not vague descriptions |
| Boundaries | At least one each of always / ask first / never |
| Description | One sentence, specific enough to distinguish from other agents |
| Tools | Only list tools the agent actually needs |

---

## Project Setup

```bash
# Install in editable mode
pip install -e .

# Install agents to a test project
cd /path/to/test-project
swe-copilot-agents

# Validate package metadata before release
python3 -m twine check dist/*
```

---

## What Is Not Accepted

- Agents that duplicate the role of an existing agent without clear differentiation
- Changes that break the existing agent file structure
- PRs that modify `master` branch protection or CI configuration without prior discussion
- Direct commits — all changes must go through a PR

---

## License

By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
