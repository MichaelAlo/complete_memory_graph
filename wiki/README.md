# wiki/

Compiled knowledge derived from `raw/` source documents and stable project facts. All pages are synthesized — do not copy raw HTML content here.

The Data Wiki is a **load-bearing artefact**, not passive documentation. It is consumed by Claude Code agents and human contributors to keep definitions of sources, canonical entities, mappings, lineage, and methodology aligned across the programme.

See [coverage-audit.md](coverage-audit.md) for the full page inventory and gap tracker.

---

## Cross-cutting pages

| Page | Contents |
|---|---|
| [architecture-overview.md](architecture-overview.md) | Platform stance, layer model, hub-and-spoke pattern, end-to-end flow, reporting split |
| [mdm-operating-model.md](mdm-operating-model.md) | First-wave domains, canonical model rules, zones/certification, governance roles, change-control workflow |
| [lake-functions-registry.md](lake-functions-registry.md) | Lake vs Module boundary, tie-break rule, per-module boundary detail, grey areas |
| [module-binding-register.md](module-binding-register.md) | Per-module read/write/Governance binding; Sun 2.x Delta book design; Flow 1 vs Flow 2 |
| [pipeline-and-controls.md](pipeline-and-controls.md) | Idempotency, run context, orchestration stance, validation controls, logging fields, security |
| [open-questions.md](open-questions.md) | Unresolved boundary and delivery questions with owners and deadlines |
| [team-and-timeline.md](team-and-timeline.md) | Module leads, company context (PACE/MPL), key deadlines, tech review workflow |
| [cashfluid-project-phases.md](cashfluid-project-phases.md) | Cashfluid 5-phase plan (reference implementation), milestones, Lake integration detail |
| [governance-compliance-detail.md](governance-compliance-detail.md) | Governance sub-domains (5) and Compliance sub-domains (4) with inputs/outputs/Lake Functions |

---

## Templates

Reusable page templates. Use the relevant template whenever creating a new page.

| Template | Use for |
|---|---|
| [templates/entity.md](templates/entity.md) | One per MDM mastered domain (Customer, Policy, etc.) |
| [templates/module.md](templates/module.md) | One per consuming module |
| [templates/source.md](templates/source.md) | One per upstream source system |
| [templates/dataset.md](templates/dataset.md) | One per certified curated table or report |
| [templates/lake-function.md](templates/lake-function.md) | One per named Lake Function category |

---

## MDM entity pages

| Page | Domain | Status |
|---|---|---|
| [entities/customer.md](entities/customer.md) | Customer | Stub — fields pending MDM DDL (~2026-05-22) |
| [entities/policy.md](entities/policy.md) | Policy | Stub — fields pending MDM DDL (~2026-05-22) |
| [entities/product.md](entities/product.md) | Product | Stub — fields pending MDM DDL (~2026-05-22) |
| [entities/chart-of-accounts.md](entities/chart-of-accounts.md) | CoA mapping | Stub — fields pending MDM DDL (~2026-05-22) |
| [entities/currency-fx.md](entities/currency-fx.md) | Currency / FX rates | Stub |
| [entities/calendar.md](entities/calendar.md) | Calendar | Stub |

---

## Source system pages

| Page | Source | Status |
|---|---|---|
| [sources/core-admin-db.md](sources/core-admin-db.md) | Core Admin DB (Coreflexi) | Stub — CDC mechanism to confirm with Kai Wang |
| [sources/external-feeds.md](sources/external-feeds.md) | External feeds (Flow 1 + Flow 2) | Stub — per-feed assignments open |

---

## Module pages

| Page | Module | Lead | Status |
|---|---|---|---|
| [modules/cashfluid.md](modules/cashfluid.md) | Cashfluid | KJ Lin | Stub → see cashfluid-project-phases.md |
| [modules/sun-2x.md](modules/sun-2x.md) | Sun 2.x | Shanshan Gu | Stub — fill after 2026-05-18 |
| [modules/moodys-2x.md](modules/moodys-2x.md) | Moody's 2.x | Betty Pun | Stub — fill after 2026-05-18 |
| [modules/hkrbc.md](modules/hkrbc.md) | HKRBC Reporting | KJ Lin | Stub — fill after 2026-05-18 |
| [modules/transactional.md](modules/transactional.md) | Transactional | Alex Moore | Stub — fill after 2026-05-18 |
| [modules/governance.md](modules/governance.md) | Governance | Bill Nichol | Stub → see governance-compliance-detail.md |
| [modules/compliance.md](modules/compliance.md) | Compliance | Betty Pun / Yang Mingyang | Stub → see governance-compliance-detail.md |
| [modules/coreflexi.md](modules/coreflexi.md) | Coreflexi | Kai Wang | Stub |

---

## Curated dataset pages

| Page | Dataset | Schema | Status |
|---|---|---|---|
| [datasets/dim_calendar.md](datasets/dim_calendar.md) | dim_calendar | nexus_curated | Stub |
| [datasets/dim_currency.md](datasets/dim_currency.md) | dim_currency | nexus_curated | Stub |
| [datasets/ref_codelist.md](datasets/ref_codelist.md) | ref_codelist | nexus_curated | Stub |

---

## Wiki change triggers

When any of the following events happens, the listed wiki pages must be updated in the **same release**:

| Change type | Wiki pages that must update |
|---|---|
| New source table extracted | `sources/core-admin-db.md`, `coverage-audit.md` |
| New MDM entity DDL confirmed | Relevant `entities/*.md` (fill fields table, remove `<!-- MDM: update when DDL confirmed -->`) |
| New curated dataset published | New `datasets/<name>.md`, `coverage-audit.md` |
| Module plan lands | Relevant `modules/<module>.md` (fill stub, remove stub marker) |
| Lake Function boundary confirmed | `lake-functions-registry.md` |
| ADR recorded | `context/decisions.md` + affected wiki pages |
| Open question resolved | `open-questions.md` (move to answered table) |

---

## Last ingested / updated

2026-05-15 — Full pass:
- `project-nexus-data-flow-architecture.html` — initial ingestion
- `project-nexus-mdm.html` — initial ingestion
- `project_nexus_handover_updated_sources.md` — initial ingestion
- `nexus_architecture.html` — sections 2, 3, 4.1–4.6, 5.1–5.10, 6 extracted via grep/awk
- Wiki build Phase W1–W5: templates, coverage audit, source pages, entity pages, module stubs, dataset pages

2026-05-15 — Targeted re-pass (ingest §4.6):
- `nexus_architecture.html` §4.6 — External Data Ingestion Module initial-wave feed inventory
- Updated `sources/external-feeds.md`: enriched Flow 2 inventory (HKIA templates, regulatory guidance, SOA experience studies, reinsurer tables, PEP lists); split sanctions/PEP; added specific Flow 1 entries from §5.3
