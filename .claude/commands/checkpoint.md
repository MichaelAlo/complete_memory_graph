# /checkpoint

Run the full merged maintenance workflow for this repository.

## Required read phase
Read:
- `CLAUDE.md`
- `context/project-overview.md`
- `context/architecture.md`
- `context/decisions.md`
- `context/worklog.md`
- the latest file in `context/session-summaries/` if one exists

Inspect:
- changed files
- current branch
- recent commits if helpful
- current contents of `src/`

## Required updates
Update these files based on the actual current repository state:
- `context/architecture.md`
- `context/decisions.md`
- `context/worklog.md`
- `context/session-summaries/{{TODAY}}.md`

### Rules
- `architecture.md`: enduring technical structure only
- `decisions.md`: append durable decisions, reversals, and rationale
- `worklog.md`: current status, blockers, next steps
- `session-summaries/{{TODAY}}.md`: today's work, outcomes, failures, open questions

## Validation step
Invoke `/lint`.
Capture pass/fail and the key issues.

## Graph refresh step
Run:
- `python3 scripts/refresh_graph.py`

If Graphify is installed, the script should update real graph artifacts.
If Graphify is unavailable, the fallback artifact should still update `graphify-out/refresh-status.json`.

## Final recording
Append lint status and graph refresh status to `context/session-summaries/{{TODAY}}.md`.
Update `context/worklog.md` with any unresolved failures or next actions.

## Final response
Return:
- files updated
- lint result
- graph refresh result
- blockers
- next step
