# /resume

Reconstruct the current project state before beginning meaningful work.

## Required read phase
Read:
- `CLAUDE.md`
- `context/project-overview.md`
- `context/worklog.md`
- the latest file in `context/session-summaries/` if one exists
- `graphify-out/GRAPH_REPORT.md` if present

Read when relevant:
- `context/architecture.md`
- `context/decisions.md`
- `context/domain-notes.md`
- `context/people-and-stakeholders.md`

## Required inspection
Inspect:
- current branch
- changed files
- recent commits if helpful
- current source roots listed in `context/architecture.md` or `scripts/refresh_graph.py`

## Final response
Return:
- files loaded
- current objective
- relevant architecture or decision context
- current blockers
- next 3 concrete actions
- any missing or stale memory that should be fixed before or during the session

## Rules
- Do not make code changes during `/resume` unless the user explicitly asks.
- Prefer concise state reconstruction over broad exploration.
- If the memory files are still placeholders, say that clearly and recommend the first setup action.
