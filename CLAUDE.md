# CLAUDE.md

## Purpose
This repository uses a merged memory model:

- `context/` for live operational memory
- `raw/` for immutable source material
- `wiki/` for compiled reusable knowledge
- `docs/` for human-facing project docs
- `specs/` for product and engineering intent
- `graphify-out/` for structural code graph outputs

`/checkpoint` is the canonical maintenance command.

## Startup routing
At the start of meaningful work:
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
`/checkpoint` must:
- update `context/architecture.md`
- update `context/decisions.md`
- update `context/worklog.md`
- update `context/session-summaries/<today>.md`
- invoke `/lint`
- refresh the code graph for `src/` via `scripts/refresh_graph.py`
- record lint and graph outcomes in the daily summary

## File ownership
- Human-owned: source code, `specs/`, most of `docs/`
- Shared: `context/architecture.md`, `context/decisions.md`, `context/worklog.md`
- Claude-maintained or Claude-assisted: `context/session-summaries/`, `wiki/`, `graphify-out/`

## Placeholder project commands
Replace these with the real repo commands.

- Lint: `npm run lint`
- Test: `npm test`
- Typecheck: `npm run typecheck`
- Dev: `npm run dev`

## Constraints to update manually
Replace this section with the real stack, deployment constraints, privacy requirements, and coding conventions for the repository.

## Additional workflow commands
- Use `/ingest` to convert `raw/` material into curated `wiki/` pages.
- Use `/decision` to append durable ADR-style decisions to `context/decisions.md`.
- Use the `wiki` skill when maintaining compiled semantic knowledge.
