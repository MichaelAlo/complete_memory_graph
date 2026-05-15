# Source: [Name]

**Owner:** [person]
**Extraction pattern:** [CDC / date-windowed batch / Flow 1 / Flow 2]
**Extract cut column:** [updated_at or equivalent]
**PII present:** [yes/no]
**Last reviewed:** [date]

---

## Tables extracted

| Table | PK | Updated-at col | PII fields | Raw landing table |
|---|---|---|---|---|

---

## Extraction config

[Reference to `src/ingest/` table config and extract module. Link to specific file paths.]

---

## PII and masking

[List PII fields present in this source. For each: field name, PDPO classification, masking rule, when masking is applied.]

Masking is applied at the extraction boundary before any row is written to `nexus_raw`. Unmasked PII never lands in any Lake schema.

---

## Known limitations

[CDC mechanism, extraction latency, known gaps, open confirmations with source system owner.]

---

## Open items

[Questions to resolve with the source system owner. Link to `wiki/open-questions.md`.]

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
