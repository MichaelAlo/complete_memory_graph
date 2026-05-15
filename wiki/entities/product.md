# Entity: Product

**Domain:** First-wave
**Source of record:** Core Admin DB (Coreflexi) + product reference data
**Data owner:** Michael Alo (Data Lake)
**Last reviewed:** 2026-05-15

---

## Business definition

A Product is an insurance product type offered by MPL. Product is mastered centrally because:
- Product classification drives HKFRS17 cohort grouping (BBA / VFA / PAA measurement model)
- Product type determines capital treatment in HKRBC (GL36 PCA modular approach)
- Consistent product codes across modules prevent measurement and reporting discrepancies
- Product lifecycle (active, discontinued) affects in-force reporting

---

## Canonical fields

<!-- MDM: update when DDL confirmed — Shanshan to provide final schema ~2026-05-22 -->

| Field | Type | Required | PII | Masked | Description |
|---|---|---|---|---|---|
| canonical_id | CHAR(36) | yes | no | — | Lake-issued UUID |
| product_id | INT | yes | no | — | Source key from Core Admin DB |
| product_code | VARCHAR(40) | yes | no | — | Short code used in policy records and CoA mapping |
| product_type | VARCHAR(40) | yes | no | — | Insurance product category (e.g. universal-life, term, endowment) |
| hkfrs17_model | VARCHAR(10) | no | no | — | HKFRS17 measurement model: BBA / VFA / PAA |
| status | VARCHAR(20) | yes | no | — | active / discontinued |
| effective_from | DATE | yes | no | — | Start of this SCD version |
| effective_to | DATE | no | no | — | End of this SCD version; NULL = current |
| created_at | DATETIME(6) | yes | no | — | Row creation timestamp |
| updated_at | DATETIME(6) | yes | no | — | Row last-updated timestamp |
| provenance | VARCHAR(80) | yes | no | — | Source system supplying surviving attributes |

---

## Effective dating

Type 2 SCD: `effective_from` / `effective_to`. Product re-classification (e.g. change of HKFRS17 model) creates a new version row; prior version is retained for retrospective measurement.

---

## Source system keys

| Source system | Key column | Notes |
|---|---|---|
| Core Admin DB | product_id | Integer PK in Coreflexi products table |

---

## PII and masking rules

Product records contain no PII.

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| Cashfluid | Model point construction; product-level assumption grouping |
| Moody's 2.x | HKFRS17 cohort grouping by product and measurement model |
| HKRBC | Product classification for GL36 capital treatment |
| Sun 2.x | CoA mapping; journal tagging by product line |
| Governance | Product-level disclosures |

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| canonical_id uniqueness | uniqueness | 0 duplicates | block promotion |
| product_id not null | completeness | 0 nulls | block promotion |
| product_code not null | completeness | 0 nulls | block promotion |
| hkfrs17_model in valid set | validity | {BBA, VFA, PAA, null} | warn |

---

## Open items

- Canonical field DDL to be confirmed by Shanshan Gu (~2026-05-22)
- Confirm HKFRS17 model classification per product with Betty Pun (Moody's 2.x lead)
- Confirm whether product classification is a Lake Function or a Cashfluid responsibility (see `wiki/open-questions.md`)

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created — fields stub pending MDM DDL | Michael Alo | — |
