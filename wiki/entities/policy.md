# Entity: Policy

**Domain:** First-wave
**Source of record:** Core Admin DB (Coreflexi)
**Data owner:** Michael Alo (Data Lake)
**Last reviewed:** 2026-05-15

---

## Business definition

A Policy is a contract between MPL and a customer for an insurance product. Policy is the central grain entity for actuarial, finance, and regulatory reporting. It is mastered centrally because:
- Policy data is the primary input to Cashfluid (liability projection), Moody's 2.x (HKFRS17 measurement), HKRBC (capital calculation), and Sun 2.x (journal posting)
- Consistent policy identification across modules prevents double-counting and reconciliation failures
- Policy lifecycle (in-force, lapsed, matured, surrendered, death-claim) drives different reporting treatments in each module

---

## Canonical fields

<!-- MDM: update when DDL confirmed — Shanshan to provide final schema ~2026-05-22 -->

| Field | Type | Required | PII | Masked | Description |
|---|---|---|---|---|---|
| canonical_id | CHAR(36) | yes | no | — | Lake-issued UUID |
| policy_id | INT | yes | no | — | Source key from Core Admin DB |
| customer_id | INT | yes | no | — | FK to canonical Customer entity |
| product_code | VARCHAR(40) | yes | no | — | FK to canonical Product entity |
| status | VARCHAR(20) | yes | no | — | active / lapsed / surrendered / matured / death-claim |
| inception_date | DATE | yes | no | — | Policy start date |
| effective_from | DATE | yes | no | — | Start of this SCD version |
| effective_to | DATE | no | no | — | End of this SCD version; NULL = current |
| created_at | DATETIME(6) | yes | no | — | Row creation timestamp |
| updated_at | DATETIME(6) | yes | no | — | Row last-updated timestamp |
| provenance | VARCHAR(80) | yes | no | — | Source system supplying surviving attributes |

Canonical status codes (source → canonical mapping in `src/standardise/table_config.py`):

| Source code | Canonical code |
|---|---|
| A | active |
| L | lapsed |
| S | surrendered |
| M | matured |
| D | death-claim |

---

## Effective dating

Type 2 SCD: `effective_from` / `effective_to` (`effective_to = NULL` = current version).
Status transitions and product/customer re-linking trigger new version rows.

---

## Source system keys

| Source system | Key column | Notes |
|---|---|---|
| Core Admin DB | policy_id | Integer PK in Coreflexi policies table |

---

## PII and masking rules

Policy records contain no direct PII. Customer identity is linked via `customer_id` FK; the customer record itself is the PII-bearing entity (see `entities/customer.md`).

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| Cashfluid | Model points; liability projection inputs |
| Moody's 2.x | HKFRS17 cohort grouping; BBA/VFA/PAA classification |
| HKRBC | BEL calculation inputs; Pillar 1 capital |
| Sun 2.x | Journal posting linkage; CoA mapping |
| Governance | In-force reporting; disclosure artefacts |
| Compliance | RPT register linkage; regulatory filings |

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| canonical_id uniqueness | uniqueness | 0 duplicates | block promotion |
| policy_id not null | completeness | 0 nulls | block promotion |
| status in valid set | validity | {active, lapsed, surrendered, matured, death-claim} | block promotion |
| inception_date not null | completeness | 0 nulls | block promotion |
| customer_id referential integrity | referential | no orphan FKs | warn |

---

## Open items

- Canonical field DDL to be confirmed by Shanshan Gu (~2026-05-22)
- Confirm full list of policy status codes in Core Admin DB with Kai Wang
- Confirm which policy-level derived fields (e.g. cohort grouping for HKFRS17) belong in the Lake vs Cashfluid (see `wiki/open-questions.md`)

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created — fields stub pending MDM DDL | Michael Alo | — |
