# Dataset: dim_currency

**Schema:** nexus_curated
**Owner:** Michael Alo (Data Lake)
**Refresh cadence:** Daily (aligned with business day FX fixing)
**Release tag required:** Yes
**Last reviewed:** 2026-05-15

---

## Business purpose

`dim_currency` holds daily FX rates (expressed as units of each currency per 1 HKD) for all currencies active in MPL's insurance business. It is the shared FX reference used by all modules requiring currency translation.

---

## Schema summary

| Column | Type | Description | Source |
|---|---|---|---|
| currency_code | CHAR(3) | ISO 4217 currency code — composite PK col 1 | External feed |
| rate_date | DATE | Rate effective date — composite PK col 2 | External feed |
| rate_to_hkd | DECIMAL(18,8) | Rate: 1 unit of currency = this many HKD | External feed |
| _run_id | CHAR(36) | Publication run ID (lineage) | Pipeline |
| _source_cut | VARCHAR(64) | Extract cut for this publication | Pipeline |
| _release_tag | VARCHAR(64) | Release tag | Pipeline |
| _certified_at | DATETIME(6) | Certification timestamp | Pipeline |

**Full DDL:** [sql/03_curated_reference.sql](../../sql/03_curated_reference.sql)

---

## Lineage

```
External FX rate provider (TBC — Flow 1 assumed)
  → src/curate/reference/currency.py   (publication)
  → nexus_curated.dim_currency
```

External provider and flow assignment (Flow 1 vs Flow 2) are open — see open items.

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| (currency_code, rate_date) uniqueness | uniqueness | 0 duplicates | block promotion |
| rate_to_hkd > 0 | validity | all positive | block promotion |
| HKD/HKD rate = 1.0 exactly | validity | = 1.0 | block promotion |
| No missing dates in reporting period | completeness | 0 gaps for active currencies | warn |

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| Sun 2.x | FX retranslation for multi-currency GL entries |
| Moody's 2.x | Foreign currency HKFRS17 translation |
| HKRBC Reporting | Asset and liability FX valuation for capital returns |
| Cashfluid | Non-HKD projection inputs |
| Governance | FX rates for board pack disclosures |

---

## Open items

- External FX rate provider TBC — module owners to confirm (KJ Lin + Shanshan Gu)
- Flow 1 vs Flow 2 assignment not yet formally recorded — given multi-module consumption, Flow 2 assumed (see open-questions.md)
- HKIA-prescribed rate sources for HKRBC returns to be confirmed with KJ Lin

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page; schema from sql/03_curated_reference.sql | Michael Alo | — |
