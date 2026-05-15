# Module: HKRBC Reporting

**Lead:** KJ Lin
**Tech reviewer:** Luke Lai
**Status:** In-build
**Last reviewed:** 2026-05-15

---

## What this module owns

HKRBC Reporting owns Hong Kong Risk-Based Capital Pillar 1 calculations and regulatory returns. It owns:
- PCA (Prescribed Capital Assessment) modular calculations under GL36 (HKIA Guideline 36)
- BEL (Best Estimate Liabilities), PCR (Prescribed Capital Requirement), MCR (Minimum Capital Requirement)
- MOCE (Margin Over Current Estimate) and TVOG (Time Value of Options and Guarantees)
- HKRBC regulatory return preparation and submission
- Journal generation for HKRBC book in Sun 2.x

---

## Reads from Lake

| Dataset | Schema | Purpose |
|---|---|---|
| Cashfluid outputs (BEL, TVOG, MOCE) | nexus_curated | Pillar 1 liability inputs |
| ESG scenarios (1,000 scenarios) | nexus_curated | Stochastic capital calculations |
| Assumption sets from Cashfluid | nexus_curated | Capital projection assumptions |
| Asset data | nexus_curated | Asset risk charge inputs |
| Regulatory templates | nexus_curated | HKIA return scaffolding |
| dim_policy (mastered) | nexus_curated | Policy-level capital attribution |
| dim_product (mastered) | nexus_curated | Product capital treatment under GL36 |
| dim_calendar | nexus_curated | Reporting period anchoring |
| dim_currency | nexus_curated | FX rates for capital calculation |

---

## Writes back to Lake

| Dataset | Schema | Content |
|---|---|---|
| Capital outputs | nexus_curated | PCR, MCR, MOCE results |
| HKRBC journal feeds | nexus_curated | Capital JEs for Sun 2.x HKRBC book |
| Regulatory return data | nexus_curated | Return-ready capital figures |
| Submission evidence | nexus_snapshot | Immutable regulatory submission artefacts |

---

## Lake Functions this module depends on

- **Cashfluid outputs** — BEL, TVOG, MOCE, 1,000 ESG scenarios must be published before HKRBC can run
- **MDM survivorship** — Policy and Product golden records for capital attribution
- **Reference data publication** — Currency/FX, Calendar, regulatory templates
- **Snapshot publication** — submission evidence frozen with release tag
- **Lineage capture** — full audit trail from input scenarios to capital output

---

## Governance interaction

HKRBC Reporting produces:
- ORSA (Own Risk and Solvency Assessment) evidence (Pillar 2 — placement TBD, see open questions)
- Regulatory returns submitted to HKIA
- Capital journal feeds to Sun 2.x for HKRBC book posting
- Submission artefacts frozen to nexus_snapshot

---

## Module dependency notes

- **HKRBC depends on Cashfluid** — BEL/TVOG/MOCE and 1,000 ESG scenarios must complete first
- **HKRBC does not depend on Moody's 2.x** — runs independently; Sun 2.x derives Delta book from both
- **Sun 2.x depends on HKRBC journal outputs** for Delta book derivation

---

## Open items

<!-- stub: update after module plan lands 2026-05-18 -->

- Full HKRBC module plan due 2026-05-18
- Pillar 2 (ORSA governance) placement: HKRBC vs Governance? (see open-questions.md)
- Pillar 3 (public disclosure templates) placement across Governance / Compliance / Strategy (see open-questions.md)
- HKIA-prescribed FX rate sources for capital returns — confirm with KJ Lin

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub from module-binding-register.md | Michael Alo | — |
