# Pipeline and Controls

**Sources:** `project-nexus-data-flow-architecture.html` (§8, §9, §10), `project-nexus-mdm.html` (§10)

---

## Pipeline design principles

Every pipeline job in the Lake must follow these patterns:

- **Idempotent** — rerunnable without duplicating results. Use upsert patterns or truncate-reload with version tracking.
- **Run context** — every job execution carries a `run_id` (UUID), `extract_cut` (source date or batch ID), and `release_tag` (GitLab tag).
- **Backfill support** — support date-range or batch-range reprocessing with versioned outputs.
- **Partial replay** — any individual dataset can be rebuilt from Raw without rebuilding the entire pipeline.

---

## Orchestration stance

**First release:** Cron or equivalent scheduling. Python jobs, disciplined logging, idempotent load patterns.

**Move to orchestrator when:** dependency chaining, retries, environment promotion, or monitoring become too fragile to manage manually. Not before.

Candidates when the time comes: Airflow, Prefect. Not mandated.

---

## Controls reference

| Control area | Implementation requirement |
|---|---|
| **Idempotency** | All ingestion and publication jobs must be rerunnable without duplicating results |
| **Backfills** | Support date-range or batch-range reprocessing with versioned outputs |
| **Logging** | Capture run_id, source cut, row counts, validation results, release tag per execution |
| **Data validation** | Apply row-count, null, uniqueness, referential, and reconciliation checks before promotion |
| **Alerting** | Trigger on: failed loads, reconciliation breaks, stale datasets, unauthorised schema drift |
| **Recovery** | Retain raw loads, change versions, and snapshots so any curated release can be rebuilt exactly |

---

## Validation checks before promotion

### Raw → Standardised
- Schema conformance (expected columns present, correct types)
- Format checks (dates parseable, codes within expected domain)
- Completeness (required fields not null)

### Standardised → Curated
- Row-count reconciliation vs source batch
- Uniqueness on business key
- Referential integrity (FK to mastered entities in nexus_curated)
- Domain-level quality rules (defined per entity in MDM)
- Owner approval recorded
- Quality score above threshold

### Curated → Reporting snapshot
- Must be initiated from a valid `release_tag`
- Source query must reference certified curated datasets only
- Approver recorded at generation time
- Snapshot is immutable after creation — no in-place updates

---

## Logging fields

Every job execution log record should include at minimum:

| Field | Description |
|---|---|
| `run_id` | UUID for this execution |
| `job_name` | Identifier for the pipeline step |
| `source_cut` | Extraction date or batch ID |
| `release_tag` | GitLab release tag in effect |
| `started_at` | UTC timestamp |
| `completed_at` | UTC timestamp |
| `row_count_in` | Rows read from source |
| `row_count_out` | Rows written to target |
| `validation_result` | pass / fail |
| `error_detail` | Null on success; error message on failure |

---

## Security and access

- **Technical write access** is separate from **analyst read access** — never grant both to the same credential.
- **PII masking** applied in non-privileged views; masking rules defined per sensitive attribute in MDM.
- **Sensitive domains** (Customer, certain policy fields) restricted by role, domain, and business need.
- **Access logging** enabled for sensitive datasets and report snapshots.
- **External providers** never receive direct DB credentials — use file drops or API integration only.
