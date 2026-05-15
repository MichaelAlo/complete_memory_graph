# Project Nexus — Data Lake

MySQL-first curated analytics platform acting as the integration backbone for Project Nexus. Centralises ingestion, standardisation, MDM, lineage, access control, data quality, and immutable reporting snapshots across all Nexus modules.

## Platform stance

- **Not a lakehouse.** A controlled curated analytics backbone that behaves operationally like a Data Lake.
- **MySQL-first.** Structured storage with Python pipeline jobs and GitLab-managed definitions.
- **Hub-and-spoke.** No point-to-point links between modules; all inter-system exchange goes through the Lake.
- **Azure deferred.** Cloud-native migration only if MySQL storage/concurrency or orchestration complexity genuinely forces it.

## Layer model

| Layer | Schema | Purpose |
|---|---|---|
| Raw | `nexus_raw` | Faithful ingestion landing — no reinterpretation |
| Standardised | `nexus_std` | Typed, cleaned, deduplicated, conformed |
| Curated | `nexus_curated` | Certified reusable datasets, MDM golden records |
| Reporting snapshot | `nexus_snapshot` | Immutable, versioned evidence behind published reports |

## Module binding

| Module | Reads from Lake | Writes back to Lake |
|---|---|---|
| Coreflexi / Core Admin DB | — (upstream source only) | One-way raw feed |
| Cashfluid | Policy, assumptions, scenarios, reference data | ECF, scenario outputs, measurement inputs |
| Sun 2.x | Journal feeds, mapping inputs, reference data | Posted entries, balances, close outputs |
| Moody's 2.x | Cashfluid outputs, expense feeds, reference data | Disclosures, journals, roll-forward outputs |
| Transactional | Portfolio and counterparty reference data | Deal outputs and evidence sets |
| HKRBC Reporting | Actuarial inputs, asset data, regulatory templates | Capital outputs, return data, journal outputs |
| Governance | Certified outputs and report snapshots | Attestation metadata |

## Source layout

```
src/
  config/         DB and environment settings
  lib/            DB connection, run context, structured logging
  ingest/         Core Admin DB extraction; external feed loading
  standardise/    Typing, dedup, code-list harmonisation
  curate/         MDM survivorship; certified dataset publication
  snapshot/       Reporting snapshot generation
  quality/        Row-count, null, uniqueness, referential, reconciliation checks
tests/            Pytest test suite
```

## Commands

| Task | Command |
|---|---|
| Lint | `ruff check .` |
| Format | `ruff format .` |
| Type check | `mypy src/` |
| Test | `pytest` |
| Install (dev) | `pip install -e ".[dev]"` |

## Session workflow

- Start every session: `/resume`
- End every session: `/checkpoint`
- Ingest raw material to wiki: `/ingest`
- Record a durable decision: `/decision`

## First-wave MDM domains

Customer · Policy · Product · Chart of Accounts mapping · Currency / FX calendars · Calendar

## Key principles

- All ingestion and publication jobs must be idempotent and rerunnable.
- No data-methodology change is complete until code, Wiki, MDM, lineage metadata, and approvals are all updated in the same release.
- PII from Core Admin DB is masked before landing in the Lake.
- Reporting snapshots stay inside the Data Lake boundary even when marts live in Governance.
