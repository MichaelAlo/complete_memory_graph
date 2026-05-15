# Project Nexus — Data Lake & Data Wiki Programme Plan

**Owner:** Michael Alo (Data Lake & Data Wiki)
**Architecture review:** Matt Burlage
**Last updated:** 2026-05-15

---

## Purpose of this document

This document describes what we are building, why, and in what sequence. It is written for all programme stakeholders — technical and non-technical — so that anyone on the team can understand:

- what the Data Lake and Data Wiki are
- what Michael is building and why
- what the programme needs from each team member, and when
- what is blocked and who can unblock it

If you are a module owner, source system owner, or senior reviewer, your inputs are called out explicitly in each milestone.

---

## What we are building

### The Data Lake

The Data Lake is a shared data platform that sits between source systems (like Coreflexi / Core Admin DB) and the specialist modules that consume data (Cashfluid, Sun 2.x, Moody's 2.x, HKRBC, Governance, Compliance, Transactional). It has four layers:

| Layer | What it holds | Who writes to it |
|---|---|---|
| **Raw** (`nexus_raw`) | Exact copies of source records, with PII masked at the moment of extraction | Extraction jobs (Data Lake) |
| **Standardised** (`nexus_std`) | Type-coerced, deduplicated, code-harmonised records — same shape as raw, cleaner values | Standardisation jobs (Data Lake) |
| **Curated** (`nexus_curated`) | Certified, release-tagged datasets ready for module consumption | Curated publication jobs (Data Lake) |
| **Snapshot** (`nexus_snapshot`) | Immutable point-in-time evidence for regulatory reporting and governance sign-off | Snapshot publisher (Data Lake, triggered by module owners) |

The governing rule: **no module talks directly to another module**. All inter-system exchange routes through the Lake.

### The Data Wiki

The Data Wiki is a structured set of markdown pages — one per entity, module, source system, dataset, and Lake Function — that acts as the shared definition of record for the programme. It is consumed by both humans and Claude Code agents.

Every schema change, mapping decision, or MDM definition must be reflected in the Wiki in the same release. The Wiki is not passive documentation; it is a load-bearing artefact.

---

## Build milestones

Progress gates on each milestone are listed explicitly. Work within a milestone runs in parallel where possible. Milestones unlock in sequence.

---

### Milestone 0 — Foundation ✓ Complete

**Status:** Done.

**What was built:**

- Four MySQL schemas provisioned: `nexus_raw`, `nexus_std`, `nexus_curated`, `nexus_snapshot`
- Job audit table (`nexus_raw.job_runs`) — every pipeline run is logged with run ID, timestamps, row counts, and pass/fail
- Core Admin DB extractor: date-windowed batch, PII masked at extraction boundary, idempotent upsert
- Standardisation pipeline: type coercion, deduplication, code harmonisation, quality gate
- MDM interface contract (`MDMProvider` protocol) — Shanshan's survivorship outputs plug straight in when ready
- Reference data publication: Calendar, Currency/FX, Code lists published to `nexus_curated`
- Snapshot publisher: append-only, release-tag-required, immutable evidence layer
- All five page templates for the Data Wiki
- 9 cross-cutting Wiki pages: architecture, MDM model, pipeline controls, open questions, team and timeline, and more
- 36-page Wiki coverage audit tracking all pages across entities, modules, sources, and datasets

**What this enables:** The pipeline foundation exists. Data can flow from Core Admin DB through all four layers. Module teams can start reading the Wiki and feeding back on their requirements.

---

### Milestone 1 — MDM First Wave

**Status:** In progress — blocked on Shanshan's DDL.

**What gets built in this milestone:**

- **Data Lake:** Full implementation of MDM survivorship logic (`src/curate/mdm/survivorship.py`) for Customer, Policy, Product, CoA, Currency, Calendar domains. Publication of `dim_customer`, `dim_policy`, `dim_product` to `nexus_curated`. First end-to-end pipeline run for policy and customer data.
- **Data Wiki:** Fill the canonical fields tables in all six entity pages (`wiki/entities/`). Promote entity pages from `stub` → `done` in coverage audit. Create `dim_customer.md`, `dim_policy.md`, `dim_product.md` dataset pages.

**What the programme needs — and from whom:**

| What is needed | Who | Why it unblocks |
|---|---|---|
| Canonical schema (column names, types, constraints) for all 6 first-wave MDM entities: Customer, Policy, Product, CoA, Currency/FX, Calendar | **Shanshan Gu** | Without this, the survivorship layer cannot be implemented, and the curated MDM datasets cannot be published |
| PDPO compliance sign-off on Customer entity PII masking (5 fields: name, date_of_birth, id_number, email, phone) | **Yang Mingyang** | No production extraction of customer records may run until this sign-off is received |

**Gate to unlock this milestone:**
> Shanshan delivers the MDM entity DDL. Yang Mingyang signs off the Customer PII masking implementation.

---

### Milestone 2 — Module Boundaries Confirmed

**Status:** In progress — blocked on module plans from all module owners.

**What gets built in this milestone:**

- **Data Lake:** Finalise the Lake Function vs Module Function split for all 8 modules. Confirm additional Core Admin DB tables to extract (beyond policies, customers, products). Resolve external feed assignments (Flow 1 vs Flow 2) per module. Implement any additional standardisation table configs that module plans reveal.
- **Data Wiki:** Fill all 8 module stub pages (`wiki/modules/`) with reads, writes, Lake Function dependencies, and governance interaction. Promote module pages from `stub` → `done`.

**What the programme needs — and from whom:**

| What is needed | Who | Why it unblocks |
|---|---|---|
| Written module plan covering: data inputs from the Lake, data outputs back to the Lake, specialist logic the module owns | **KJ Lin** (Cashfluid, HKRBC) | Lake Function boundary decisions; HKRBC regulatory feed inventory |
| Same module plan | **Shanshan Gu** (Sun 2.x) | Delta book design; GL journal handling; expense allocation decision |
| Same module plan | **Betty Pun** (Moody's 2.x, Compliance) | HKFRS 17 inputs; foreign currency translation; compliance sub-domain scope |
| Same module plan | **Alex Moore** (Transactional) | Policy transaction grain; what pre-aggregations the Lake should own |
| Same module plan | **Bill Nichol** (Governance) | Governance sub-domain scope; reporting snapshot cadence |
| Confirmation: CDC event log available, or must extraction stay date-windowed? | **Kai Wang** | Finalises extraction pattern for Core Admin DB |
| Confirmation: hard-delete handling in Core Admin DB | **Kai Wang** | Prevents Lake serving stale records for deleted policies |
| Confirmation: complete table list beyond policies/customers/products | **Kai Wang** (once module plans land) | Finalises `table_config.py` extraction scope |
| Decisions: expense allocation (Lake vs module), reinsurance routing, Pillar 2/3 module placement, Sun 2.x aggregation boundary | **Matt Burlage** | Scope boundary for several Lake Functions |

**Gate to unlock this milestone:**
> All 8 module plans received. Kai Wang confirms CDC mechanism and hard-delete handling. Matt Burlage signs off on the four architectural boundary decisions.

---

### Milestone 3 — First Module Integration Live

**Status:** Not started — depends on M1 and M2.

**What gets built in this milestone:**

Cashfluid is the reference implementation. The pattern established here will be reused for all other modules.

- **Data Lake:** Cashfluid reads `nexus_curated` datasets (Calendar, Currency, Policy, Customer). Cashfluid writes results back to a dedicated Lake schema (or Lake receives Cashfluid outputs into snapshot). First full cycle: raw extraction → standardisation → curated certification → module consumption → snapshot.
- **Data Wiki:** Cashfluid module page filled to `done`. First snapshot dataset page created.

**What the programme needs — and from whom:**

| What is needed | Who | Why it unblocks |
|---|---|---|
| KJ Lin confirms Cashfluid can connect to `nexus_curated` and execute against the curated schema | **KJ Lin** | End-to-end integration test |
| KJ Lin confirms what (if anything) Cashfluid writes back to the Lake | **KJ Lin** | Snapshot schema design |

**Gate to unlock this milestone:**
> M1 and M2 complete. Cashfluid integration tested end-to-end.

---

### Milestone 4 — External Feeds and Full Coverage

**Status:** Not started — depends on M2.

**What gets built in this milestone:**

- **Data Lake:** Wire up all external feed connections (Flow 1 and Flow 2). Implement `src/ingest/external/loader.py`. Publish all module-required external datasets to `nexus_curated`. Expand extraction scope to all Core Admin DB tables confirmed in M2.
- **Data Wiki:** Complete `wiki/sources/external-feeds.md` with all per-feed Flow 1/2 assignments. Promote sources and relevant dataset pages to `done`.

**What the programme needs — and from whom:**

| What is needed | Who | Why it unblocks |
|---|---|---|
| FX rate provider name and connection details | **KJ Lin + Shanshan Gu** | `src/curate/reference/currency.py` feed wiring |
| Confirmation of HKIA-prescribed FX rate sources for HKRBC capital returns | **KJ Lin** | HKRBC regulatory compliance for FX inputs |
| Inventory of all Flow 1 and Flow 2 feeds per module | All module owners (via M2 plans) | External feed loader scope |

**Gate to unlock this milestone:**
> M2 complete. All external feed details confirmed.

---

### Milestone 5 — Governance Reporting Snapshots Live

**Status:** Not started — depends on M1, M2, M3.

**What gets built in this milestone:**

- **Data Lake:** All first-wave regulatory and governance reports land as release-tagged, immutable snapshots in `nexus_snapshot`. Governance module reads from Lake and triggers snapshot publication. Compliance module integration.
- **Data Wiki:** All Wiki pages at `done`. Coverage audit: 36/36 pages complete.

**What the programme needs — and from whom:**

| What is needed | Who | Why it unblocks |
|---|---|---|
| Governance reporting schedule and report templates | **Bill Nichol** | Snapshot schema design for governance reports |
| Compliance regulatory return scope and cadence | **Betty Pun / Yang Mingyang** | Compliance snapshot schema |
| Final sign-off on snapshot immutability and access controls | **Matt Burlage** | Production readiness gate |

**Gate to unlock this milestone:**
> M1–M3 complete. All governance and compliance report specs received.

---

## Milestone dependency map

```
M0 Foundation ✓
  ├── M1 MDM First Wave
  │     ├── Gate: Shanshan's entity DDL
  │     └── Gate: Yang Mingyang's PDPO sign-off
  └── M2 Module Boundaries Confirmed
        ├── Gate: All 8 module plans
        ├── Gate: Kai Wang CDC + schema clarifications
        └── Gate: Matt Burlage architecture decisions

M1 + M2 → M3 First Module Integration Live (Cashfluid reference)
M2      → M4 External Feeds and Full Coverage
M1+M2+M3→ M5 Governance Reporting Snapshots Live
```

M1 and M2 run in parallel. M3 requires both.

---

## What every team member should know

**If you are a module owner (KJ Lin, Shanshan Gu, Betty Pun, Alex Moore, Bill Nichol):**
Your module plan is the most important input to the programme right now. Without it, the Lake cannot finalise what data to prepare, how to transform it, or what to certify. A plan does not need to be perfect — it needs to state: what data your module reads from the Lake, what data it writes back, and what specialist logic your module owns (not the Lake).

**If you are a source system owner (Kai Wang):**
The Lake's extraction jobs are built around what you can tell us about Core Admin DB. CDC vs date-windowed batch, hard-delete handling, and the full table list are the three outstanding items. Each one unlocks a part of the build.

**If you are the architecture reviewer (Matt Burlage):**
Four boundary decisions are open and affect how the Lake scopes its Lake Functions. These are listed in Milestone 2. The programme will not assume answers — your sign-off is the gate.

**If you are the PDPO/compliance reviewer (Yang Mingyang):**
No customer records — even masked — will be extracted into production until your sign-off on the masking implementation is received. This is a hard gate before M1 completes.

**If you are a technical reviewer (Luke Lai):**
Review gates apply at each milestone before promotion to the next. The pipeline has test coverage, mypy type checking, and ruff linting in the CI gate. Review requests will come with diffs and a test report.

---

## Open questions requiring a decision

| Question | Owner | Milestone gate |
|---|---|---|
| Expense allocation pre-aggregation: Lake Function or module-owned? | Matt Burlage | M2 |
| Reinsurance gross/net split: Lake transform or module-owned? | Matt Burlage | M2 |
| Pillar 2 (ORSA governance) module: HKRBC or Governance? | Matt Burlage | M2 |
| Pillar 3 (public disclosure): which module owns it? | Matt Burlage | M2 |
| Sun 2.x aggregation boundary: Sun handles internally, or Lake receives raw JE lines? | Matt Burlage + Shanshan Gu | M2 |
| FX rate provider and HKIA-prescribed rate confirmation | KJ Lin + Shanshan Gu | M4 |
| CDC mechanism available in Core Admin DB? | Kai Wang | M2 |
| Hard-delete handling in Core Admin DB | Kai Wang | M2 |
| Complete table list beyond policies/customers/products | Kai Wang + module owners | M2 |
| Flow 1 vs Flow 2 assignment for FX rates (multi-module consumer — Flow 2 assumed) | KJ Lin + Shanshan Gu | M4 |

---

## How to engage

**To submit your module plan:** Send directly to Michael Alo. Include: what your module reads from the Lake, what it writes back, and what specialist logic it owns. A short document or structured notes are both fine.

**To answer an open question:** Tag Michael Alo directly. If the question has architecture implications, loop in Matt Burlage.

**To request a schema or data change:** Raise a GitLab issue. Every schema change must update code, the Data Wiki, and lineage metadata together as one tagged release — no partial updates.

**To review a module page draft:** Michael will share a draft wiki page for your module once your module plan is received. The page is yours to review and correct before it is marked `done`.
