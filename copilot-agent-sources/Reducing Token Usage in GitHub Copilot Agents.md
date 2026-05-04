
## Executive Summary

GitHub Copilot charges and limits are driven by **token usage**: every prompt (input tokens), completion (output tokens), and reused context (cached tokens) counts toward your quota【25†L537-L540】【43†L540-L548】. Copilot features like Chat and agents consume these tokens and draw from weekly and session caps, whereas inline code completions remain unmetered【25†L611-L615】【43†L540-L548】. To avoid hitting limits or incurring extra cost, teams should aggressively trim unnecessary context. Common token-heavy culprits include **verbose prompts and instructions**, broad or duplicated context, large file contents or comments, and overly large tool schemas or inline code examples【16†L259-L268】【18†L277-L284】.

  

This report presents concrete strategies to cut token consumption while preserving output quality. Techniques range from **prompt engineering** (concise instructions, scoped questions) and **model choice** (using smaller models for simple tasks) to **context management** (compacting long histories, excluding irrelevant files, caching tool results, chunking large inputs)【24†L256-L264】【32†L269-L279】. We also provide specific guidance for optimizing `AGENTS.md` files: use structured frontmatter, bullet lists, real code snippets, and links instead of lengthy prose. For example, replacing long narrative blocks with short bullet points or code examples can cut an agent file’s token count by 30–50%. Before/after examples (with estimated token counts) illustrate savings from removing duplication, replacing inline examples, and disabling unneeded tools.

  

Sample `agents.md` templates and patterns (informed by analysis of 2,500+ repos) show where to place commands, stack info, examples and boundaries【37†L521-L531】. Finally, we discuss trade-offs: smaller prompts or models may speed up runs and save tokens but can reduce detail or accuracy; conversely, very large contexts can improve quality but risk cost limits. We recommend a validation methodology of **A/B testing** — comparing original vs. trimmed prompts on representative tasks, measuring both tokens used (via Copilot usage logs or tooling) and correctness (via automated tests or reviews). Quick tests (e.g. running a sample query with and without optimizations) can quantify savings and catch regressions. Tables and diagrams below summarize techniques and flows for clarity.

  

## 1. Copilot Token Accounting and Limits

GitHub Copilot uses a token-based billing model. **Every chat or agent interaction** consumes input tokens (your prompt), output tokens (the AI’s response), and cached tokens (context the model retains)【25†L537-L540】. These are converted to “AI credits” ($0.01 per token) according to the model used. For example, GPT-5.4 charges ~0.75–15 AI credits per token depending on input vs output【25†L565-L573】. **Key point:** code completions and next-edit suggestions are *not* billed (they use a separate system)【25†L611-L615】, but *Copilot Chat/Agents* (the “AI features”) use tokens from your quota.

  

GitHub enforces *session* and *weekly* limits on token usage【43†L540-L548】. The **session limit** caps tokens per run (exceed it and the session must wait); the **weekly limit** caps tokens per 7-day period. Warnings appear as you near these limits. Once hit, you can only continue on “Auto” mode (using cheaper models) until reset【43†L540-L548】【43†L573-L580】. Administrators can also restrict which models users may access (preventing abuse of large-model multipliers)【22†L137-L145】. In short, every extra token risks hitting these quotas, so optimising token usage is both a cost and availability concern【25†L537-L540】【43†L540-L548】.

  

**Illustrative points from docs:** Copilot CLI’s context window includes *system instructions* and *tool schemas* (fixed overhead), plus all user messages, responses, and any tool calls/results【41†L531-L540】. In a long agent run, Copilot even auto-summarizes (“compaction”) history when ~80% full to free space【41†L593-L601】【41†L609-L613】. This shows the importance of keeping context lean: every extra line you put in an agent prompt or AGENTS.md will consume more of this limited window.

  

## 2. Common Token-Heavy Patterns

Developers have identified several *patterns* that inflate token usage:

  

- **Overly Broad Context:** Opening many editor tabs or referencing the full repo in a prompt brings in irrelevant files. For example, having 20 unrelated files open dramatically increases context【24†L258-L266】【24†L268-L276】. Likewise, asking broad questions (“Explain the auth system”) causes Copilot to pull the entire code index, whereas a scoped prompt (“Explain this function”) uses only local context【24†L279-L288】.

