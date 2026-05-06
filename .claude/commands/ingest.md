# /ingest

Compile source material from `raw/` into reusable knowledge in `wiki/`.

## Goal
Turn immutable source material into curated, high-signal project knowledge.

## Read phase
Read:
- `CLAUDE.md`
- relevant files under `raw/`
- relevant pages already present under `wiki/`
- `context/decisions.md` and `context/architecture.md` if they affect interpretation

## Rules
- Treat `raw/` as evidence, not polished truth.
- Do not copy large chunks verbatim from source material.
- Synthesize, normalize, de-duplicate, and cross-reference.
- Prefer one topic per wiki page.
- Update existing wiki pages when the topic already exists instead of creating near-duplicates.
- Record uncertainty explicitly if the source material is incomplete or conflicting.

## Output expectations
For each ingestion pass:
- create or update one or more pages in `wiki/`
- preserve important source provenance inside the wiki page
- keep wiki pages concise, structured, and reusable
- if ingestion changes project understanding materially, update `context/decisions.md` or `context/architecture.md`

## Final response
Return:
- source files reviewed
- wiki pages created or updated
- unresolved ambiguities
- recommended next ingestion target
