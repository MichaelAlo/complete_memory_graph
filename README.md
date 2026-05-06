# Claude Code Memory System

A markdown-based persistent memory architecture for Claude Code.
Combines two systems:
1. **Project memory** — gives Claude durable engineering context across sessions
2. **LLM Wiki** — a Karpathy-style knowledge base Claude builds and maintains from raw sources

---

## Why this exists

Claude Code has no memory between sessions by default.
Every time you start a new session, Claude starts cold.

This system solves that on two levels:

**Level 1 — Project memory (`context/`)**
Stores your project's state, decisions, architecture, and worklog.
Claude reads these on demand. You run `/resume` and Claude reconstructs the full session state in seconds.

**Level 2 — Knowledge base (`raw/` + `wiki/`)**
Instead of re-deriving knowledge from raw documents on every query (RAG),
Claude reads your source documents once and compiles them into a structured,
interlinked wiki it actively maintains. Knowledge compounds over time.
This is Andrej Karpathy's LLM Wiki pattern (GitHub Gist, April 2026).

---

## Full file and folder reference
```
your-project/
│
├── CLAUDE.md ← Auto-loaded by Claude Code. Router + operating rules.
├── README.md ← This file.
│
├── .claude/
│ └── commands/
│ ├── resume.md ← /resume → reconstruct session state from context/
│ ├── checkpoint.md ← /checkpoint → write session summary + update worklog
│ ├── decision.md ← /decision → append a decision to decisions.md
│ ├── ingest.md ← /ingest → ingest a raw source into the wiki
│ └── lint.md ← /lint → health-check the wiki
│
├── context/ ← PROJECT MEMORY. Claude reads these on demand.
│ ├── project-overview.md ← Mission, goals, priorities, non-goals, current status
│ ├── architecture.md ← System design, components, data flow, invariants
│ ├── decisions.md ← ADR-style log of durable decisions and their rationale
│ ├── worklog.md ← Current branch, objective, blockers, next actions
│ ├── domain-notes.md ← Business/domain knowledge that is stable but not code
│ ├── stakeholders.md ← People, teams, external dependencies, contacts
│ └── session-summaries/
│ └── YYYY-MM-DD.md ← One file per session. Written by Claude via /checkpoint.
│
├── raw/ ← KARPATHY WIKI: immutable source documents. You own this.
│ ├── articles/ ← Web articles, blog posts (use Obsidian Web Clipper)
│ ├── papers/ ← Research papers, PDFs converted to markdown
│ └── references/ ← API docs, specs, external references
│
├── wiki/ ← KARPATHY WIKI: LLM-generated knowledge base. Claude owns this.
│ ├── index.md ← Master index of all wiki pages with one-line summaries
│ ├── concepts/ ← Concept pages: definitions, explanations, comparisons
│ ├── entities/ ← Entity pages: people, tools, systems, organizations
│ └── summaries/ ← Per-source summaries linked back to raw/
│
├── specs/ ← Human-written feature/system specs. Input to Claude.
│ ├── feature-x.md
│ └── api-contract.md
│
├── docs/ ← Generated documentation. Output from Claude.
│ ├── api.md
│ └── onboarding.md
│
└── src/ ← Your actual codebase.
```

---

## The two systems explained

### System 1 — Project memory (`context/`)

Stores everything Claude needs to know about your project's current state.
Claude reads these files on demand based on the task type.
You and Claude maintain them together via the five commands below.

**You write:** `project-overview.md`, `domain-notes.md`, `stakeholders.md`, `CLAUDE.md`
**Claude writes:** `decisions.md` (via `/decision`), `worklog.md` and `session-summaries/` (via `/checkpoint`), `architecture.md` (when prompted after structural changes)

### System 2 — LLM Wiki (`raw/` + `wiki/`)

Inspired by Andrej Karpathy's LLM Knowledge Bases pattern (April 2026).
The key insight: instead of rediscovering knowledge from raw documents on every query,
the LLM compiles them once into a structured wiki and keeps it current as new sources arrive.

**You own:** `raw/` — drop sources here, never modify them. This is your source of truth.
**Claude owns:** `wiki/` — Claude creates pages, updates them, maintains cross-references. You only read it.
**You co-evolve:** The wiki schema section in `CLAUDE.md` that defines conventions and workflows.

The three wiki operations:
- **Ingest** — drop a file in `raw/`, run `/ingest raw/[file]`
- **Query** — ask: *"Query the wiki about [topic]"*
- **Lint** — run `/lint` weekly for a health check

---

## File reference