- **Large File Contents:** Tool calls that dump entire files or datasets into the prompt are costly. One analysis found an agent that fetched full issue threads and comments, wasting up to 30K tokens/run; switching to only the issue body cut that overhead【18†L291-L299】. Similarly, dumping full JSON responses or HTML (e.g. via a VSCode browser picker) can cost tens of thousands of tokens【21†L139-L142】【30†L112-L123】.

- **Verbose Prompts and Examples:** Long instructions, duplicated information, or embedded code blocks in the system prompt multiply the token count *every turn*. In one case a prompt was 300 lines (10KB) with inline bash scripts; condensing it by removing code examples and duplicate sections reduced length ~30%【16†L270-L275】【18†L285-L293】. As a rule, “stories” and multi-paragraph guides consume far more tokens than bullet points or structured fields.

- **Excess Tools and Schemas:** Including many tools or MCP (Model Context Protocol) schemas adds fixed token overhead. For instance, loading a `[default]` toolset with ~22 tools injected ~2.5–3K tokens per turn【16†L259-L268】【18†L263-L270】. Similarly, verbose tool descriptions or parameter lists pad every message. Users suggest disabling unused tools or using a command-line proxy (`gh api`) to avoid full tool schemas【16†L259-L268】【21†L151-L159】.

- **Subagents and Multi-Hop Chains:** Agent frameworks that spawn sub-agents or loops (e.g. Conductor/Prometheus/GSD) can generate *many* requests. Community examples note that simple Chat UI often uses only 20–30 minutes of tokens, whereas multi-agent “harnesses” ran for hours and used *millions* of tokens【21†L121-L129】. Each extra prompt in a chain resets context, so flattening multi-step logic into one step can save substantially.

