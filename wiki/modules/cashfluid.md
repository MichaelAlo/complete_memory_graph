# Module: Cashfluid

**Lead:** KJ Lin
**Tech reviewer:** Luke Lai
**Status:** In-build (Phase 2 active)
**Last reviewed:** 2026-05-15

> Full project detail: see [cashfluid-project-phases.md](../cashfluid-project-phases.md)

---

## What this module owns

Cashfluid is the actuarial liability projection platform. It owns:
- Liability cashflow projection logic (ECF — Expected Cash Flows)
- ALM (Asset-Liability Management) and KRD (Key Rate Duration) matching engine
- SAA (Strategic Asset Allocation) optimisation
- ESG (Economic Scenario Generator) scenario management
- Assumption framework (mortality, lapse, expense, etc.)
- MOCE, BEL, TVOG outputs for HKRBC and HKFRS17 measurement

---

## Reads from Lake

| Dataset | Schema | Purpose |
|---|---|---|
| dim_policy (mastered) | nexus_curated | Model point construction |
| dim_product (mastered) | nexus_curated | Product-level assumption grouping |
| dim_calendar | nexus_curated | Projection period anchoring |
| dim_currency | nexus_curated | FX rates for non-HKD business |
| Expense data | nexus_curated | Expense allocation inputs |
| Assumption tables (via Lake API) | nexus_curated | Published assumption sets |
| Scenario library (ESG) | nexus_curated | Stochastic and deterministic scenarios |
| ref_codelist | nexus_curated | Code list harmonisation |

---

## Writes back to Lake

| Dataset | Schema | Content |
|---|---|---|
| ECF outputs | nexus_curated | Expected cashflows per policy block per scenario |
| RA inputs | nexus_curated | Risk adjustment calculation inputs |
| Scenario outputs | nexus_curated | BEL, TVOG, MOCE per scenario set |
| Projection run snapshots | nexus_snapshot | Immutable run evidence with release tag |

---

## Lake Functions this module depends on

- **Ingestion + standardisation** — policy, product, customer data landed and standardised before Cashfluid reads
- **MDM survivorship** — golden-record Policy and Product entities consumed as model points
- **Reference data publication** — Calendar, Currency/FX, Assumption tables published to nexus_curated
- **Snapshot publication** — projection run outputs frozen to nexus_snapshot with release tag
- **Lineage capture** — run_id traceability from source data to projection output
- **Data quality checks** — input validation gates (completeness, uniqueness) before Cashfluid run

---

## Governance interaction

Cashfluid outputs are evidence for:
- HKFRS17 measurement (Moody's 2.x consumes ECF)
- HKRBC Pillar 1 capital (HKRBC Reporting consumes BEL, TVOG, MOCE)
- Board and regulatory submissions (snapshots stored in nexus_snapshot)

---

## Module dependency notes

- **Cashfluid must complete before Moody's 2.x** — ECF outputs are required inputs for HKFRS17 measurement
- **Cashfluid must complete before HKRBC Reporting** — BEL/TVOG/MOCE are required for capital returns
- Cashfluid does not depend on outputs from Moody's 2.x or HKRBC

---

## Open items

<!-- stub: see cashfluid-project-phases.md for full detail -->

- Phase 5 Lake integration detail (10 Lake Functions) documented in cashfluid-project-phases.md
- Policy-level derived fields: Lake (uniform) vs Cashfluid (with actuarial logic) — open (see open-questions.md)
- Expense allocation pre-aggregation: Lake Function or Cashfluid? — open (see open-questions.md)

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub — full detail in cashfluid-project-phases.md | Michael Alo | — |
