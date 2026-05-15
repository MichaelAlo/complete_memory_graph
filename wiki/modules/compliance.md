# Module: Compliance

**Lead:** Betty Pun (co-lead), Yang Mingyang (co-lead)
**Tech reviewer:** Luke Lai
**Status:** In-build (several boundaries still open)
**Last reviewed:** 2026-05-15

> Full sub-domain detail: see [governance-compliance-detail.md](../governance-compliance-detail.md)

---

## What this module owns

Compliance owns regulatory obligations, data privacy, RPT filings, and non-Pillar-1 HKIA returns. It owns:
- Regulatory compliance framework (AML/CFT, PDPO, HKIA licensing obligations)
- Data and privacy compliance (PDPO Data Protection Principles, consent management, DPIA)
- RPT (Related-Party Transaction) Register management
- Non-Pillar-1 HKIA regulatory returns (Pillar 3 placement TBD)

---

## Reads from Lake

| Dataset | Schema | Purpose |
|---|---|---|
| Governed curated outputs | nexus_curated | Regulatory reporting inputs |
| Counterparty MDM (is_related_party) | nexus_curated | RPT register source |
| Sanctions lists (via Flow 2) | nexus_raw / nexus_std | AML/CFT screening |
| dim_customer (masked) | nexus_curated | PDPO obligations — masked records only |
| dim_policy | nexus_curated | Policy-level compliance reporting |

---

## Writes back to Lake

| Dataset | Schema | Content |
|---|---|---|
| TBD — several boundaries still open | TBD | TBD |

---

## Lake Functions this module depends on

- **Access governance / masking** — PDPO-compliant masked views required for all customer data access
- **RPT tagging service** — Lake applies `is_related_party` to JE lines from MDM Counterparty entity; Compliance owns the RPT Register
- **Snapshot publication** — regulatory filing evidence frozen with release tag
- **Flow 2 ingestion** — sanctions lists and external compliance reference data

---

## Governance interaction

Compliance is primarily a downstream consumer. It provides:
- PDPO compliance evidence (attestation artefacts)
- RPT disclosure filings to HKIA
- Regulatory return data to Governance for board-level oversight

---

## Open items

<!-- stub: update after module plan lands 2026-05-18 -->

- Full Compliance module plan due 2026-05-18
- Compliance module boundaries are partially specified — several Lake vs Module decisions remain open (see open-questions.md)
- Pillar 3 (public disclosure) placement: Compliance vs Governance vs Strategy (see open-questions.md)
- PDPO masking review of customer entity: Yang Mingyang to confirm before first production run

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub — full detail in governance-compliance-detail.md | Michael Alo | — |
