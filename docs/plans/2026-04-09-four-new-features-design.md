# Design: Four New Features

**Date:** 2026-04-09
**Status:** Approved
**Author:** @brainstormer

## Overview

Add 2 new agents and modify 2 existing agents to expand the GitHub Copilot agent collection:
1. New `readme-generator` agent for README generation/update from knowledge-graph.yaml
2. Add `todo` tool to existing `plan-executor` agent
3. Modify existing `brainstormer` agent with Decision Helper mode
4. New `infra-setup` agent for AWS Fargate + Terraform infra generation from knowledge-graph.yaml

## Feature 1: README Generator Agent

### Purpose
Auto-generate or update README.md based on knowledge-graph.yaml data.

### Behavior
- **No README exists:** Generates full README using KG data
  - Project name, description from metadata
  - Tech stack from languages
  - File structure from files section
  - Installation instructions from external_dependencies
  - Entry points documentation
- **README exists:** Updates KG-derived sections (marked with `<!-- KG:SECTION_NAME -->` comments)
  - Preserves all manual sections
  - Updates: tech stack, file structure, dependencies, entry points

### Tools
- `read`, `edit`, `search`, `execute`

### Key KG Sections Used
- `metadata` — project name, languages, scan date
- `entry_points` — how to run/use the project
- `files` — project structure
- `external_dependencies` — installation requirements
- `concerns` — security/auth notes

### File: `agents/readme-generator.agent.md`

## Feature 2: Todo Tool in Plan-Executor

### Purpose
Allow plan-executor to manage task lists during execution.

### Change
- Add `"todo"` to the `tools` list in plan-executor's YAML frontmatter
- Current: `tools: ["read", "edit", "search", "execute"]`
- New: `tools: ["read", "edit", "search", "execute", "todo"]`

### File: `agents/plan-executor.agent.md`

## Feature 3: Brainstormer Decision Helper Mode

### Purpose
Add explicit options/recommendation mode to brainstormer for decision-making scenarios.

### Behavior
When user asks for options, comparison, or recommendation:
1. Present 2-4 options with structured pros/cons per option
2. Give ONE clear recommendation with reasoning
3. Show comparison table
4. Existing iterative questioning mode stays unchanged

### Addition
New section "Decision Helper Mode" added to brainstormer.agent.md after the questioning section.

### File: `agents/brainstormer.agent.md`

## Feature 4: Infra Setup Agent

### Purpose
Generate Terraform files for AWS ECS Fargate deployment based on knowledge-graph.yaml.

### Output
`infra/` folder containing:
- `main.tf` — provider, backend, locals
- `variables.tf` — configurable inputs
- `outputs.tf` — exported values (ALB URL, ECS cluster, etc.)
- `ecs.tf` — cluster, task definitions, services
- `alb.tf` — load balancer, target groups, listeners
- `security.tf` — security groups, IAM roles

### KG Data Used
- `entry_points` — define ECS services and container ports
- `external_dependencies` — RDS, ElastiCache, S3 resources
- `concerns` — security group rules (auth, database access)

### Focus
AWS Fargate only. Terraform HCL only. Never runs `terraform apply`.

### Tools
- `read`, `edit`, `execute`

### File: `agents/infra-setup.agent.md`

## Success Criteria
- [ ] readme-generator.agent.md created with KG-based generate/update behavior
- [ ] plan-executor.agent.md updated with `todo` in tools list
- [ ] brainstormer.agent.md updated with Decision Helper mode section
- [ ] infra-setup.agent.md created with AWS Fargate + Terraform generation
- [ ] README.md updated to document new agents
- [ ] All agents follow existing persona pattern with boundaries
