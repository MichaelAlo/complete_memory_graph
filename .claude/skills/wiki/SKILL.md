---
name: wiki
description: Maintain compiled project knowledge in wiki/ by ingesting raw materials, de-duplicating pages, and preserving reusable facts.
---

# Wiki Maintenance Skill

Use this skill when maintaining or expanding the compiled knowledge base in `wiki/`.

## Purpose
`wiki/` is the curated semantic layer of the repository. It should contain stable, reusable, high-signal knowledge rather than raw notes.

## Inputs
Relevant sources may include:
- `raw/`
- `context/architecture.md`
- `context/decisions.md`
- `specs/`
- `docs/`
- source code when needed for verification

## Rules
- One topic per page when practical.
- Prefer updating existing pages over creating duplicates.
- De-duplicate aggressively.
- Preserve provenance and note uncertainty.
- Keep pages concise, skimmable, and structured.
- When a wiki update changes project understanding, also update `context/architecture.md` or `context/decisions.md`.

## Typical outputs
- topic summaries
- subsystem notes
- terminology pages
- integration notes
- distilled research pages
