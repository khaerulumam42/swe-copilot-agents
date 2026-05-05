# swe-copilot-agents

A collection of GitHub Copilot custom agents for the complete software development lifecycle — from planning through implementation, testing, and documentation.

## Installation

```bash
pip install swe-copilot-agents
```

Then install agents into your project:

```bash
cd /path/to/your/project
swe-copilot-agents
```

This copies 7 `.agent.md` files to `.github/agents/` in your project:

```
✓ rug-orchestrator.agent.md
✓ brainstormer.agent.md
✓ plan-executor.agent.md
✓ plan-reviewer.agent.md
✓ pytest-agent.agent.md
✓ knowledge-graph-agent.agent.md
✓ readme-generator.agent.md
```

## Agents

| Agent | Role |
|-------|------|
| `@rug-orchestrator` | Orchestrates the full dev cycle using the RUG (Repeat Until Good) pattern |
| `@brainstormer` | Asks clarifying questions and writes detailed implementation plans |
| `@plan-executor` | Implements plans by matching your codebase's existing style |
| `@plan-reviewer` | Audits implementation against the plan — evidence-driven |
| `@pytest-agent` | Writes exhaustive pytest suites with expert-level mocking |
| `@knowledge-graph-agent` | Builds a `knowledge-graph.yaml` map of your codebase |
| `@readme-generator` | Generates and updates README from the knowledge graph |

See [docs/AGENTS.md](docs/AGENTS.md) for full details on each agent.

## Usage

Start with the orchestrator for end-to-end workflow:

```
@rug-orchestrator
I want to add a user authentication system with JWT tokens
```

Or invoke agents directly:

```
@brainstormer
I need to add a search feature to my application

@plan-reviewer
Review the implementation against docs/plan/2025-03-02-auth.md
```

## How it works

```
User Request
      ↓
@rug-orchestrator (Pure Delegator)
      │
      ├─ Phase 1: @brainstormer → Plan document
      │           ↓ Human Approval
      ├─ Phase 2: @plan-executor → Implementation (per task)
      ├─ Phase 3: @plan-reviewer → Validate
      │           ├─ FAIL → Retry @plan-executor (up to 3×)
      │           └─ PASS → Continue
      └─ Phase 4: @pytest-agent → Tests (optional)
```

Each task is validated before moving on. Failed tasks are retried up to 3 times, then escalated to the human.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
