# Entity: Customer

**Domain:** First-wave
**Source of record:** Core Admin DB (Coreflexi)
**Data owner:** Michael Alo (Data Lake) — with PDPO review by Yang Mingyang (Compliance)
**Last reviewed:** 2026-05-15

---

## Business definition

A Customer is an individual or organisation that holds or has applied for one or more insurance policies with MPL. Customer is the central identity entity across all modules. It is mastered centrally in the Lake because:
- Multiple source systems may hold partial customer records
- PDPO (Hong Kong Personal Data Privacy Ordinance) requires PII to be governed at a single control point
- Customer identity is needed for RPT (Related-Party Transaction) tagging, Governance disclosures, and Compliance reporting

---

## Canonical fields

<!-- MDM: update when DDL confirmed — Shanshan to provide final schema ~2026-05-22 -->

| Field | Type | Required | PII | Masked | Description |
|---|---|---|---|---|---|
| canonical_id | CHAR(36) | yes | no | — | Lake-issued UUID; primary identifier |
| customer_id | INT | yes | no | — | Source key from Core Admin DB |
| status | VARCHAR(20) | yes | no | — | active / inactive / merged |
| effective_from | DATE | yes | no | — | Start of this version |
| effective_to | DATE | no | no | — | End of this version; NULL = current |
| created_at | DATETIME(6) | yes | no | — | Row creation timestamp |
| updated_at | DATETIME(6) | yes | no | — | Row last-updated timestamp |
| provenance | VARCHAR(80) | yes | no | — | Winning source system |
| name | VARCHAR | yes | **yes** | `***` | Customer full name — **masked at extraction** |
| date_of_birth | DATE | no | **yes** | `***` | Date of birth — **masked at extraction** |
| id_number | VARCHAR | no | **yes** | `***` | HKID or passport number — **masked at extraction** |
| email | VARCHAR | no | **yes** | `***` | Email address — **masked at extraction** |
| phone | VARCHAR | no | **yes** | `***` | Phone number — **masked at extraction** |

---

## Effective dating

Type 2 SCD: `effective_from` / `effective_to` (`effective_to = NULL` means current open version).
A new version row is created on any change to survivorship-relevant attributes.

---

## Source system keys

| Source system | Key column | Notes |
|---|---|---|
| Core Admin DB | customer_id | Integer PK in Coreflexi customers table |

---

## PII and masking rules

**PDPO classification:** Customer records are Personal Data under Hong Kong's Personal Data Privacy Ordinance (PDPO). The following fields are masked at the extraction boundary in `src/ingest/core_admin/extract.py:_mask_pii()`:

| Field | PDPO basis | Masking method | Stored in Lake? |
|---|---|---|---|
| name | Personal data (identity) | Replaced with `***` | No — never lands in any Lake schema |
| date_of_birth | Personal data (identity) | Replaced with `***` | No — never lands in any Lake schema |
| id_number | Sensitive personal data (HKID/passport) | Replaced with `***` | No — never lands in any Lake schema |
| email | Personal data (contact) | Replaced with `***` | No — never lands in any Lake schema |
| phone | Personal data (contact) | Replaced with `***` | No — never lands in any Lake schema |

Access to unmasked customer data requires explicit PDPO-compliant authorisation. No unmasked PII exists inside the Nexus boundary.

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| Governance | Customer-level disclosures, RPT identification |
| Compliance | PDPO obligations, AML/CFT screening |
| Moody's 2.x | Policy-level grouping (customer ↔ policy join) |
| Cashfluid | Model points requiring customer attributes |
| Transactional | Counterparty identification for M&A/Section 24 |

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| canonical_id uniqueness | uniqueness | 0 duplicates | block promotion |
| customer_id not null | completeness | 0 nulls | block promotion |
| status in valid set | validity | {active, inactive, merged} | block promotion |
| PII fields all masked | integrity | 0 unmasked values | block promotion + alert |

---

## Open items

- Canonical field DDL to be confirmed by Shanshan Gu (~2026-05-22) — update fields table above
- Confirm whether additional PII fields exist in Core Admin DB beyond the 5 listed above (Kai Wang to confirm)
- PDPO masking review required by Yang Mingyang before first production run

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created — fields stub pending MDM DDL | Michael Alo | — |
