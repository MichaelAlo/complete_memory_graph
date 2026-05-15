# /wiki

Create or update a wiki page for a named artefact (entity, module, dataset, source system, or Lake Function).

## Goal
Keep the Data Wiki in sync with the code, schema, and MDM state. Every artefact that the pipeline touches should have a corresponding wiki page.

## Read phase
Before writing or updating:
1. Read `wiki/coverage-audit.md` — find the target page's current status
2. Read `wiki/templates/<type>.md` — use the appropriate template for the page type
3. Read the relevant source page(s) if updating existing content (entity, module, or dataset page)
4. Read `context/decisions.md` if the artefact is affected by recent ADRs
5. Read `wiki/open-questions.md` if the artefact has unresolved questions

## Page types and templates

| Type | Template | Directory |
|---|---|---|
| MDM entity | `wiki/templates/entity.md` | `wiki/entities/` |
| Module | `wiki/templates/module.md` | `wiki/modules/` |
| Source system | `wiki/templates/source.md` | `wiki/sources/` |
| Curated dataset | `wiki/templates/dataset.md` | `wiki/datasets/` |
| Lake Function | `wiki/templates/lake-function.md` | `wiki/` (or a future `wiki/functions/`) |

## Rules
- Use the template for the relevant page type. Do not deviate from the template structure.
- Stub fields that are not yet confirmed — mark with `<!-- stub: reason -->` or `<!-- MDM: update when DDL confirmed -->`.
- Do not invent facts. If something is unknown, say so explicitly and note who can confirm it.
- Cross-link to related pages (e.g. a dataset page links to its entity page; a module page links to its source pages).
- Every new or updated page must include a Change history entry.
- If the artefact has an open question in `open-questions.md`, link to it from the Open items section.

## Output expectations
After creating or updating a wiki page:
1. Update `wiki/coverage-audit.md` — change the status from `missing` → `stub` or `stub` → `done`
2. Update `wiki/README.md` — add or update the page entry in the relevant table
3. If a new subdirectory was created, update the README to reference it

## Final response
Return:
- Page created or updated (path)
- Coverage audit change
- Any open items surfaced that need owner follow-up
- Whether any related pages should also be updated (flag, do not update without asking)
