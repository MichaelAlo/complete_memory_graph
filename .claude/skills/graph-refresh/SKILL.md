---
name: graph-refresh
description: Refresh the structural graph for src/ and summarize the result
---

Refresh the structural graph for `src/`.

Default implementation:
- Run `python3 scripts/refresh_graph.py`

Requirements:
- State whether graph refresh succeeded.
- State where the graph artifacts were written.
- If refresh falls back to a file index, say that explicitly.
- If refresh fails, report the blocking error.
