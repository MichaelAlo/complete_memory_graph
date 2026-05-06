# /decision

Capture a durable architecture or product decision in `context/decisions.md`.

## Goal
Record a decision as an ADR-style entry with enough context to be reusable later.

## Read phase
Read:
- `CLAUDE.md`
- `context/decisions.md`
- relevant files in `context/architecture.md`, `specs/`, `docs/`, or `wiki/`

## Entry format
Append a new decision entry containing:
- date
- title
- status
- context
- decision
- rationale
- consequences
- supersedes or superseded-by links if relevant

## Rules
- Record only durable decisions, not transient preferences.
- If the decision reverses an earlier one, say so explicitly.
- Keep language factual and compact.
- If the evidence is insufficient, state that the decision is provisional.

## Final response
Return:
- decision title
- affected files
- whether an earlier decision was superseded
