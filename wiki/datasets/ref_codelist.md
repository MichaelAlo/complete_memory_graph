# Dataset: ref_codelist

**Schema:** nexus_curated
**Owner:** Michael Alo (Data Lake)
**Refresh cadence:** On release (when source-to-canonical code mappings change)
**Release tag required:** Yes
**Last reviewed:** 2026-05-15

---

## Business purpose

`ref_codelist` is the canonical code list reference table. It stores source-to-canonical code mappings for all harmonised code dimensions (e.g. policy status, product type, book codes). It is the single point of truth for code harmonisation across the pipeline.

This dataset backs the `harmonise_codelist()` function in `src/standardise/pipeline.py` — if a mapping is not in this table, it falls through to the source code unchanged.

---

## Schema summary

| Column | Type | Description | Source |
|---|---|---|---|
| list_name | VARCHAR(80) | Code list name — composite PK col 1 (e.g. policy_status, product_type) | Defined by Data Lake |
| source_code | VARCHAR(80) | Source system code — composite PK col 2 (e.g. "A") | Source system |
| canonical_code | VARCHAR(80) | Canonical Lake code (e.g. "active") | Data Lake |
| description | VARCHAR(255) | Human-readable description | Data Lake |
| _run_id | CHAR(36) | Publication run ID (lineage) | Pipeline |
| _source_cut | VARCHAR(64) | Extract cut for this publication | Pipeline |
| _release_tag | VARCHAR(64) | Release tag | Pipeline |
| _certified_at | DATETIME(6) | Certification timestamp | Pipeline |

**Full DDL:** [sql/03_curated_reference.sql](../../sql/03_curated_reference.sql)

---

## Lineage

```
src/standardise/table_config.py  (codelist_maps per table — authoritative source)
  → src/curate/reference/codelist.py   (publication to curated)
  → nexus_curated.ref_codelist
```

The standardisation table config (`src/standardise/table_config.py`) is the authoritative definition of code mappings. `ref_codelist` is the published, release-tagged version of that config — enabling consumers to query it directly.

---

## Example entries

| list_name | source_code | canonical_code | description |
|---|---|---|---|
| policy_status | A | active | In-force policy |
| policy_status | L | lapsed | Lapsed (non-payment) |
| policy_status | S | surrendered | Surrendered by policyholder |
| policy_status | M | matured | Matured at end of term |
| policy_status | D | death-claim | Death claim in progress |

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|
| (list_name, source_code) uniqueness | uniqueness | 0 duplicates | block promotion |
| canonical_code not null | completeness | 0 nulls | block promotion |
| list_name not null | completeness | 0 nulls | block promotion |

---

## Downstream consumers

| Consumer | Purpose |
|---|---|
| All pipeline standardisation jobs | Code harmonisation validation |
| Governance | Code list lookups for reporting |
| Compliance | Regulatory term mappings |
| Any module reading nexus_curated | Canonical code lookup for display and filtering |

---

## Open items

- Confirm which additional code lists need publishing (beyond policy_status) — module plans will drive this
- Consider whether to publish as a single table (current) or split per list_name (evaluate when volume grows)

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page; schema from sql/03_curated_reference.sql | Michael Alo | — |
