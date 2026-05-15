# Module: Transactional

**Lead:** Alex Moore
**Co-lead:** Rui Huang
**Tech reviewer:** Luke Lai
**Status:** In-build
**Last reviewed:** 2026-05-15

---

## What this module owns

Transactional owns deal evaluation, structuring, and governance for portfolio transfers and M&A activity. It owns:
- Deal evaluation and financial modelling
- Section 24 (portfolio transfer) deal structuring
- VDR (Virtual Data Room) document generation and management
- Deal governance and approvals

---

## Reads from Lake

| Dataset | Schema | Purpose |
|---|---|---|
| dim_policy (mastered) | nexus_curated | Portfolio composition for deal evaluation |
| Counterparty MDM | nexus_curated | Counterparty reference data for deal structuring |
| dim_product (mastered) | nexus_curated | Product composition of transferred portfolios |
| dim_currency | nexus_curated | Deal valuation FX rates |

---

## Writes back to Lake

| Dataset | Schema | Content |
|---|---|---|
| Deal outputs | nexus_curated | Deal evaluation results and evidence (as needed) |
| Diligence artefacts | nexus_snapshot | Due diligence evidence sets with release tag |

---

## Lake Functions this module depends on

- **MDM survivorship** — Policy, Product, Counterparty golden records for portfolio analysis
- **Snapshot publication** — deal evidence frozen to nexus_snapshot with release tag
- **Lineage capture** — portfolio composition traceability

---

## Governance interaction

Transactional produces:
- Deal memos and diligence evidence stored in nexus_snapshot
- Section 24 regulatory evidence for HKIA

---

## Open items

<!-- stub: update after module plan lands 2026-05-18 -->

- Full Transactional module plan due 2026-05-18
- Confirm Counterparty MDM scope: first-wave or second-wave? (currently assumed second-wave unless Transactional confirms immediate need)
- VDR integration pattern: Flow 1 or separate artefact management?

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub from module-binding-register.md | Michael Alo | — |