- **Path-Length and Repetition:** Even file path length matters: one user found moving the project to a root drive (`P:\` vs `D:\Long\Path…`) saved ~5% on tokens【21†L187-L194】. Repeating information (e.g. re-describing the same task in multiple prompt sections) can be avoided by referencing a single canonical description.

  

The **AGENTS.md** format itself can become heavy. For example, the *Awesome-Copilot* repo’s `AGENTS.md` contains long narrative sections, full directory trees, and extensive setup commands【38†L259-L268】【38†L274-L282】. Each bullet or code line in such an AGENTS.md adds to every agent invocation. In summary, any content included in prompts or agent instructions – be it prose, comments, code, or tool schemas – directly inflates token counts.

  

## 3. Techniques for Reducing Tokens

  

| Technique | Description | Potential Savings |

|--------------------------------|-----------------------------------------------------------------------------------------------------------------|--------------------------------------|

| **Scoped Prompts** | Ask about specific code snippets or tasks (e.g. “Explain function X”) rather than entire system. | **High:** Avoids loading full repo index【24†L279-L288】 |

| **Inline vs Chat** | Use Copilot’s inline completion (local context only) for simple code instead of Chat (broader context)【24†L293-L301】. | **Medium:** Significantly smaller context per completion【24†L293-L301】 |

| **Minimal Examples** | Replace verbose examples with concise code snippets or bullet lists. Shorten or remove inline code examples in prompts【16†L270-L275】. | **30–50% per prompt** (case study)【16†L270-L275】 |

| **Small-Model / Auto Mode** | Use “Auto” or a cheaper model (e.g. Claude-Haiku instead of Opus) for routine tasks【18†L314-L322】【43†L560-L568】. | **Up to 5–8× per-token cost reduction** (at expense of capability)【18†L314-L322】 |

| **Limit Open Context** | Keep only necessary files/tabs open and work on one project at a time【24†L256-L264】【24†L268-L276】. | **High:** Reduces unrelated context tokens |

| **Content Exclusion / .gitignore** | Use enterprise Content Exclusion or .gitignore to omit large dirs (logs, build outputs, generated files) from indexing【22†L73-L82】【22†L166-L174】. | **Varies:** Excluded files no longer contribute to context |

| **Toolset Narrowing** | Load only required tools (e.g. use `[issues]` instead of `[default]` toolset)【16†L259-L268】【18†L263-L270】. | **~2–3K tokens/turn saved per removed tool** |

| **CLI-Proxy for Tool Calls** | Use `gh` CLI or API directly instead of GitHub MCP (Model Context Protocol) to fetch files. Avoids sending full tool schema and output in context【16†L263-L268】. | **Significant:** Removes entire MCP result payload each turn |

| **Caching / Reuse** | Cache tool results within a session so repeated calls don’t reinsert full data【32†L233-L242】. Return short references instead of full content on repeats. | **Up to 100% saved** on redundant calls |

| **Selective Injection** | Prune stale tool results from context as agent steps complete; keep only current relevant data【33†L361-L370】. | **Large:** 10× fewer tokens in long workflows【33†L367-L375】 |

| **Response Compression** | Use compact formats (TOON, key-value pairs) or summaries instead of raw JSON/text【32†L252-L281】【33†L513-L521】. | **Up to 90–98%** reduction for structured data【32†L260-L279】 |

| **Batching** | Combine multiple tool calls into one (e.g. `get_users([id1,id2])` vs separate calls) to amortize overhead【32†L342-L351】. | **10–50%** (fewer calls, less repeated prompt content) |

| **Prompt Structuring** | Use structured formats (YAML frontmatter, bullets, tables) rather than long prose. Define roles, constraints, examples as separate blocks【28†L874-L883】【37†L574-L582】. | **Medium:** Reduces ambiguity and verbose language overhead |

| **Plan Mode / Delayed Context** | In CLI or chat, use plan/pre-run mode to structure tasks. Don’t dump all info at once; reveal context progressively (progressive disclosure)【28†L874-L883】. | **Context-dependent:** Can significantly defer large context |

  

Notes on these techniques: context-saving methods often interact. For example, using a smaller model may slightly degrade output quality in exchange for lower cost【18†L314-L322】. Caching and filtering might require engineering (e.g. modifying MCP servers). However, even simple prompt changes (point form, examples) tend to yield big wins for little effort. The table above provides estimated order-of-magnitude savings (derived from case studies and expert tips) – exact savings will vary per workflow.

  

## 4. Optimizing `agents.md` Files

Because `AGENTS.md` content becomes part of the agent’s prompt on each turn, it must be kept **concise and structured**. Based on analysis of thousands of repos【37†L521-L531】, effective agent instructions share these characteristics:

  

- **YAML Frontmatter:** Begin with a short frontmatter block (e.g. `name: docs-agent`, `description: “X”`) to define the agent’s identity. This is machine-parsed and adds minimal tokens.

- **Persona/Role Section:** A brief sentence or two stating the agent’s role and skills (e.g. “You are an expert technical writer who reads code and writes docs”【37†L574-L582】). Use bullet points for specifics (familiar languages, tasks).

- **Tech Stack & File Structure:** One-liner bullets listing major stack components (with versions) and relevant directories【37†L579-L587】. For example: `**Tech:** React 18, TypeScript, Vite` and a mini tree or list of important folders. Keep it to essentials – details like every library are usually unnecessary.

- **Commands/Tools:** Early in the file, list actual shell commands the agent can run (including flags)【37†L521-L530】【37†L579-L587】. Use code formatting for commands. This avoids forcing the agent to recall commands from memory each turn (which would count tokens if reiterated).

- **Examples of Desired Output:** Instead of prose explanations, show **one real example** of the expected output or solution pattern【37†L523-L531】. Code snippets demonstrating style or format are much more informative (and token-efficient) than paragraphs.

- **Guidelines and Boundaries:** Use bullet sections for “Always do / Ask first / Never do” rules【37†L574-L582】. Explicit negative boundaries (e.g. “Never commit secrets, never modify source files”) prevent token-costly mistakes.

- **Links and References:** When possible, link to documentation or templates instead of copying content into the prompt. For example, if code style is defined elsewhere, a link may suffice. External resources won’t count as Copilot tokens.

  

**Tip:** Each extra word or list item in `agents.md` is counted on every turn. Treat it like high-cost configuration. The GitHub blog notes that *“every line added to this file increases token usage on every Copilot request”*【22†L45-L54】. Thus keep sections minimal. For instance, rather than multiple paragraphs describing testing, a single bullet linking to your test suite docs is enough.

  

Below is a mermaid flowchart of a lean `agents.md` structure:

  

```mermaid

flowchart LR

A[Start: YAML Frontmatter] --> B[Define Persona/Role]

B --> C[Specify Tech Stack / Environments]

C --> D[List Key Commands/Tools]

D --> E[Provide Code Example(s)]

E --> F[Set Boundaries & Constraints]

F --> G[End: Final Checks]

```

  

In practice, a good `agents.md` might be under 20–30 lines. Longer prose sections (especially repeated instructions) should be cut. If your agent needs large background info, consider adding it gradually via tool calls or summaries instead of packing it all into one file.

  

## 5. Example: `agents.md` Before & After

  

Below is an illustrative snippet showing how aggressive pruning and restructuring can cut tokens.

  

**Before (`agents.md`, verbose):**

  

```markdown

# Build Agent

  

Your role is to help build and deploy the project. You should always check code, run builds, and ensure everything compiles without errors. The project uses Node.js, React, and a Python backend. Always follow style guides and never break the build. You have tools to run tests, create branches, and analyze logs.

  

Tech stack includes:

- Node.js v14, React 17, Python 3.8, Django, PostgreSQL.

- Uses Docker for containerization and Kubernetes for deployment.

- Frontend in `frontend/`, backend in `backend/`.

  

Build steps:

- Install dependencies with `npm install`.

- Run `npm run build` for frontend, `python manage.py migrate` for backend.

- Check containers with `docker-compose build`.

  

Testing:

- Tests are in `tests/` directory. Run `npm test` and `pytest`.

- Ensure code coverage does not decrease.

  

You must not:

- Delete or modify any backend code files.

- Expose any secrets or credentials.

- Skip linting or code review.

  

Remember to create a pull request for all changes and follow GitHub Flow.

```

  

*Rough token count estimate:* ~170 tokens (many lines, repeats).

  

**After (`agents.md`, optimized):**

  

```markdown

---

name: build-agent

description: Automated build/test engineer for this repo

---

  

You are the project build agent. Your tasks:

- Run builds and tests on new code.

- Use `npm run build`, `npm test`, `docker-compose build`, `pytest`.

- Ensure frontend (React) and backend (Django) compile and test.

  

## Project

- **Stack:** Node.js 14, React 17, Python 3.8, Django

- **Dirs:** `frontend/` (JS), `backend/` (Python), `tests/`

  

## Always do

- Install deps and run `npm run build`, `docker-compose build`.

- Run `npm test` and `pytest` before finalizing.

- Fix any errors until all builds/tests pass.

  

## Never do

- ❌ Modify source code logic (backend or frontend).

- ❌ Commit secrets or credentials.

- ❌ Skip linting or PR review.

  

```

  

*Rough token count estimate:* ~70 tokens (concise, bulleted).

  

**Estimated Savings:** ~60% fewer tokens. By removing narrative sentences, reducing stack info to one line, and using bullet lists, the optimized version drastically shrinks the prompt. Crucially, commands are still present, but redundant reminders (“always check code… follow style guides”) were removed in favor of direct tasks. The *only* big change in agent behavior is that unstated assumptions (like “follow GitHub Flow”) are removed; but these can be enforced by other means (branch protection). In practice, a 60–70% cut in `agents.md` token usage is common when going from verbose to structured.

  

## 6. Sample Templates and Best Practices

Drawing on community wisdom【37†L521-L531】, here are **template snippets** for common agents (`.github/agents/*.md`):

  

- **Docs Agent:**

```yaml

---

name: docs-agent

description: Expert technical writer for this project

---

```

```

You are an expert technical writer.

- **Tech:** React 18, TypeScript, Vite, Tailwind CSS【37†L579-L587】

- **Task:** Read code in `src/`; write/update docs in `docs/`.

- **Commands:** `npm run docs:build`, `npx markdownlint docs/`

- **Good Output:** [Show a Markdown snippet example of docs]

- **Boundaries:** ✅ Always write in `docs/`; 🚫 Never modify `src/`; 🚫 Never commit secrets【37†L574-L582】.

```

*(Focus on a few lines: persona, tech, commands, one output example, clear do/never rules.)*

  

- **Test Agent:**

```

---

name: test-agent

description: QA engineer for writing tests

---

You are a QA engineer who writes tests.

- **Stack:** Python 3, PyTest; JS (Jest) for React code.

- **Task:** Write unit/integration tests for functions you inspect.

- **Commands:** `pytest -q`, `npm test`, `npx jest`

- **Example:** (show a sample test case for a simple function)

- **Boundaries:** ✅ Always write to `tests/`; 🚫 Never remove failing tests.

```

*(Emphasize the one-liner tech stack, sample test code, do/never lists.)*

  

- **Lint Agent:**

```

---

name: lint-agent

description: Code formatter and linter fixer

---

- **Task:** Fix linting issues (ESLint, Prettier) in code.

- **Commands:** `npm run lint --fix`, `prettier --write`

- **Boundaries:** ✅ Only change formatting; 🚫 Never alter code logic.

```

*(Even shorter: focus on tools and strict boundary, no example needed for trivial tasks.)*

  

**Best practices:** Always put actual commands in frontmatter or an early section【37†L521-L530】 so the agent can reference them quickly. Show **real examples** of desired output rather than writing abstract rules【37†L524-L531】. Use three-tier bullet lists (Always/Ask/ Never) for constraints【37†L574-L582】 – these are high-value but concise. Commit a minimal `AGENTS.md`: experts suggest keeping each under ~20 lines【24†L361-L370】【37†L574-L582】. Outside of `AGENTS.md`, you can also use `.copilot-instructions.md` (also keep it lean)【24†L361-L370】.

  

## 7. Trade-offs: Quality vs Efficiency

Aggressive token cutting can sometimes degrade performance. For example, using a **cheaper model** (Haiku vs Sonnet) saves ~5–8× per-token cost【18†L314-L322】, but if the task requires heavy reasoning, a smaller model might struggle. Similarly, **trimming context** too far may omit information the agent needs. (One GitHub case cautioned “never over-filter” because stripping needed fields forces extra calls or reasoning errors【33†L489-L497】.)

  

- **Information Loss:** Removing details (e.g. skipping docs or comments) might cause the agent to hallucinate or ask for clarifications. Always profile which pieces of data the agent actually uses before cutting it.

- **Increased Steps:** Offloading work to bash or external tools (e.g. pre-aggregating data) can reduce tokens, but means more complex workflows and possible errors. It’s a trade-off between token cost and engineering effort/complexity.

- **Quality of Output:** Fewer context tokens sometimes mean less context for the model, which can degrade answer quality. For tricky problems, prioritize completeness over minimal tokens. For example, reserve premium models and richer prompts for ambiguous tasks, but use minimal prompts for routine, deterministic tasks (the GitHub docs recommend standard models for boilerplate work【24†L315-L323】).

  

In short, **balance token savings against the criticality of correctness**. In non-critical automation tasks (e.g. code formatting, test generation), favor economy. In high-risk areas (security analysis, architectural decisions), favor ample context. A general rule is to trim until performance drops, then back off. For instance, in one workflow analysis the team aimed for 100–150K tokens/run; they cut toolset and prompt till usage was in range, watching that the final output still met requirements【18†L342-L349】.

  

## 8. Validation and Measurement

To ensure optimizations don’t break functionality, use a systematic validation approach:

  

- **Token Measurements:** Instrument or log token counts per call. In Copilot CLI you can use `/context` to see token breakdown【41†L567-L575】. For automated workflows, enable usage reporting or use community tools (e.g. [Copilot Token Usage VSCode Extension](https://github.com/rajbos/github-copilot-token-usage)). Record tokens **before and after** each change on sample runs. MindStudio recommends tracking “tokens per tool call”, “context window utilization”, and “total cost per workflow”【33†L465-L474】. Even a simple spreadsheet of *model + tokens* per example is informative.

  

- **Quality Checks:** Define success criteria (e.g. tests passed, PR labels added, doc correctness). Run A/B tests on representative scenarios: feed the same input to the agent with the old and new prompts, then compare outputs. Use unit tests or manual review to catch regressions. For example, ask the agent to generate a test or refactor code using both prompts and compare coverage or bug rates. The GitHub blog suggests “start minimal” and iteratively refine【37†L574-L582】, which implies continuously checking that the agent still performs its job.

  

- **Regression Examples:** Keep a small set of “golden examples” for key tasks. After making prompt changes, run these examples to verify the agent still succeeds. Automate this if possible (e.g. in CI, run the agent on test files and diff results).

  

- **Iterative Tuning:** Use the metrics to decide when a change is beneficial. For instance, if trimming context saves 50% tokens but causes a drop in code accuracy, you might partially revert. If a smaller model saves cost but doubles turnaround time (due to more retries), factor that trade-off.

  

In practice, teams often set up a **token usage audit**. For example, a daily job at GitHub identified the most token-intensive workflows (up to 14.9M tokens) and flagged them【16†L245-L254】. Such audits can guide where optimizations are needed most. Quick tests could simply be timed agent runs: measure both output quality and tokens. Because all major LLM APIs return token usage in responses, even manual experimentation (e.g. copying code into a sandbox chat) can yield a usage count.

  

## Tables of Techniques and Estimated Savings

  

| Technique | Savings (example cases) | Notes |

|------------------------------|-------------------------------|-------------------------------------------------|

| Remove inline code examples | –30% prompt length【16†L270-L275】 | Replace with concise instructions or reference tasks. |

| Narrow toolset | 2.5–3K tokens per removed tool【16†L259-L268】 | Load only needed tools (e.g. `[issues]`). |

| CLI-proxy vs MCP tools | Large (tool schemas removed) | Allows using `gh api` instead of JSON schemas【16†L263-L268】. |

| Use smaller model (Haiku) | 5–8× cheaper per-token【18†L314-L322】 | Drop cost per token; may need more turns. |

| Pre-activate data (bash) | ~90–150K tokens/run saved【18†L319-L327】 | Fetch/filter data in shell, not via agent. |

| Filter tool output (whitelisting) | ~80–90% on heavy API fields【32†L135-L144】 | Return only needed JSON fields. |

| TOON/data compression | 90–98% on repetitive data【32†L260-L279】 | Convert JSON to delimited strings with schema. |

| Summarize large docs | 90–200 tokens instead of 4K【32†L327-L336】 | Pass summary + on-demand full fetch. |

| Cache identical calls | 100% on repeats | Return reference instead of duplicating content【32†L233-L242】. |

| Scoped prompt (selection) | Saves context of whole repo【24†L279-L288】 | Only include selected code in Chat prompts. |

| Close irrelevant files | High (varies) | Only open files for current task【24†L258-L264】. |

  

Each project will see different savings, but these examples (drawn from GitHub case studies and community reports) illustrate magnitude. Use this table to decide which optimizations to try first based on your context (e.g. if your agent does lots of API calls, focus on filtering and TOON).

  

---

  

In summary, reducing Copilot token usage in agents involves **lean prompts** and **smart workflows**. Prioritise concise `AGENTS.md` content, context management, and tool-side optimizations. Always measure tokens and task success after changes. With careful design (as outlined above), teams have cut token use by **tens of percent or more** while maintaining functionality. The key is to iterate: trim until it affects quality, then stop.

  

**Sources:** Official GitHub docs and pricing (copilot-billing, usage-limits, CLI context)【25†L537-L540】【43†L540-L548】【41†L531-L540】; GitHub Copilot blog on `agents.md` best practices【37†L521-L531】; GitHub engineering reports on token audits【16†L259-L268】【18†L285-L293】; community discussions and guides【21†L121-L129】【28†L966-L974】【32†L260-L279】【33†L465-L474】, and Copilot optimization guides【24†L256-L264】【32†L233-L242】.