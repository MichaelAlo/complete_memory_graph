# Wiki Coverage Audit

Last updated: 2026-05-15

Track the status of every wiki page. Update this file whenever a page is created, filled, or becomes stale.

| Status values: `done` = complete and reviewed; `stub` = page exists but content incomplete; `missing` = page not yet created |

---

## Cross-cutting pages (9)

| Page | Type | Status | Owner | Notes |
|---|---|---|---|---|
| architecture-overview.md | cross-cutting | done | Michael Alo | |
| mdm-operating-model.md | cross-cutting | done | Michael Alo | |
| lake-functions-registry.md | cross-cutting | done | Michael Alo | |
| module-binding-register.md | cross-cutting | done | Michael Alo | |
| pipeline-and-controls.md | cross-cutting | done | Michael Alo | |
| open-questions.md | cross-cutting | done | Michael Alo | Active tracking doc — keep current |
| team-and-timeline.md | cross-cutting | done | Michael Alo | |
| cashfluid-project-phases.md | cross-cutting | done | Michael Alo | Reference implementation detail |
| governance-compliance-detail.md | cross-cutting | done | Michael Alo | |

## Templates (5)

| Page | Type | Status | Owner | Notes |
|---|---|---|---|---|
| templates/entity.md | template | done | Michael Alo | |
| templates/module.md | template | done | Michael Alo | |
| templates/source.md | template | done | Michael Alo | |
| templates/dataset.md | template | done | Michael Alo | |
| templates/lake-function.md | template | done | Michael Alo | |

## MDM entity pages (6 first-wave)

| Page | Type | Status | Owner | Notes |
|---|---|---|---|---|
| entities/customer.md | entity | stub | Michael Alo | Fields stub — update when Shanshan's DDL lands (~2026-05-22) |
| entities/policy.md | entity | stub | Michael Alo | Fields stub — update when Shanshan's DDL lands (~2026-05-22) |
| entities/product.md | entity | stub | Michael Alo | Fields stub — update when Shanshan's DDL lands (~2026-05-22) |
| entities/chart-of-accounts.md | entity | stub | Michael Alo | Fields stub — update when Shanshan's DDL lands (~2026-05-22) |
| entities/currency-fx.md | entity | stub | Michael Alo | Reference data; fields can be defined sooner |
| entities/calendar.md | entity | stub | Michael Alo | Reference data; fields can be defined sooner |

## Source system pages (2)

| Page | Type | Status | Owner | Notes |
|---|---|---|---|---|
| sources/core-admin-db.md | source | stub | Kai Wang | CDC mechanism to confirm with Kai |
| sources/external-feeds.md | source | stub | Michael Alo | Per-dataset Flow 1 vs Flow 2 assignment open |

## Module pages (8)

| Page | Type | Status | Owner | Notes |
|---|---|---|---|---|
| modules/cashfluid.md | module | stub | KJ Lin | Links to cashfluid-project-phases.md; fill after 2026-05-18 |
| modules/sun-2x.md | module | stub | Shanshan Gu | Fill after module plan lands 2026-05-18 |
| modules/moodys-2x.md | module | stub | Betty Pun | Fill after module plan lands 2026-05-18 |
| modules/hkrbc.md | module | stub | KJ Lin | Fill after module plan lands 2026-05-18 |
| modules/transactional.md | module | stub | Alex Moore | Fill after module plan lands 2026-05-18 |
| modules/governance.md | module | stub | Bill Nichol | Links to governance-compliance-detail.md |
| modules/compliance.md | module | stub | Betty Pun / Yang Mingyang | Links to governance-compliance-detail.md |
| modules/coreflexi.md | module | stub | Kai Wang | Outside Nexus boundary; coordinate with Kai |

## Curated dataset pages

| Page | Type | Status | Owner | Notes |
|---|---|---|---|---|
| datasets/dim_calendar.md | dataset | stub | Michael Alo | Schema from sql/03_curated_reference.sql |
| datasets/dim_currency.md | dataset | stub | Michael Alo | Provider TBC; Flow 1/2 assignment open |
| datasets/ref_codelist.md | dataset | stub | Michael Alo | Schema from sql/03_curated_reference.sql |
| datasets/dim_customer.md | dataset | missing | Michael Alo | Deferred — after Shanshan's MDM DDL |
| datasets/dim_policy.md | dataset | missing | Michael Alo | Deferred — after Shanshan's MDM DDL |
| datasets/dim_product.md | dataset | missing | Michael Alo | Deferred — after Shanshan's MDM DDL |

---

## Coverage summary

| Type | Total | Done | Stub | Missing |
|---|---|---|---|---|
| Cross-cutting | 9 | 9 | 0 | 0 |
| Templates | 5 | 5 | 0 | 0 |
| MDM entities | 6 | 0 | 6 | 0 |
| Source systems | 2 | 0 | 2 | 0 |
| Modules | 8 | 0 | 8 | 0 |
| Datasets | 6 | 0 | 6 | 0 |
| **Total** | **36** | **14** | **22** | **0** |

---

## Wiki change triggers

When one of these events happens, the listed wiki pages must be updated in the same release.

| Change type | Wiki pages that must update |
|---|---|
| New source table extracted | `sources/core-admin-db.md`, this file |
| New MDM entity DDL confirmed | Relevant `entities/*.md` (fill fields table, remove stub marker) |
| New curated dataset published | New `datasets/<name>.md`, this file |
| Module plan lands | Relevant `modules/<module>.md` (fill stub sections) |
| Lake Function boundary confirmed | `lake-functions-registry.md` |
| ADR recorded | `context/decisions.md` + affected wiki pages |
| Open question resolved | `open-questions.md` (move to answered table) |
