# Project Overview

## Mission

Build and operate the **Project Nexus Data Lake**: a MySQL-first curated analytics platform that acts as the integration backbone for an insurance analytics programme covering actuarial (Cashfluid), general ledger (Sun 2.x), HKFRS17 measurement (Moody's 2.x), capital/regulatory reporting (HKRBC), transactional (Transactional), and oversight/reporting (Governance) modules.

The immediate objective is **operability, traceability, auditability, and maintainability** — not distributed compute or object-storage-first architecture.

## Users

| Consumer | How they use the Lake |
|---|---|
| Data Lake team (Michael Alo, Shanshan Gu) | Build and operate pipelines, MDM, quality controls, and snapshots |
| Module owners (Cashfluid, Sun, Moody's, HKRBC, Transactional) | Consume certified curated datasets; return module outputs through controlled interfaces |
| Governance | Consume certified outputs and reporting snapshots for board packs, compliance workflows, attestations |
| Compliance / Strategy | Governed read access to curated and snapshot zones |
| Kai Wang | Upstream source context for Core Admin DB extractions |

## Constraints

- **Platform:** MySQL 8+, Python 3.11+, GitLab for code and documentation.
- **No Azure lakehouse yet.** MySQL-first until storage, concurrency, or orchestration complexity genuinely forces a migration.
- **PII/PDPO:** Customer PII must be masked before landing in the Lake. Raw PII does not live in any Lake schema.
- **No point-to-point:** Modules may not exchange data directly. All inter-system exchange routes through the Lake.
- **Idempotency:** Every ingestion and publication job must support reruns, partial backfills, and replay without duplicating results.
- **Change control:** Every schema, semantic, mapping, or quality-rule change starts as a GitLab issue and must update code, MDM, Wiki, and lineage metadata together as one tagged release.
- **Orchestration:** Cron or equivalent scheduling first; move to a heavier orchestrator only when dependency chaining and monitoring become fragile.
- **External providers:** No direct read/write access to Nexus-controlled databases. All external data enters via Flow 1 (direct-to-module, contract-based) or Flow 2 (External Ingestion Module → Lake → consumers).

## Priorities

1. Raw and standardised ingestion path from Core Admin DB and highest-priority external feeds.
2. First-wave MDM domains: Customer, Policy, Product, CoA mapping, Currency/FX calendars, Calendar.
3. Lineage, quality, and snapshot controls before onboarding too many consumers.
4. Certified curated datasets for the most urgent downstream module consumers.
5. Governance-facing reporting snapshot handoff and audit trail model.

## What to postpone

- Azure-native lakehouse tooling.
- Heavy orchestration (Airflow, Prefect) until cron becomes operationally unsafe.
- Real-time streaming unless a genuine freshness requirement appears.
- Broad document-repository functions inside MySQL beyond metadata and structured tracking.
