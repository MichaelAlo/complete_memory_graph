# Lake Functions Registry

**Sources:** `project-nexus-data-flow-architecture.html`, `project-nexus-mdm.html`, `project_nexus_handover_updated_sources.md`

---

## Purpose

This page defines the boundary between Lake Functions (owned and operated by the Data Lake team) and Module Functions (owned by each specialist module). Getting this boundary right prevents over-centralisation of specialist logic and keeps the Lake generic and maintainable.

---

## Tie-break rule

> If the logic is generic and reusable across multiple modules, it belongs in the Lake.
> If it depends on actuarial, accounting, regulatory, or transaction-specific meaning, it belongs in the module.
> If two modules would otherwise implement the same thing independently, default it into the Lake.

---

## Lake Functions — centralise these

| Function | Notes |
|---|---|
| Ingestion and intake control | Raw landing from Core Admin DB, external feeds, and module output drops |
| Standardisation and deduplication | Type coercion, dedup, format normalisation |
| Code-list harmonisation | Canonical code mapping across source systems |
| MDM survivorship | Golden-record assembly with effective-dated versioning |
| Reference-data versioning | Versioned reference tables (currencies, calendars, CoA) |
| Snapshotting | Immutable reporting snapshots with audit metadata |
| Lineage capture | Run ID, source cut, transformation version, dataset provenance |
| Data quality controls | Row-count, null, uniqueness, referential integrity, timeliness checks |
| Access governance and masking | Role-based access, PII masking, sensitive-domain restrictions |
| Generic reusable aggregations | Only when the aggregation logic is truly domain-agnostic |

---

## Module Functions — keep in modules

| Function | Module | Why it stays in the module |
|---|---|---|
| Liability cash-flow projection and scenario logic | Cashfluid | Actuarial meaning drives the logic |
| Journal validation and posting-rule logic | Sun 2.x | Posting rules are accounting-domain specific |
| Close, allocations, consolidation | Sun 2.x | Finance-domain specific |
| CSM roll-forward and RA disclosure assembly | Moody's 2.x | HKFRS17 contract-grouping and measurement rules |
| BEL, PCR, MCR, MOCE, TVOG capital logic | HKRBC | Regulatory capital formula is jurisdiction-specific |
| Deal modelling and carve-out logic | Transactional | Transaction-domain specific |
| Governance attestation and workflow logic | Governance | Compliance workflow is Governance-domain specific |

---

## Per-module boundary notes (from architecture §2)

The following detail was confirmed or flagged per module:

| Function | Sits in | Note |
|---|---|---|
| Liability cash-flow projection, ESG runs, RA/CSM input generation, stochastic scenario runs | Cashfluid | Actuarial meaning |
| Model-point grouping (clustering seriatim policies into representative model points) | Cashfluid | Future task; sits with projection logic |
| GL36-prescribed Pillar 1 stress scenarios (mortality, longevity, life CAT, morbidity, expense, lapse) | HKRBC Reporting | Applied at capital-aggregation layer, not inside Cashfluid |
| Expense allocation pre-aggregation (rolling raw GL expense data up into HKFRS17 cohort/product buckets) | **Data Lake** (to be confirmed) | Open question between Shanshan / Michael / Matt |
| Policy-level derived fields (whether to compute in Lake uniformly or keep in Cashfluid with actuarial logic) | **TBD** | Open question; Phase 5 steps written basis-agnostic |
| Journal validation against CoA & posting rules; sub-ledger GL postings; Delta book derivation | Sun 2.x | Posting rules are accounting-domain specific |
| Journal entry mapping logic; multi-GAAP conversion; FX translation | **Data Lake** | Confirmed as Lake Functions for Sun 2.x intake |
| Management reporting aggregations (statutory, financial statement, management reporting, planning/forecast) | Grey area — Sun 2.x vs Lake | Boundary not yet confirmed |
| Contract grouping, cohort assembly, CSM roll-forward, RA disclosure, OCI option handling | Moody's 2.x | HKFRS17 domain-specific |
| Segmental and group reporting | Grey area — Moody's 2.x vs Lake | Preliminary in scope; boundary needs confirmation |
| Section 24 carve-out logic, VDR/document agents, transaction-specific scenario overlays | Transactional | Transaction-domain specific |
| BEL/PCR/MCR/MOCE/TVOG capital logic; [CA.P.G.x] regulatory return generation | HKRBC Reporting | Regulatory capital formula |
| RPT flag application to every JE line | **Data Lake** | Via Counterparty lookup; Lake data-tagging service |
| ORSA governance and narrative assembly (Pillar 2) | **TBD** | Open — may sit in Governance |
| Pillar 3 public disclosure template build | **TBD** | Open — may sit in Governance or Compliance |

## Grey areas and unresolved boundaries

| Function | Current assumption | Status |
|---|---|---|
| Reinsurance gross/net split (applying treaty terms to split cashflows gross/ceded/net) | Module Function — TBD | Do not centralise until explicitly confirmed |
| Expense allocation pre-aggregation into HKFRS17 cohort buckets | Lake Function — but to be confirmed | Active open question (Shanshan / Michael / Matt) |
| Policy-level derived fields | TBD — Lake vs Cashfluid | Phase 5 basis-agnostic until resolved |
| Management reporting aggregations in Sun 2.x | Grey area | Check with Sun 2.x / Data Lake leads |
| Pillar 2 / Pillar 3 placement | Unclear whether Governance, Compliance, or Strategy | Open — flagged as unresolved |

---

## Practical exception

Some functions that architecturally belong in the Lake may temporarily remain in Coreflexi if reporting-period deadlines or team capacity make that the only realistic short-term option. These must be:
- Explicitly triaged and logged (GitLab issue).
- Given a migration target date.
- Treated as technical debt, not as a permanent boundary decision.

---

## How to use this page

When designing a new pipeline job or evaluating where logic should live:
1. Check the tie-break rule.
2. Check the grey-area table for the specific function.
3. If still unclear, consult the relevant module owner and record the decision in `context/decisions.md` via `/decision`.
