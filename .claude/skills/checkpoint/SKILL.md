---
name: checkpoint
description: Update semantic memory, run lint, and refresh structural graph
---

Execute the full checkpoint workflow.

## Step 1: inspect recent state
Review the relevant code changes and recent conversation context.
Read as needed:
- `context/architecture.md`
- `context/decisions.md`
- `context/worklog.md`
- latest file in `context/session-summaries/`

## Step 2: update semantic memory
Update these files carefully:
- `context/architecture.md` only if architectural understanding changed materially
- `context/decisions.md` only if a durable decision was made
- `context/worklog.md` with current state, blockers, and next actions
- today's file under `context/session-summaries/` with done, decisions, current state, next steps, open questions

Rules:
- Keep updates concise, factual, and retrieval-friendly.
- Add dates where useful.
- Do not duplicate content unnecessarily.
- Do not convert `architecture.md` into a chronological log.

## Step 3: quality gate
Invoke `/lint`.
If lint fails, continue the workflow but report the failure explicitly.

## Step 4: structural memory refresh
Invoke `/graph-refresh`.
Refresh only the graph derived from `src/`.
If graph refresh falls back or fails, report that explicitly.

## Step 5: final report
Return a compact report with:
- files updated
- lint result
- graph refresh result
- unresolved issues
- whether the checkpoint is fully successful or only partial