### `CLAUDE.md`
The control file. Auto-loaded by Claude Code every session.
Contains: project identity, context loading policy, wiki routing policy, operating rules, real commands, hard constraints, output style, wiki schema.
**Keep it short (40–80 lines).** It is a router and rule file, not a knowledge dump.
**You maintain it.** Update when project norms, stack, or wiki conventions change.

---

### `.claude/commands/resume.md` — `/resume`
Run at the **start of every session**.
Claude reads `CLAUDE.md`, `context/worklog.md`, the latest session summary, and recent decisions.
Outputs: current objective, last session summary, active branch/spec, next actions, open questions.
Do not start working until you have verified the output is accurate.

---

### `.claude/commands/checkpoint.md` — `/checkpoint`
Run at the **end of every session**.
Claude writes `context/session-summaries/YYYY-MM-DD.md` and updates `context/worklog.md`.
Also flags if `context/architecture.md` needs updating based on what changed this session.
Review the output before closing. Correct anything inaccurate.

---

### `.claude/commands/decision.md` — `/decision <text>`
Run **immediately after any durable design decision**.
Claude appends a formatted ADR entry to `context/decisions.md`.
Do not batch decisions. Log them the moment they are made.

Example:
```
/decision Use Alembic for DB migrations instead of a custom system — integrates cleanly with SQLAlchemy.
```

---

### `.claude/commands/ingest.md` — `/ingest raw/[file]`
Run when you **add a new source** to `raw/`.
Claude reads the source, discusses key takeaways with you, writes a summary page
to `wiki/summaries/`, updates relevant `wiki/concepts/` and `wiki/entities/` pages,
updates `wiki/index.md`, and flags any contradictions with existing wiki content.
A single source typically touches 10–15 wiki pages.

Example:
```
/ingest raw/articles/attention-is-all-you-need.md
```

---

### `.claude/commands/lint.md` — `/lint`
Run **weekly** to keep the wiki healthy.
Claude reads `wiki/index.md`, scans all pages, and produces a structured report covering:
contradictions, stale claims, orphan pages, missing cross-references, and data gaps.
Claude then asks which issues to fix immediately.

---

### `context/project-overview.md`
Mission, goals, non-goals, current priorities, status, success criteria, key constraints.
**You maintain it.** Update at milestones or when priorities shift. Not every session.

---

### `context/architecture.md`
System map: components, locations in `src/`, data flow, external dependencies, invariants, tech debt.
**Claude maintains it** when prompted after structural code changes.
Prompt: *"Update context/architecture.md to reflect the change we just made."*

---

### `context/decisions.md`
Permanent ADR log. One entry per decision, never deleted.
**Claude maintains it** via `/decision`.
Superseded decisions should be annotated, not removed.

---

### `context/worklog.md`
Live state of work: current branch, active spec, objective, in-progress tasks, blockers, next actions, open questions.
**Claude maintains it** via `/checkpoint` every session end.
Most-read file in the system. A stale worklog breaks continuity.

---

### `context/domain-notes.md`
Stable business/domain knowledge: core concepts, business rules, compliance constraints, glossary.
**You maintain it.** Update when domain rules change or Claude repeatedly misunderstands a domain concept.

---

### `context/stakeholders.md`
Team members, external dependencies, contacts, key relationships.
**You maintain it.** Update when team or dependencies change.

---

### `context/session-summaries/YYYY-MM-DD.md`
Compact session record: what was done, decisions made, current state, next actions, open questions.
**Claude writes it** via `/checkpoint`. One file per day.
Retain last 30 days. Delete older files once `worklog.md` reflects current state.

---

### `raw/`
Immutable source documents for the wiki. Articles, papers, references.
**You own it.** Drop files here. Never modify them after adding.
Use Obsidian Web Clipper to capture web articles as markdown.
This is the source of truth for the wiki layer.

---

### `wiki/`
LLM-generated knowledge base. Summaries, concept pages, entity pages, cross-references.
**Claude owns it entirely.** You only read it, never manually edit it.
Grows and deepens every time you ingest a new source.
Sub-folders: `concepts/`, `entities/`, `summaries/`.
`index.md` is the master index of all pages.

---

### `wiki/index.md`
Master index of all wiki pages. Claude updates it on every ingest and every lint pass.
Contains: page title, one-line summary, link, last updated date.
Seed it with the topics you want the wiki to cover before the first ingest.

---

### `specs/`
Human-written feature and system specifications. Written before asking Claude to build anything.
Each file covers: purpose, inputs, outputs, constraints, acceptance criteria, open questions.
**You write it.** One file per feature or system component.
Rule: never ask Claude to build a complex feature without a spec file first.

---

