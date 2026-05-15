# Dataset: dim_calendar

**Schema:** nexus_curated
**Owner:** Michael Alo (Data Lake)
**Refresh cadence:** On-demand (regenerate when date range needs extending or on data platform re-provision)
**Release tag required:** Yes
**Last reviewed:** 2026-05-15

---

## Business purpose

`dim_calendar` provides one row per calendar date. It is the shared time dimension used by all modules for:
- Period-close date joins
- Reporting period bucketing (monthly, quarterly, annual)
- Extract cut validation in pipeline jobs
- Time-window anchoring in standardisation and curation

---

## Schema summary

| Column | Type | Description | Source |
|---|---|---|---|
| calendar_date | DATE | Primary key — one row per date | Generated |
| year | SMALLINT | Calendar year | Derived |
| month | TINYINT | Month number 1–12 | Derived |
| day | TINYINT | Day of month 1–31 | Derived |
| day_of_week | TINYINT | 0=Monday … 6=Sunday (Python weekday) | Derived |
| is_weekend | TINYINT(1) | 1=Saturday or Sunday; 0=weekday | Derived |
| quarter | TINYINT | Quarter 1–4 | Derived |
| _run_id | CHAR(36) | Publication run ID (lineage) | Pipeline |
| _source_cut | VARCHAR(64) | Extract cut for this publication | Pipeline |
| _release_tag | VARCHAR(64) | Release tag | Pipeline |
| _certified_at | DATETIME(6) | Certification timestamp | Pipeline |

**Full DDL:** [sql/03_curated_reference.sql](../../sql/03_curated_reference.sql)

---

## Lineage

```
Generated internally (no source extract)
  → src/curate/reference/calendar.py   (publication)
  → nexus_curated.dim_calendar
```

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| calendar_date uniqueness | uniqueness | 0 duplicates | block promotion |
| No date gaps in published range | completeness | 0 gaps | block promotion |
| is_weekend consistent with day_of_week | consistency | 100% | block promotion |
| quarter consistent with month | consistency | 100% | block promotion |

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| All pipeline jobs | Extract cut validation; batch window anchoring |
| Sun 2.x | Period-close date joins |
| Cashfluid | Projection period anchoring |
| Moody's 2.x | Reporting period for HKFRS17 cohort measurements |
| HKRBC Reporting | Reporting period for capital returns |
| Governance | Period labelling in board packs and disclosures |

---

## Open items

- Confirm whether HK public holiday flags should be added (suggestion: yes — raise with Shanshan Gu)
- Confirm default date range for generation (currently configurable at call time; suggest 2015-01-01 to 2035-12-31)

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page; schema from sql/03_curated_reference.sql | Michael Alo | — |
