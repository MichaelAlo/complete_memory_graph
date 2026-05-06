# CLAUDE.md

## Identity
Project: [PROJECT NAME]
Stack: [e.g. Python 3.12, FastAPI, PostgreSQL, Docker]
Repo: [repo URL or local path]

## Context loading policy (project memory layer)
Before starting any task, load the minimum relevant files:
- Continuing work / orientation → context/worklog.md + latest context/session-summaries/
- Feature work → context/worklog.md + relevant specs/ file
- Architecture changes → context/architecture.md + context/decisions.md
- Domain/business logic → context/domain-notes.md OR wiki/concepts/
- Full project orientation → context/project-overview.md

## Knowledge base policy (Karpathy wiki layer)
- Domain/research questions → query wiki/ first
- Feature work requiring domain knowledge → read wiki/concepts/ or wiki/summaries/
- New source to ingest → /ingest raw/[filename]
- Periodic health check → /lint

## Commands
- Test:      [e.g. pytest tests/]
- Lint:      [e.g. ruff check .]
- Typecheck: [e.g. mypy src/]
- Run:       [e.g. uvicorn src.main:app --reload]
- Build:     [e.g. docker build -t app .]

## Hard constraints
- [e.g. Never commit secrets or API keys]
- [e.g. All endpoints must have typed request/response models]
- [e.g. No synchronous DB calls in async routes]

## Output style
- Be concise and implementation-oriented
- State assumptions before editing when uncertainty is high
- Explain tradeoffs when proposing architecture changes

## Operating rules
- Never invent project history. If context is missing, say so explicitly.
- Follow existing conventions before introducing new patterns.
- After every durable design decision → append to context/decisions.md
- After every session of substance → write context/session-summaries/YYYY-MM-DD.md + update context/worklog.md
- After structural code changes → update context/architecture.md
- After completing a spec → mark done in context/worklog.md

## Wiki schema (Karpathy wiki layer)

### Routing
- Domain/research questions → query wiki/ first
- Feature work needing domain context → check wiki/concepts/ before building
- New source to ingest → /ingest raw/[filename]
- Periodic health check → /lint

### Page conventions
All wiki pages must start with this YAML frontmatter:
---
title: [Page title]
type: [concept | entity | summary | index]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [list of raw/ files this page draws from]
related: [list of other wiki pages]
---

Page structure by type:
- concept pages:  definition → context → key properties → related concepts → sources
- entity pages:   what it is → why it matters → key facts → related entities → sources
- summary pages:  source metadata → key takeaways → concepts introduced → entities mentioned

### Ownership rules
- Claude owns wiki/ entirely. Never ask the user to edit wiki/ manually.
- raw/ is immutable. Claude reads from it, never writes to it.
- wiki/index.md is updated on every ingest and every lint pass.

### Ingest log
Append one line to wiki/index.md after every ingest:
- YYYY-MM-DD | [source filename] | [one-line description] | [N pages created, M updated]