### `docs/`
Project documentation output. Claude generates and updates these after code changes.
Contains: `api.md` (endpoint reference), `onboarding.md` (new developer setup).
Prompt Claude: *"Update docs/api.md to reflect the endpoint we just added."*

---

### `src/`
Your actual codebase. The memory system describes it; it does not contain the memory system.

---

## The five commands

| Command | When | What it does |
|---|---|---|
| `/resume` | Start of every session | Reads context files, reports current state |
| `/checkpoint` | End of every session | Writes session summary, updates worklog |
| `/decision <text>` | Immediately after any design decision | Logs ADR entry to decisions.md |
| `/ingest raw/[file]` | When adding a new source to the wiki | Reads source, writes summary, updates concept/entity pages and index |
| `/lint` | Weekly | Health-checks wiki for contradictions, orphans, stale claims, gaps |

---

## Session protocol

### Starting a session
```
/resume
```

Verify the output is accurate. Correct any stale context file before starting work.

### During a session

| Situation | Action |
|---|---|
| Made a design decision | `/decision <text>` immediately |
| Added a module or changed system structure | *"Update context/architecture.md to reflect [change]"* |
| Starting a new feature | Write `specs/feature-name.md` first |
| Adding new knowledge source | Drop in `raw/`, then `/ingest raw/[filename]` |
| Need domain/research context | *"Query the wiki about [topic]"* |

### Ending a session
```
/checkpoint
```

Review and correct the output before closing.

---

## Wiki maintenance

### Ingest a new source
```
Drop file into raw/articles/, raw/papers/, or raw/references/
Then run: /ingest raw/[filename]
```

Claude reads the source, writes a summary page, updates relevant concept and entity pages,
updates `wiki/index.md`, and appends to the ingest log.
A single source typically touches 10–15 wiki pages.

### Query the wiki
```
"Query the wiki about [topic] and give me a synthesis."
```

Claude searches relevant pages, reads them, and synthesizes an answer.
Output can be a markdown page, comparison table, or summary.

### Lint the wiki (weekly)
```
/lint
```


---

## Weekly maintenance (5 minutes)

| Task | File | Action |
|---|---|---|
| Archive old done items | `context/worklog.md` | Remove items older than 2 weeks |
| Check for contradictions | `context/decisions.md` | Annotate superseded entries |
| Verify structure matches code | `context/architecture.md` | Compare against real `src/` |
| Clean old summaries | `context/session-summaries/` | Delete files older than 30 days |
| Update priorities | `context/project-overview.md` | Refresh if focus has shifted |
| Lint wiki | `wiki/` | Run `/lint` |

---

## What degrades the system

| Failure mode | Effect | Prevention |
|---|---|---|
| Skipping `/checkpoint` | Worklog goes stale, next `/resume` is inaccurate | Make it the last thing you type every session |
| Bloating `CLAUDE.md` | Instructions dilute, Claude loads noise | Move knowledge to `context/`; keep `CLAUDE.md` as rules only |
| Not logging decisions | Future Claude contradicts past choices | Use `/decision` immediately, not retroactively |
| Never updating `architecture.md` | Claude misunderstands codebase structure | Prompt an update after every structural change |
| Editing files in `wiki/` manually | Wiki loses integrity, Claude loses trust in its own layer | Never edit `wiki/` manually. Claude owns it. |
| Adding modified files to `raw/` | Source of truth is corrupted | `raw/` is append-only and immutable |
| Leaving placeholders unfilled | Claude operates without real context | Complete the first-time setup checklist below |

---

## First-time setup checklist

**Project memory layer**
- [ ] Fill in `CLAUDE.md` commands section with real test/lint/run/build commands
- [ ] Fill in `context/project-overview.md` with real mission, goals, non-goals
- [ ] Fill in `context/architecture.md` with real components and data flow
- [ ] Add 3–5 real past decisions to `context/decisions.md`
- [ ] Fill in `context/worklog.md` with current branch, objective, next actions
- [ ] Write `context/session-summaries/` seed summary manually

**Wiki layer**
- [ ] Seed `wiki/index.md` with the topics you want this wiki to cover
- [ ] Add `.gitkeep` to `raw/articles/`, `raw/papers/`, `raw/references/` and commit
- [ ] Drop first source into `raw/` and run `/ingest` to verify the pipeline works

**Verify**
- [ ] Run `/resume` and confirm the output reflects reality
- [ ] Run a test ingest and confirm `wiki/index.md` was updated

Once all boxes are checked, the system is operational.

---

## The one rule

> **`/resume` to start. `/checkpoint` to end. `/decision` for every real choice.**

These three habits keep the project memory alive.
For the wiki: **ingest sources as you find them, lint weekly.**
