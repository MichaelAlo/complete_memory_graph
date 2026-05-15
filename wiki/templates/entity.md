# Entity: [Name]

**Domain:** [First-wave / Second-wave]
**Source of record:** [Core Admin DB / external / reference]
**Data owner:** [person]
**Last reviewed:** [date]

---

## Business definition

[What this entity represents in insurance operations and why it is mastered centrally.]

---

## Canonical fields

<!-- MDM: update when DDL confirmed -->

| Field | Type | Required | PII | Masked | Description |
|---|---|---|---|---|---|
| canonical_id | CHAR(36) | yes | no | — | Lake-issued primary identifier (UUID) |
| business_key | VARCHAR | yes | no | — | Natural business identifier from source |
| status | VARCHAR(20) | yes | no | — | active / inactive / merged |
| effective_from | DATE | yes | no | — | Start of this version (Type 2 SCD) |
| effective_to | DATE | no | no | — | End of this version; NULL = current |
| created_at | DATETIME(6) | yes | no | — | Row creation timestamp |
| updated_at | DATETIME(6) | yes | no | — | Row last-updated timestamp |
| provenance | VARCHAR(80) | yes | no | — | Source system supplying surviving attributes |

---

## Effective dating

Type 2 SCD: `effective_from` / `effective_to` (`effective_to = NULL` means current open version).
A new version row is created whenever a survivorship-relevant attribute changes.
Prior versions are retained indefinitely for audit and retrospective reporting.

---

## Source system keys

| Source system | Key column | Notes |
|---|---|---|
| [source] | [key_column] | |

---

## PII and masking rules

[List any PII fields. For each: PDPO classification, masking rule applied at extraction boundary, access restriction.]

---

## Downstream consumers

[Which modules and curated datasets consume this entity. List with purpose.]

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| canonical_id uniqueness | uniqueness | 0 duplicates | block promotion |
| status validity | validity | in {active, inactive, merged} | block promotion |
| effective_from ≤ effective_to | referential | — | block promotion |

---

## Open items

[Unresolved questions — link to `wiki/open-questions.md` entries where applicable.]

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
