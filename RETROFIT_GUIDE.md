# Claude Code Memory Scaffold Retrofit Guide

Use this guide when you already have an advanced project and want to add the Claude Code memory scaffold so your AI coding agent can keep better long-term context.

The scaffold belongs at the root of your existing project repository.

Example:

```text
your-project/
├── .claude/
├── context/
├── raw/
├── wiki/
├── docs/
├── specs/
├── plans/
├── scripts/
├── graphify-out/
├── CLAUDE.md
├── MEMORY_README.md
├── .graphifyignore
├── README.md
├── package.json / pyproject.toml / etc.
└── src/ or app/ or backend/ or frontend/
```

## 1. Unzip The Scaffold

Unzip the scaffold somewhere temporary first, not directly over your project.

```bash
unzip claude-memory-scaffold.zip -d /tmp/claude-memory-scaffold
```

Inspect the contents. You should see files and folders like:

```text
.claude/
context/
raw/
wiki/
docs/
specs/
plans/
scripts/refresh_graph.py
graphify-out/
CLAUDE.md
MEMORY_README.md
.graphifyignore
```

## 2. Copy Scaffold Files Into Your Project Root

Copy these into the root of your existing project:

```text
.claude/
context/
raw/
wiki/
docs/
specs/
plans/
scripts/refresh_graph.py
graphify-out/
CLAUDE.md
MEMORY_README.md
.graphifyignore
```

Be careful with your existing project `README.md`.

Do not overwrite it. Keep the scaffold instructions as `MEMORY_README.md`, or manually merge the relevant workflow sections into your project README.

## 3. Open Claude Code In The Project Root

Go to your project root:

```bash
cd path/to/your-project
claude
```

Then ask Claude Code to adapt the scaffold.

Use this prompt:

```text
This project already exists and is well advanced. I have added a Claude Code memory scaffold to the repo.

Please retrofit the scaffold to this actual project.

Start by reading:
- README.md
- MEMORY_README.md
- CLAUDE.md
- package.json, pyproject.toml, Makefile, justfile, or other build/config files
- the main source folders
- context/project-overview.md
- context/architecture.md
- context/worklog.md
- context/decisions.md
- .claude/commands/lint.md
- scripts/refresh_graph.py

Then update:
- CLAUDE.md with the real stack, coding conventions, constraints, and repo commands
- context/project-overview.md with the actual project mission, users, and priorities
- context/architecture.md with the real system structure and source roots
- context/worklog.md with the current status, active objective, blockers, and next steps
- context/decisions.md with any known durable technical/product decisions
- .claude/commands/lint.md with the real lint/test/typecheck fallback order
- scripts/refresh_graph.py if the code does not live under src/

Do not modify product code unless needed for this scaffold setup.

At the end, tell me:
- what files you updated
- what commands should be used for lint, test, typecheck, dev, and build
- what source folders are included in the graph refresh
- what I should run at the beginning and end of each Claude Code session
```

## 4. Confirm The Source Code Location

By default, the scaffold assumes source code lives in:

```text
src/
```

If your project uses something else, such as:

```text
app/
frontend/
backend/
packages/
services/
```

ask Claude Code to update:

```text
scripts/refresh_graph.py
context/architecture.md
CLAUDE.md
```

so the scaffold understands the real project layout.

## 5. Install Optional Graphify Support

The scaffold works without Graphify, but Graphify can provide richer structural code maps.

Optional install:

```bash
uv tool install graphifyy
graphify install
```

or:

```bash
pipx install graphifyy
graphify install
```

Then test:

```bash
python3 scripts/refresh_graph.py
```

If Graphify is not installed, the script should still create a fallback file index in:

```text
graphify-out/
```

## 6. Validate The Scaffold

In Claude Code, run:

```text
/resume
```

Claude should summarize:

- files loaded
- current project objective
- relevant architecture
- blockers
- next actions
- missing or stale memory

Then run:

```text
/checkpoint
```

Claude should:

- update `context/worklog.md`
- update today's `context/session-summaries/YYYY-MM-DD.md`
- update `context/architecture.md` if architecture changed
- update `context/decisions.md` if durable decisions were made
- run `/lint`
- run `python3 scripts/refresh_graph.py`
- record lint and graph results

## 7. Daily Usage

At the start of every meaningful coding session:

```bash
cd path/to/your-project
claude
```

Then:

```text
/resume
```

This reloads the project memory.

During work, use Claude normally:

```text
Implement this feature...
Debug this failing test...
Review this PR...
Refactor this module...
Update the docs...
```

When you make a durable technical or product decision, use:

```text
/decision
```

When you add raw notes, meeting notes, research, or copied context into `raw/`, use:

```text
/ingest
```

At the end of every meaningful session, run:

```text
/checkpoint
```

That keeps the memory current for the next session.

## 8. Folder Roles

Use the folders like this:

| Path | Role |
|---|---|
| `context/` | Live project memory. Claude reads and updates this constantly. |
| `raw/` | Unprocessed source material: chats, notes, meeting transcripts, vendor docs, research snippets. |
| `wiki/` | Curated reusable knowledge compiled from `raw/`. |
| `docs/` | Human-facing documentation. |
| `specs/` | Product specs, engineering specs, requirements, implementation intent. |
| `plans/` | Planning documents and task breakdowns. |
| `graphify-out/` | Generated structural code graph or fallback source index. |

## 9. Maintenance Commands

Use these regularly:

```text
/resume
```

Start a session by reconstructing project state.

```text
/checkpoint
```

End a session by updating memory, running validation, and refreshing the graph.

```text
/lint
```

Run the project's validation workflow.

```text
/decision
```

Record a durable decision.

```text
/ingest
```

Turn raw source material into curated wiki knowledge.

Manual graph refresh:

```bash
python3 scripts/refresh_graph.py
```

## 10. The Core Habit

The whole scaffold depends on one habit:

```text
Start with /resume.
End with /checkpoint.
```

That is what lets Claude Code avoid starting cold every time.
