# Entity: Currency / FX Rates

**Domain:** First-wave
**Source of record:** External reference data provider (Flow 1 feed)
**Data owner:** Michael Alo (Data Lake)
**Last reviewed:** 2026-05-15

---

## Business definition

Currency and FX rate data provides daily exchange rates used for liability valuation, asset retranslation, and regulatory capital calculation. It is mastered centrally because:
- Multiple modules (Sun 2.x, HKRBC, Moody's 2.x) require consistent FX rates for the same reporting period
- Rate inconsistency across modules creates reconciliation failures in financial close and capital returns
- HKIA prescribes specific rate sources for some regulatory outputs (confirm with KJ Lin)

The Lake holds two related reference datasets:
1. **Currency master** — list of supported currencies with ISO codes
2. **FX rates** — daily rates per currency pair relative to HKD (reporting currency)

---

## Canonical fields

<!-- MDM: update when DDL confirmed -->

### Currency master

| Field | Type | Required | Description |
|---|---|---|---|
| currency_code | CHAR(3) | yes | ISO 4217 currency code (e.g. HKD, USD, EUR) |
| currency_name | VARCHAR(80) | yes | Full name |
| is_reporting_currency | TINYINT(1) | yes | 1 = HKD (reporting currency); 0 = foreign |
| status | VARCHAR(20) | yes | active / inactive |
| effective_from | DATE | yes | Start of this SCD version |
| effective_to | DATE | no | End of this SCD version; NULL = current |

### FX rates (implemented in nexus_curated.dim_currency)

| Field | Type | Required | Description |
|---|---|---|---|
| currency_code | CHAR(3) | yes | Source currency ISO code |
| rate_date | DATE | yes | Effective date for this rate |
| rate_to_hkd | DECIMAL(18,8) | yes | Rate: 1 unit of currency_code = rate_to_hkd HKD |
| _run_id | CHAR(36) | yes | Lineage: extraction run ID |
| _source_cut | VARCHAR(64) | yes | Extract cut boundary |
| _release_tag | VARCHAR(64) | yes | Release tag for this publication |
| _certified_at | DATETIME(6) | yes | Certification timestamp |

---

## Effective dating

FX rates are not versioned via Type 2 SCD — each `(currency_code, rate_date)` pair is unique and immutable once published. The currency master uses Type 2 SCD for currency lifecycle changes.

---

## Source system keys

| Source system | Key column | Notes |
|---|---|---|
| External provider (TBC) | currency_code + rate_date | Provider TBC — module owners to confirm |

---

## PII and masking rules

FX rate data contains no PII.

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| Sun 2.x | FX retranslation for multi-currency GL entries |
| HKRBC | Asset and liability valuation in HKD for capital returns |
| Moody's 2.x | HKFRS17 foreign currency translation |
| Cashfluid | Projection inputs for non-HKD business |
| Governance | Reporting period FX rates for board packs |

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| (currency_code, rate_date) uniqueness | uniqueness | 0 duplicates | block promotion |
| rate_to_hkd > 0 | validity | all positive | block promotion |
| HKD/HKD rate = 1.0 | validity | exactly 1.0 | block promotion |
| No missing dates in reporting period | completeness | 0 gaps for active currencies | warn |

---

## Open items

- External FX rate provider to be confirmed by module owners (KJ Lin + Shanshan Gu)
- Confirm whether Flow 1 (direct-to-module) or Flow 2 (via Lake) is appropriate — given multi-module consumption, Flow 2 is assumed but not yet formally assigned (see `wiki/open-questions.md`)
- Confirm HKIA-prescribed rate sources for HKRBC regulatory returns with KJ Lin

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created | Michael Alo | — |
