# Module: Governance

**Lead:** Bill Nichol
**Co-lead:** Betty Pun
**Tech reviewer:** Luke Lai
**Status:** Not started (slower timeline)
**Last reviewed:** 2026-05-15

> Full sub-domain detail: see [governance-compliance-detail.md](../governance-compliance-detail.md)

---

## What this module owns

Governance owns all user-facing reporting and oversight surfaces. It owns:
- Risk and capital governance (model validation, risk appetite, board reporting)
- Conduct and ethics governance
- Operational governance (DOA — Delegation of Authority matrices)
- Board and committee governance (board packs, minutes, meeting workflows)
- Audit and attestation backbone (attestation workflows, evidence management)

**Key rule:** Governance owns the reporting *marts* (user-facing surfaces); the Data Lake owns the immutable *snapshots* and evidence trail behind them.

---

## Reads from Lake

| Dataset | Schema | Purpose |
|---|---|---|
| Certified curated outputs | nexus_curated | Inputs for reporting marts |
| Report snapshots | nexus_snapshot | Evidence artefacts for board and audit use |
| MDM golden records (Customer, Policy, Product, etc.) | nexus_curated | Entity lookups for governance reporting |
| dim_calendar | nexus_curated | Period labelling in board packs |

---

## Writes back to Lake

| Dataset | Schema | Content |
|---|---|---|
| Attestation evidence metadata | nexus_snapshot | Attestation records (if required) |

Governance is primarily a downstream consumer — it does not feed other operational modules.

---

## Lake Functions this module depends on

- **Snapshot publication** — all evidence stored in nexus_snapshot with release tag before Governance consumes
- **Access governance / masking** — Governance users have governed read access; PII-restricted views apply
- **Lineage capture** — full audit trail from source to governance output required for attestation

---

## Module dependency notes

- Governance is **downstream-only** — it does not produce data consumed by Cashfluid, Sun 2.x, Moody's 2.x, or HKRBC
- Exception: model validation approvals from Governance flow back as signals to Cashfluid / HKRBC / Moody's 2.x (approval, not data)

---

## Open items

<!-- stub: update after module plan lands 2026-05-18 -->

- Full Governance module plan due 2026-05-18 (described as slower timeline — may lag)
- Governance app-to-module binding in practice: detailed workflow not yet designed (Bill Nichol to lead)
- Pillar 2 (ORSA) placement: HKRBC vs Governance? (see open-questions.md)
- Pillar 3 (public disclosure) placement: Governance / Compliance / Strategy (see open-questions.md)
- Board pack and attestation workflow design: not started

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub — full detail in governance-compliance-detail.md | Michael Alo | — |
