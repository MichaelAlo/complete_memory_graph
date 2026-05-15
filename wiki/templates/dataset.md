# Dataset: [name]

**Schema:** nexus_curated / nexus_snapshot
**Owner:** [person]
**Refresh cadence:** [daily / per-period-close / on-demand]
**Release tag required:** [yes/no]
**Last reviewed:** [date]

---

## Business purpose

[What decisions, reports, or module computations this dataset enables.]

---

## Schema summary

| Column | Type | Description | Source field | Notes |
|---|---|---|---|---|
| _run_id | CHAR(36) | Extraction run ID (lineage) | pipeline | added by publisher |
| _source_cut | VARCHAR(64) | Extract cut boundary | pipeline | added by publisher |
| _release_tag | VARCHAR(64) | Deployment release tag | pipeline | added by publisher |
| _certified_at | DATETIME(6) | Certification timestamp | pipeline | added by publisher |

---

## Lineage

```
[Source system / table]
  → nexus_raw.[table]         (extraction)
  → nexus_std.[table]         (standardisation)
  → nexus_curated.[dataset]   (curation / this table)
```

---

## Quality rules

| Check | Type | Threshold | Action on fail |
|---|---|---|---|

---

## Downstream consumers

[Modules and reports that read from this dataset. Note what they use it for.]

---

## Open items

[Unresolved questions. Link to `wiki/open-questions.md`.]

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
