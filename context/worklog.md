# Worklog

## Current focus

Project Nexus Data Lake — pipeline implementation complete (Phases 1–5). Data Wiki build complete (Phases W1–W5). Programme plan rewritten as stakeholder-facing milestone document.

## Status as of 2026-05-15 (session 2)

### Data Lake — done
- SQL DDL: all four schemas + audit table + curated reference DDL + snapshot DDL
- Extraction: Core Admin DB date-windowed batch, PII masked, idempotent upsert, job_runs logging
- Standardisation: type coercion, dedup, code-list harmonisation, quality gate, StandardisationGateError
- Curated publication: Calendar, Currency/FX, Code list fully implemented; MDMProvider Protocol ready for Shanshan's DDL
- Snapshot publisher: append-only, release_tag required, UUID-keyed
- Tests: 5 test files covering extract, standardise, snapshot, quality, run_context

### Data Wiki — done (stubs)
- 36 pages tracked in coverage-audit.md: 14 done (cross-cutting + templates), 22 stubs, 0 missing
- All entity, module, source, dataset pages exist as stubs — content pending external inputs
- Wiki README updated with change-trigger table and directory index

### Programme plan — done
- `plans/data-lake-build.md` rewritten as stakeholder-facing milestone document
- Covers M0 (complete) through M5; names every external dependency per milestone

## Blockers

| Blocker | Owner | Milestone |
|---|---|---|
| MDM entity DDL (Customer, Policy, Product, CoA, Currency, Calendar) | Shanshan Gu | M1 |
| PDPO sign-off on Customer PII masking implementation | Yang Mingyang | M1 |
| Module plans from all 8 module owners | KJ Lin, Shanshan Gu, Betty Pun, Alex Moore, Bill Nichol | M2 |
| CDC mechanism + hard-delete handling confirmation | Kai Wang | M2 |
| 4 architectural boundary decisions (expense alloc, reinsurance, Pillar 2/3, Sun 2.x boundary) | Matt Burlage | M2 |
| FX rate provider confirmation | KJ Lin + Shanshan Gu | M4 |
| MySQL DB connection not yet validated end-to-end (no .env configured) | Michael Alo | M1 |

## Next steps

1. Configure `.env` with MySQL credentials and run `python scripts/provision_db.py` to provision all four schemas.
2. Validate end-to-end pipeline with a test Core Admin DB connection.
3. Follow up on module plans (due 2026-05-18) — escalate to Matt Burlage if any missing by 2026-05-19.
4. When Shanshan's MDM DDL lands (~2026-05-22): implement `src/curate/mdm/survivorship.py`, create `dim_customer.md`, `dim_policy.md`, `dim_product.md` wiki pages, promote 6 entity pages to `done`.

## Completed

- 2026-05-06: Merged memory scaffold created.
- 2026-05-15 session 1: Project Nexus context initialized. Python package scaffolded. CLAUDE.md, README, context files updated.
- 2026-05-15 session 2: Full pipeline implementation (Phases 1–5). Full Data Wiki build (Phases W1–W5). Programme plan rewritten as stakeholder document. CLAUDE.md updated with PM role, /wiki and /pm commands, wiki page types.
