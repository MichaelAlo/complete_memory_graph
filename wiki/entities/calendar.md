# Entity: Calendar

**Domain:** First-wave
**Source of record:** Generated internally (no external provider)
**Data owner:** Michael Alo (Data Lake)
**Last reviewed:** 2026-05-15

---

## Business definition

The Calendar dimension provides one row per calendar date with derived time attributes (year, month, quarter, day-of-week, weekend flag). It is mastered centrally because:
- Period-close dates, extract cut boundaries, snapshot dates, and time-bucket joins all reference a shared calendar
- Consistent period definitions across modules prevent off-by-one errors in monthly/quarterly aggregations
- The calendar is the simplest first-wave entity to publish — no external dependency, no PII, no MDM survivorship required

The calendar is generated programmatically by the Data Lake for a configurable date range. It is not extracted from any source system.

---

## Canonical fields (implemented in nexus_curated.dim_calendar)

| Field | Type | Required | Description |
|---|---|---|---|
| calendar_date | DATE | yes | Primary key — one row per date |
| year | SMALLINT | yes | Calendar year (e.g. 2026) |
| month | TINYINT | yes | Month number 1–12 |
| day | TINYINT | yes | Day of month 1–31 |
| day_of_week | TINYINT | yes | 0 = Monday … 6 = Sunday (Python weekday convention) |
| is_weekend | TINYINT(1) | yes | 1 = Saturday or Sunday; 0 = weekday |
| quarter | TINYINT | yes | Quarter 1–4 |
| _run_id | CHAR(36) | yes | Lineage: publication run ID |
| _source_cut | VARCHAR(64) | yes | Extract cut for this publication |
| _release_tag | VARCHAR(64) | yes | Release tag |
| _certified_at | DATETIME(6) | yes | Certification timestamp |

**Full DDL:** `sql/03_curated_reference.sql`
**Publication code:** `src/curate/reference/calendar.py`

---

## Effective dating

Calendar rows are point-in-time immutable — one row per date, no versioning required. Holiday calendars (if added later) would use a separate entity with effective dating.

---

## Source system keys

Not applicable — calendar is generated, not extracted.

---

## PII and masking rules

Calendar data contains no PII.

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| All modules | Time-bucket joins; period-close date lookups |
| Pipeline jobs | Extract cut date validation; batch window anchoring |
| Sun 2.x | Financial close calendar; period-end date joins |
| HKRBC | Reporting period definition |
| Governance | Board pack period labelling; report date joins |

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| calendar_date uniqueness | uniqueness | 0 duplicates | block promotion |
| No date gaps in published range | completeness | 0 gaps | block promotion |
| is_weekend matches day_of_week | consistency | 100% consistent | block promotion |
| quarter derived correctly | consistency | 100% consistent | block promotion |

---

## Open items

- Confirm whether Hong Kong public holiday flags should be added to this entity (suggest yes for period-close logic — raise with Shanshan Gu)
- Confirm date range to generate (currently configurable at call time; suggest default: 2015-01-01 to 2035-12-31)

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created; fields based on implemented DDL | Michael Alo | — |
