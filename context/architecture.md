# Architecture

## Current system

MySQL-first curated analytics platform. Four logical layers, each a dedicated MySQL schema. Python jobs move data between layers. GitLab holds all SQL, Python, mappings, MDM definitions, Wiki pages, changelogs, and release tags.

## MySQL schemas

| Schema | Layer | Promotion rule |
|---|---|---|
| `nexus_raw` | Raw | Ingestion-validated only. No business reinterpretation. |
| `nexus_std` | Standardised | Schema, format, and completeness checks pass. |
| `nexus_curated` | Curated | Reconciliation + lineage + owner approval + quality threshold. |
| `nexus_snapshot` | Reporting snapshot | Generated only from certified curated outputs; release-tagged. |

Module-owned state lives in separate module schemas (`cashfluid_*`, `sun_*`, `moodys_*`, etc.) — not in the shared Lake schemas.

## Source layout

```
sql/
  01_schemas.sql           Four-schema DDL (CREATE DATABASE IF NOT EXISTS)
  02_audit.sql             nexus_raw.job_runs audit table
  03_curated_reference.sql dim_calendar, dim_currency, ref_codelist DDL
  04_snapshot.sql          nexus_snapshot.rpt_policy_in_force DDL
scripts/
  provision_db.py          Runs sql/ files against configured DB
src/
  config/
    settings.py            Config dataclass; reads from environment + source DB fields
  lib/
    db.py                  MySQL connection factory (context manager, cast-typed)
    run_context.py         RunContext: run_id, extract_cut, release_tag, logging
    job_log.py             log_run_start / log_run_complete → nexus_raw.job_runs
  ingest/
    core_admin/
      extract.py           Date-windowed batch extraction; PII masking; idempotent upsert
      table_config.py      TABLES dict (TableConfig dataclass per table)
    external/
      loader.py            External feed loader stub; supports Flow 1 and Flow 2
  standardise/
    pipeline.py            Type coercion, dedup, code-list harmonisation → nexus_std
    table_config.py        TABLE_CONFIG per source table (type_map, required_fields, etc.)
    errors.py              StandardisationGateError
  curate/
    mdm/
      survivorship.py      MasteredRecord dataclass + assembly stub (MDMProvider contract)
      contracts.py         MDMProvider Protocol — typed interface for Shanshan's outputs
    reference/
      calendar.py          Publish dim_calendar reference data
      currency.py          Publish dim_currency FX rates
      codelist.py          Publish ref_codelist code mappings
    publish.py             Certified dataset publication → nexus_curated
  snapshot/
    publisher.py           Reporting snapshot generation → nexus_snapshot (append-only)
  quality/
    checks.py              Row-count, null, uniqueness checks (_fetch_int helper)
    reconcile.py           Source-to-target reconciliation (_fetch_scalar helper)
tests/
  test_quality_checks.py
  test_run_context.py
  test_extract.py
  test_standardise_pipeline.py
  test_snapshot.py
wiki/
  templates/               5 page templates (entity, module, source, dataset, lake-function)
  entities/                6 MDM entity pages (all stub — fields pending Shanshan's DDL)
  modules/                 8 module pages (all stub — fill after 2026-05-18 plans)
  sources/                 2 source system pages (core-admin-db, external-feeds; both stub)
  datasets/                3 dataset pages (dim_calendar, dim_currency, ref_codelist; stub)
  coverage-audit.md        36-page tracking table; 14 done, 22 stub, 0 missing
  README.md                Wiki index with change-trigger table
```

## End-to-end flow

```
Core Admin DB ──CDC──► nexus_raw ──standardise──► nexus_std ──MDM+curate──► nexus_curated
External feeds ─────────────┘                                                      │
                                                                              Modules consume
                                                                              Module outputs ──► nexus_raw (controlled interface)
                                                                              nexus_curated ──snapshot──► nexus_snapshot ──► Governance
```

## Major modules

- `src/`: primary codebase root; all Python pipeline code.
- `context/`: live operational memory (architecture, decisions, worklog, session summaries).
- `raw/`: immutable source HTML and markdown reference documents.
- `wiki/`: compiled reusable knowledge (ingested from `raw/` via `/ingest`).
- `graphify-out/`: structural graph outputs for `src/`.
- `specs/`: product and engineering intent documents.

## Lake Functions (owned by Data Lake team)

Ingestion · Standardisation · Deduplication · Code-list harmonisation · MDM survivorship · Reference-data versioning · Snapshotting · Lineage capture · Data quality controls · Access governance and masking · Generic reusable aggregations only.

## Module Functions (owned by each module)

Cashfluid liability cash-flow projection · Sun 2.x journal validation and posting-rule logic · Moody's 2.x CSM roll-forward and disclosure assembly · HKRBC capital logic (BEL, PCR, MCR, MOCE, TVOG) · Transactional deal modelling · Governance attestation and workflow logic.

## Invariants

- `/checkpoint` updates architecture, decisions, worklog, daily summary, lint result, and graph state together.
- Structural graph refreshes target `src/` only.
- PII is masked before any record leaves Core Admin DB extraction.
- All jobs carry a `run_id`, `extract_cut`, and `release_tag` for full replay.
- No module-to-module direct links; all exchange routes through the Lake.
