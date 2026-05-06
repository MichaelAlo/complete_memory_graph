# Merged Claude Code Memory Setup

This scaffold merges MichaelAlo's project-local memory architecture with Lucas Rosati's Graphify-oriented Claude Code workflow.

It is designed so that `/checkpoint` becomes the single maintenance gateway for the repository:

- update semantic memory in `context/`
- preserve compiled knowledge layers (`raw/`, `wiki/`, `docs/`, `specs/`)
- run `/lint`
- refresh the structural code graph from `src/`

## What this scaffold includes

```text
.
├── CLAUDE.md
├── README.md
├── .graphifyignore
├── .claude/
│   ├── settings.json
│   ├── hooks/
│   │   └── remind-checkpoint.sh
│   ├── commands/
│   │   ├── checkpoint.md
│   │   └── lint.md
│   └── skills/
│       ├── checkpoint/SKILL.md
│       ├── graph-refresh/SKILL.md
│       ├── lint/SKILL.md
│       └── resume/SKILL.md
├── context/
│   ├── architecture.md
│   ├── decisions.md
│   ├── domain-notes.md
│   ├── people-and-stakeholders.md
│   ├── project-overview.md
│   ├── worklog.md
│   └── session-summaries/
├── raw/
├── wiki/
├── docs/
├── specs/
├── graphify-out/
├── scripts/
│   └── refresh_graph.py
└── src/
```

## What `/checkpoint` is intended to do

The merged approach assumes `/checkpoint` performs this sequence:

1. Read the live memory files and recent repo state.
2. Update:
   - `context/architecture.md`
   - `context/decisions.md`
   - `context/worklog.md`
   - `context/session-summaries/<today>.md`
3. Invoke `/lint`.
4. Refresh the code graph for `src/` via `scripts/refresh_graph.py`.
5. Record the lint outcome and graph refresh outcome in the session summary.

## Manual setup you still need to do

This scaffold is intentionally not magic. You still need to make repository-specific edits.

### Required manual edits

Before real use, update these files:

- `CLAUDE.md` — replace placeholder project commands, stack assumptions, and constraints.
- `context/project-overview.md` — describe the real project mission, priorities, and constraints.
- `context/architecture.md` — replace placeholders with the real system structure and invariants.
- `context/decisions.md` — seed historical decisions so Claude has anchors.
- `context/worklog.md` — set the current branch, active objective, blockers, and next steps.
- `.claude/commands/lint.md` — ensure the fallback order matches your stack.
- `scripts/refresh_graph.py` — change the graph target if your code does not live under `src/`.

### Required installs

This scaffold assumes:

- `python3` is available on PATH
- Claude Code is installed and supports project-level `.claude/` configuration
- optionally, Graphify is installed if you want a real graph instead of fallback file indexing

Recommended Graphify installation:

- `uv tool install graphifyy`
- or `pipx install graphifyy`
- then `graphify install`
- optionally `graphify hook install`

### Skills and commands already included

This scaffold already includes:

- `.claude/commands/checkpoint.md`
- `.claude/commands/lint.md`
- `.claude/skills/checkpoint/SKILL.md`
- `.claude/skills/graph-refresh/SKILL.md`
- `.claude/skills/lint/SKILL.md`
- `.claude/skills/resume/SKILL.md`

You do **not** need to create those from scratch unless you want to rewrite them.

### Optional manual additions you may want

Depending on your workflow, you may also want to add:

- `.claude/commands/ingest.md` for `raw/` → `wiki/` compilation
- `.claude/commands/decision.md` for ADR capture
- `.claude/skills/wiki/SKILL.md` for compiled-knowledge maintenance
- a repo-specific test command inside `CLAUDE.md`
- a real Graphify configuration if you want clustering or wiki generation

## Integrate an existing project

Use this section when you already have a repository and want to retrofit the merged memory system.

### Step 1: copy the scaffold into the existing repo

Copy these items into the repository root:

- `CLAUDE.md`
- `.claude/`
- `.graphifyignore`
- `context/`
- `raw/`
- `wiki/`
- `docs/`
- `specs/`
- `scripts/refresh_graph.py`
- `graphify-out/`

