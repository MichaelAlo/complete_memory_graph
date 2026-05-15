# Source: External Feeds

**Owner:** Michael Alo (Data Lake team) — per-feed module owner for direct feeds
**Extraction patterns:** Flow 1 (direct-to-module) and Flow 2 (External Ingestion Module → Lake → consumers)
**PII present:** Possible in some feeds (e.g. sanctions lists) — assess per feed
**Last reviewed:** 2026-05-15

> External data enters the Lake through one of two approved paths. External providers never receive direct read or write access to a Nexus-controlled database.

---

## Flow definitions

| Flow | When to use | Extraction owner |
|---|---|---|
| **Flow 1: Direct-to-Module** | Stable, professionally structured, contract-based feeds consumed by a single or few modules | Module owner (with Lake team oversight) |
| **Flow 2: External Ingestion Module → Lake → consumers** | Ad hoc, multi-consumer, or quality-variable datasets requiring shared validation, standardisation, versioning, and lineage | Data Lake team |

Flow 2 avoids each consuming module reimplementing extraction, validation, and versioning for the same external data.

---

## Feed inventory

### Flow 1 feeds (direct-to-module)

Per-dataset Flow 1 routing applies where the source publishes a stable API or professionally structured feed with guaranteed quality/schema, and consumption is limited to one or a few modules.

| Feed | Provider | Consuming module | Owner | Cadence | Landing | Status |
|---|---|---|---|---|---|---|
| Public market data (rates / FX / indices / proxy ESG) | TBC | Cashfluid | KJ Lin | Daily | Direct to Cashfluid | Open — provider TBC |
| In-house risk-neutral ESG codebase | Internal | Cashfluid | Matt Burlage | Per-run | Direct to Cashfluid | Cashfluid Phase 2 |
| Asset-manager real-world projections + proxy asset curves | External asset managers | Cashfluid | KJ Lin | Per-run | Direct to Cashfluid | Open — provider TBC |
| Regulator-published reference rates (e.g. HKIA discount curves) | HKIA / HKMA | HKRBC, Cashfluid | KJ Lin | Per publication | Direct to module | Open — not yet assigned |

### Flow 2 feeds (via External Ingestion Module → Lake)

Per-dataset Flow 2 routing applies where: (a) structure or quality varies by source, (b) multiple Nexus modules consume the same dataset, or (c) the data is reusable reference material.

| Feed | Provider | Consuming modules | Owner | Cadence | Landing table | Status |
|---|---|---|---|---|---|---|
| HKIA regulatory return templates | HKIA | HKRBC Reporting, Compliance | KJ Lin | Per publication | nexus_raw.hkia_templates | Open — not yet implemented |
| HKFRS17 / HKRBC regulatory guidance text | HKIA | Moody's 2.x, HKRBC, Compliance | Michael Alo | Per publication | nexus_raw.regulatory_guidance | Open — not yet implemented |
| SOA mortality and lapse experience studies | Society of Actuaries / HKIA | Cashfluid, HKRBC Reporting | KJ Lin | Periodic | nexus_raw.experience_study | Open — not yet implemented |
| Reinsurer experience tables | Reinsurance partners | Cashfluid, Transactional | KJ Lin | Per treaty cycle | nexus_raw.reinsurer_experience | Open — not yet implemented |
| Sanctions lists | TBC (regulatory / OFAC / etc.) | Compliance, Governance, Transactional | Yang Mingyang | Per update | nexus_raw.sanctions_list | Open — not yet implemented |
| PEP (Politically Exposed Persons) lists | TBC | Compliance, Governance, Transactional | Yang Mingyang | Per update | nexus_raw.pep_list | Open — not yet implemented |
| ESG reference datasets (scenario calibration) | TBC | Cashfluid, Strategy | Michael Alo | Periodic | nexus_raw.esg_data | Open — not yet implemented |

---

## Implementation

Flow 2 extraction is handled by `src/ingest/external/loader.py` (currently a stub). Each Flow 2 feed will have a config entry and a `flow2_extract()` call that:
1. Receives the raw file or API payload
2. Validates structure and format
3. Writes to the designated `nexus_raw.*` table with standard landing columns (`_run_id`, `_source_cut`, `_loaded_at`)
4. Logs the run to `nexus_raw.job_runs`

---

## Per-feed Flow 1 vs Flow 2 assignment

Per-dataset Flow 1 vs Flow 2 assignment is an open question — each feed must be formally assigned in MDM. See `wiki/open-questions.md`.

The assignment decision criteria:
- **Flow 1** if: stable contract-based feed; single or very few consuming modules; professionally structured with no quality concerns
- **Flow 2** if: ad hoc or irregular; multiple consumers; quality-variable; requires shared validation and versioning

---

## Open items

- Formal per-dataset Flow 1 vs Flow 2 assignment to be recorded in MDM (see `wiki/open-questions.md`)
- All feed providers in the inventory above are TBC — module owners to confirm
- `src/ingest/external/loader.py` is a stub — implement when first Flow 2 feed is confirmed

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created from architecture docs | Michael Alo | — |
| 2026-05-15 | Enriched feed inventory with initial-wave Flow 2 list from nexus_architecture.html §4.6; split sanctions/PEP; added Flow 1 specifics from §5.3 | Michael Alo | — |
