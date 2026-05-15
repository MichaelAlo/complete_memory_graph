# Entity: Chart of Accounts (CoA) Mapping

**Domain:** First-wave
**Source of record:** Sun 2.x
**Data owner:** Shanshan Gu (Data Lake co-lead / Sun 2.x lead)
**Last reviewed:** 2026-05-15

---

## Business definition

The Chart of Accounts (CoA) mapping is the canonical finance account code structure used across Sun 2.x, Moody's 2.x, and reporting outputs. It is mastered centrally because:
- CoA consistency is a prerequisite for Sun 2.x to write back to the Lake reliably
- Moody's 2.x consumes the CoA for HKFRS17 journal classification
- Inconsistent account codes across systems cause reconciliation failures in financial close

**Note:** This is an MDM entity for the *mapping layer* between source-system account codes and canonical Lake account codes — not the full chart of accounts hierarchy maintained in Sun 2.x itself.

---

## Canonical fields

<!-- MDM: update when DDL confirmed — Shanshan to provide final schema ~2026-05-22 -->

| Field | Type | Required | PII | Masked | Description |
|---|---|---|---|---|---|
| canonical_id | CHAR(36) | yes | no | — | Lake-issued UUID |
| source_system | VARCHAR(40) | yes | no | — | System this code comes from (e.g. sun_2x, core_admin) |
| source_account_code | VARCHAR(40) | yes | no | — | Account code in the source system |
| canonical_account_code | VARCHAR(40) | yes | no | — | Canonical Lake account code |
| account_name | VARCHAR(120) | yes | no | — | Human-readable account name |
| account_type | VARCHAR(40) | no | no | — | Asset / Liability / Equity / Revenue / Expense |
| status | VARCHAR(20) | yes | no | — | active / deprecated |
| effective_from | DATE | yes | no | — | Start of this SCD version |
| effective_to | DATE | no | no | — | End of this SCD version; NULL = current |
| created_at | DATETIME(6) | yes | no | — | Row creation timestamp |
| updated_at | DATETIME(6) | yes | no | — | Row last-updated timestamp |

---

## Effective dating

Type 2 SCD. Account code changes (reclassification, deprecation) create new version rows; prior versions are retained for retrospective period-close reconciliation.

---

## Source system keys

| Source system | Key column | Notes |
|---|---|---|
| Sun 2.x | account_code | Sun 2.x CoA hierarchy code |

---

## PII and masking rules

CoA mapping records contain no PII.

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| Sun 2.x | Consistent account coding for journal posting and GL close |
| Moody's 2.x | HKFRS17 journal classification and disclosure mapping |
| Governance | Management reporting and board pack account labelling |
| HKRBC | Capital return account mapping |

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| canonical_id uniqueness | uniqueness | 0 duplicates | block promotion |
| canonical_account_code not null | completeness | 0 nulls | block promotion |
| source_account_code not null | completeness | 0 nulls | block promotion |
| No orphan mappings (source code must exist in source system snapshot) | referential | 0 orphans | warn |

---

## Open items

- Canonical CoA DDL to be confirmed by Shanshan Gu (~2026-05-22)
- Confirm account_type taxonomy with Shanshan and Betty Pun
- Confirm whether Sun 2.x CoA changes require a Data Lake release or can be applied between releases

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created — fields stub pending MDM DDL | Michael Alo | — |
