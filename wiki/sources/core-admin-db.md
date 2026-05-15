# Source: Core Admin DB

**Owner:** Kai Wang (upstream source and extraction context)
**Extraction pattern:** Date-windowed batch (`WHERE updated_at > last_cut AND updated_at <= extract_cut`)
**Extract cut column:** `updated_at`
**PII present:** Yes — in `customers` table
**Last reviewed:** 2026-05-15

> Core Admin DB is the operational policy administration system (Coreflexi). It is outside the Project Nexus boundary. Kai Wang maintains the detailed documentation. This page documents what the Data Lake extracts and how.

---

## Tables extracted

| Table | PK | Updated-at col | PII fields | Raw landing table |
|---|---|---|---|---|
| customers | customer_id | updated_at | name, date_of_birth, id_number, email, phone | nexus_raw.customers |
| policies | policy_id | updated_at | — | nexus_raw.policies |
| products | product_id | updated_at | — | nexus_raw.products |

All PII fields in `customers` are masked with `***` before any row is written to `nexus_raw`. See masking rules below.

---

## Extraction config

Implemented in:
- [src/ingest/core_admin/table_config.py](../src/ingest/core_admin/table_config.py) — per-table config (PK, updated-at col, PII fields)
- [src/ingest/core_admin/extract.py](../src/ingest/core_admin/extract.py) — extraction logic, PII masking, upsert to nexus_raw

The extractor uses `nexus_raw.job_runs` to determine the `last_cut` for each table. On first run, falls back to `Config.initial_extract_from` (default: 2020-01-01).

---

## PII and masking

PII masking is applied in `extract.py:_mask_pii()` before any row is written to `nexus_raw`. The PDPO-governed fields are:

| Field | Table | PDPO classification | Masking rule | Access in Lake |
|---|---|---|---|---|
| name | customers | Personal data | Replaced with `***` at extraction | Not stored in any Lake schema |
| date_of_birth | customers | Personal data | Replaced with `***` at extraction | Not stored in any Lake schema |
| id_number | customers | Sensitive personal data (HKID/passport) | Replaced with `***` at extraction | Not stored in any Lake schema |
| email | customers | Personal data | Replaced with `***` at extraction | Not stored in any Lake schema |
| phone | customers | Personal data | Replaced with `***` at extraction | Not stored in any Lake schema |

**Hard rule (ADR-008):** Unmasked customer PII must never leave the Core Admin DB extraction boundary. No Lake schema stores raw PII.

To extend the PII field list, update `TABLES["customers"].pii_fields` in `src/ingest/core_admin/table_config.py` and update this page in the same release.

---

## Known limitations

- **CDC mechanism:** Currently implemented as date-windowed batch using `updated_at`. True CDC (event-log-based) has not been confirmed with Kai Wang — the current approach is a safe fallback.
- **Hard-delete handling:** Records deleted from Core Admin DB will not be reflected in nexus_raw without a separate reconciliation or soft-delete pattern. To be confirmed with Kai Wang.
- **Table coverage:** Only `customers`, `policies`, and `products` are configured. Additional tables will be added as module plans confirm what the Lake needs.
- **Schema stability:** Core Admin DB schema changes must be communicated to the Data Lake team before deployment to avoid extraction failures.

---

## Open items

- Confirm CDC mechanism with Kai Wang — can we get an event log or must we continue with `updated_at` windowing? (see `wiki/open-questions.md`)
- Confirm hard-delete handling approach.
- Confirm complete list of tables to extract for first-wave needs.
- Kai Wang to review this page for accuracy against Core Admin DB documentation.

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial page created from handover docs | Michael Alo | — |