Do not blindly overwrite an existing `README.md`; merge the relevant instructions into the project's real README.

### Step 2: map the scaffold to the actual codebase

Immediately update:

- actual lint command
- actual test/typecheck commands
- actual code root if it is not `src/`
- actual architecture in `context/architecture.md`
- actual historical decisions in `context/decisions.md`
- actual current status in `context/worklog.md`

### Step 3: validate the maintenance loop

Inside Claude Code, test this sequence:

1. `/resume`
2. make a small repo change
3. `/checkpoint`

Then verify that:

- `context/architecture.md` changed only if the architecture materially changed
- `context/decisions.md` was appended only with durable decisions
- `context/worklog.md` reflects current next actions
- `context/session-summaries/<today>.md` was updated
- `graphify-out/` contains a refreshed status or graph artifact

### Step 4: tighten the placeholders

After the first successful run, remove generic filler from all starter files so Claude is not learning from boilerplate.

## Set up a new project

Use this section when you are starting from an empty repository.

### Step 1: start with the scaffold in place

Create the repo with this structure from day zero:

- `CLAUDE.md`
- `.claude/`
- `context/`
- `raw/`
- `wiki/`
- `docs/`
- `specs/`
- `scripts/refresh_graph.py`
- `src/`

This is cleaner than retrofitting because memory and maintenance conventions become part of the repo contract immediately.

### Step 2: fill the truth files before heavy coding

Complete these before substantial implementation:

- `CLAUDE.md`
- `context/project-overview.md`
- `context/architecture.md`
- `context/worklog.md`

At minimum, define purpose, constraints, source root, canonical commands, and module boundaries.

### Step 3: install dependencies

- install Graphify if desired
- ensure `python3` is available
- ensure the repo has a working lint command
- optionally enable project hooks through `.claude/settings.json`

### Step 4: adopt the operating rhythm

Recommended rhythm:

- start work with `/resume`
- capture durable design choices in `context/decisions.md`
- use `raw/` for source material, `wiki/` for compiled knowledge
- finish meaningful work with `/checkpoint`

## Maintain an existing project

This section is about ongoing maintenance after setup.

### Per session

At the end of a meaningful work session:

- run `/checkpoint`
- review what it wrote to the daily summary
- ensure it did not add transient noise to `architecture.md`
- ensure `worklog.md` has a clean next action

### Weekly maintenance

Once a week for active projects:

- prune duplicated facts across `architecture.md`, `decisions.md`, and summaries
- clear stale blockers from `worklog.md`
- ensure important design decisions are in `decisions.md`
- verify `scripts/refresh_graph.py` still points at the correct source root
- review whether `raw/` contains material that should be compiled into `wiki/`

### Monthly maintenance

Once a month:

- reduce bloat in `CLAUDE.md`
- archive or merge noisy session summaries
- mark deprecated decisions explicitly instead of silently replacing them
- inspect whether `docs/`, `specs/`, and `wiki/` are drifting or overlapping

### After major refactors

After any major refactor:

- run `/checkpoint`
- verify lint still passes
- verify graph refresh still targets the correct code root
- manually update `context/architecture.md` if subsystem boundaries changed
- review whether older decisions should be marked superseded

## File roles

| Path | Role |
|---|---|
| `CLAUDE.md` | Repo operating contract and routing rules |
| `context/architecture.md` | Enduring technical structure and invariants |
| `context/decisions.md` | Durable decisions and tradeoffs |
| `context/worklog.md` | Current state, blockers, next actions |
| `context/session-summaries/` | Daily or session-based change records |
| `raw/` | Immutable source material |
| `wiki/` | Compiled knowledge |
| `docs/` | Human-facing documentation |
| `specs/` | Product and engineering specifications |
| `graphify-out/` | Structural graph outputs |

## Sanity checks before relying on it

Before trusting the setup, verify:

- `/checkpoint` updates the expected four context files
- `/lint` runs the correct repo command
- `scripts/refresh_graph.py` points at the actual code root
- `graphify-out/refresh-status.json` is created after a refresh
- placeholders have been replaced with real project data
