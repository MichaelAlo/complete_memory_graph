# CLAUDE.md

## Purpose
This repository uses a merged memory model:

- `context/` for live operational memory
- `raw/` for immutable source material
- `wiki/` for compiled reusable knowledge
- `docs/` for human-facing project docs
- `specs/` for product and engineering intent
- `graphify-out/` for structural code graph outputs

Claude Code acts as **software development and project management assistant** for the build of:
- **Data Lake**: MySQL-first curated analytics pipeline (Raw → Std → Curated → Snapshot)
- **Data Wiki**: structured markdown knowledge layer covering MDM entities, modules, datasets, source systems, and Lake Functions

`/resume` is the canonical startup command.
`/checkpoint` is the canonical end-of-session maintenance command.

## Startup routing
At the start of meaningful work, run `/resume`.

`/resume` must:
1. Read `context/project-overview.md`
2. Read `context/worklog.md`
3. Read the latest summary in `context/session-summaries/` if resuming prior work
4. Read `context/decisions.md` and `context/architecture.md` when needed
5. Consult `graphify-out/` when code structure matters

Then state:
- what was loaded
- assumptions being made
- missing context

## Command contract
`/resume` must:
- reconstruct the current objective
- summarize relevant architecture and decision context
- identify current blockers
- propose the next 3 concrete actions
- flag stale or missing memory before work begins

`/checkpoint` must:
- update `context/architecture.md`
- update `context/decisions.md`
- update `context/worklog.md`
- update `context/session-summaries/<today>.md`
- invoke `/lint`
- refresh the code graph for `src/` via `scripts/refresh_graph.py`
- record lint and graph outcomes in the daily summary
- review `wiki/open-questions.md` and flag any deadlines passing within 3 days
- review `context/worklog.md` blockers and check if any can be unblocked
- check `wiki/coverage-audit.md` and flag wiki gaps that are now fillable

## File ownership
- Human-owned: source code in `src/`, `specs/`, most of `docs/`
- Shared: `context/architecture.md`, `context/decisions.md`, `context/worklog.md`
- Claude-maintained or Claude-assisted: `context/session-summaries/`, `wiki/`, `graphify-out/`

## Stack

- **Language:** Python 3.11+
- **Database:** MySQL 8+ (four Lake schemas: `nexus_raw`, `nexus_std`, `nexus_curated`, `nexus_snapshot`)
- **Version control / CI:** GitLab
- **Config:** environment variables via `.env` (use `python-dotenv` in dev)
- **Dependencies:** `mysql-connector-python`, `python-dotenv`
- **Dev dependencies:** `pytest`, `mypy`, `ruff`

## Commands

| Task | Command |
|---|---|
| Lint | `ruff check .` |
| Format | `ruff format .` |
| Type check | `mypy src/` |
| Test | `pytest` |
| Install (dev) | `pip install -e ".[dev]"` |
| Graph refresh | `python scripts/refresh_graph.py` |

There is no dev server — this is a data pipeline platform, not a web app.

## Coding conventions

- All pipeline jobs must be idempotent: rerunnable without duplicating results.
- Every job function must accept a `RunContext` (from `src/lib/run_context.py`) as its first argument.
- Use `get_connection()` from `src/lib/db.py` for all MySQL access.
- Schema and table names come from `Config` (from `src/config/settings.py`), never hardcoded in job logic.
- PII fields must be masked before any record is written to a Lake schema; masking happens in the extraction layer.
- Prefer small, named functions over large procedural scripts.
- No orchestration framework yet — jobs are designed to be called by cron or equivalent.

## Constraints

- No point-to-point module integrations. All inter-system exchange routes through the Lake.
- External providers may not have direct DB access. Use Flow 1 or Flow 2 ingestion patterns.
- No Azure / cloud-native tooling in the first phase.
- Every change that touches a schema, mapping, MDM definition, or quality rule must update code, MDM, Wiki, and lineage metadata together as one tagged release.
- PDPO: Customer PII masked at extraction boundary; do not store unmasked PII in any Lake schema.

## Wiki page types and templates

Every wiki page belongs to one of these types. Use the template in `wiki/templates/` for the relevant type.

| Type | Template | When to create |
|---|---|---|
| MDM entity | `wiki/templates/entity.md` | One per mastered domain (Customer, Policy, etc.) |
| Module | `wiki/templates/module.md` | One per consuming module |
| Source system | `wiki/templates/source.md` | One per upstream source (Core Admin DB, external feeds) |
| Curated dataset | `wiki/templates/dataset.md` | One per certified curated table or report |
| Lake Function | `wiki/templates/lake-function.md` | One per named Lake Function category |

## Additional workflow commands
- Use `/resume` at the beginning of every meaningful Claude Code session.
- Use `/checkpoint` before ending every meaningful Claude Code session.
- Use `/ingest` to convert `raw/` material into curated `wiki/` pages.
- Use `/decision` to append durable ADR-style decisions to `context/decisions.md`.
- Use `/wiki` to create or update a wiki page for a domain, entity, module, dataset, or function.
- Use `/pm` to review project status: open questions, blockers, deadlines, and next concrete actions.
- Use the `wiki` skill when maintaining compiled semantic knowledge.
