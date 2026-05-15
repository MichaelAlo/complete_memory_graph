# Claude Code Memory Scaffold New Project Guide

Use this guide when you are starting a brand-new project and want the Claude Code memory scaffold to be part of the repository from day one.

For a new project, the scaffold is not retrofitted around existing code. It becomes the starting repo contract: where memory lives, how Claude Code resumes context, and how each session gets checkpointed.

The core habit is:

```text
Start with /resume.
End with /checkpoint.
```

## 1. Create The Project Folder

Create a new empty folder for your project:

```bash
mkdir my-new-project
cd my-new-project
```

## 2. Unzip The Scaffold Into The Project Root

Unzip the scaffold directly into the new project folder:

```bash
unzip path/to/claude-memory-scaffold.zip -d .
```

You should now have a structure like:

```text
my-new-project/
├── .claude/
├── context/
├── raw/
├── wiki/
├── docs/
├── specs/
├── plans/
├── scripts/
│   └── refresh_graph.py
├── graphify-out/
├── src/
├── CLAUDE.md
├── MEMORY_README.md
├── COLLEAGUE_RETROFIT_GUIDE.md
├── NEW_PROJECT_GUIDE.md
└── .graphifyignore
```

## 3. Create A Product README

For new projects, keep:

```text
MEMORY_README.md
```

as the scaffold documentation.

Create a separate project/product README:

```bash
touch README.md
```

Use `README.md` for the actual product: what it does, how to install it, how to run it, and how to deploy it.

## 4. Open Claude Code In The Project Root

From the new project root, run:

```bash
claude
```

Then ask Claude Code to initialize the project.

Use this prompt:

```text
I am starting a new project using this Claude Code memory scaffold.

Project idea:
[describe the product]

Preferred stack:
[describe the stack, or say "recommend one"]

Please initialize this project inside the scaffold.

Use the scaffold conventions:
- keep MEMORY_README.md as the scaffold guide
- create or update README.md as the product README
- put source code in src/ unless there is a strong reason not to
- fill context/project-overview.md with the project mission, users, constraints, and priorities
- fill context/architecture.md with the initial architecture and source roots
- initialize context/worklog.md with current focus, blockers, and next steps
- add initial decisions to context/decisions.md where appropriate
- update CLAUDE.md with the real stack, repo commands, coding conventions, and constraints
- update .claude/commands/lint.md with the actual validation commands
- update scripts/refresh_graph.py if the source root is not src/

Then scaffold the application files, run the relevant validation commands, and tell me:
- what files you created or updated
- what commands I should use for dev, lint, test, typecheck, and build
- what source folders are included in the graph refresh
- what I should run at the beginning and end of each Claude Code session
```

## 5. Decide Where Code Lives

By default, put application code in:

```text
src/
```

This matches the default graph refresh script:

```text
scripts/refresh_graph.py
```

If your stack has a strong convention, you can use another layout:

```text
app/
frontend/
backend/
packages/
services/
```

If you do, ask Claude Code to update:

```text
scripts/refresh_graph.py
context/architecture.md
CLAUDE.md
```

so the scaffold understands the actual source roots.

## 6. Fill The Truth Files Before Heavy Coding

Before the project grows, make sure these files are real and specific:

```text
context/project-overview.md
context/architecture.md
context/worklog.md
context/decisions.md
CLAUDE.md
```

These are the files Claude Code will rely on most.

At minimum, they should define:

- what the project is for
- who the users are
- what stack is being used
- where source code lives
- what commands run the project
- what commands validate the project
- what constraints matter
- what decisions have already been made
- what the next concrete tasks are

## 7. Install Optional Graphify Support

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

## 8. Validate The First Session

Once the initial app scaffold exists, run:

```text
/resume
```

Claude should summarize:

- files loaded
- current project objective
- initial architecture
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
- update `context/architecture.md` if the architecture changed
- update `context/decisions.md` if durable decisions were made
- run `/lint`
- run `python3 scripts/refresh_graph.py`
- record lint and graph results

## 9. Daily Usage

At the start of every meaningful coding session:

```bash
cd path/to/my-new-project
claude
```

Then:

```text
/resume
```

During work, use Claude normally:

```text
Implement this feature...
Debug this failing test...
Design this data model...
Create this component...
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

## 10. Folder Roles

Use the folders like this:

| Path | Role |
|---|---|
| `src/` | Default home for application source code. |
| `context/` | Live project memory. Claude reads and updates this constantly. |
| `raw/` | Unprocessed source material: chats, notes, meeting transcripts, vendor docs, research snippets. |
| `wiki/` | Curated reusable knowledge compiled from `raw/`. |
| `docs/` | Human-facing documentation. |
| `specs/` | Product specs, engineering specs, requirements, implementation intent. |
| `plans/` | Planning documents and task breakdowns. |
| `graphify-out/` | Generated structural code graph or fallback source index. |

## 11. Maintenance Commands

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

## 12. The Core Habit

The scaffold is useful only if the memory stays fresh:

```text
Start with /resume.
End with /checkpoint.
```

That is what lets Claude Code build context over time instead of starting cold every session.
