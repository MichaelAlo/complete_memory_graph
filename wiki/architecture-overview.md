# Architecture Overview

**Sources:** `project-nexus-data-flow-architecture.html`, `project-nexus-mdm.html`, `project_nexus_handover_updated_sources.md`

---

## Platform stance

Project Nexus is a **MySQL-first curated analytics platform**, not a cloud-native lakehouse. The honest framing matters: it avoids overpromising and keeps the operating model practical for a small team.

It behaves operationally like a Data Lake because it centralises ingestion, standardisation, MDM, lineage, access control, quality, reusable datasets, and immutable reporting snapshots — but the storage engine is MySQL, the compute is Python jobs, and the control layer is GitLab.

**Azure migration criteria:** defer until one of these triggers is real: MySQL storage pressure, query concurrency pain, semi-structured data volume at scale, or orchestration complexity beyond what lightweight Python cron can handle.

---

## Layer model

| Layer | MySQL schema | Purpose | Promotion rule |
|---|---|---|---|
| Raw | `nexus_raw` | Faithful landing of source extracts. No reinterpretation. | Ingestion-validated only |
| Standardised | `nexus_std` | Typed, cleaned, deduplicated, conformed | Schema + format + completeness checks pass |
| Curated | `nexus_curated` | Certified reusable business-ready datasets, MDM golden records | Reconciliation + lineage + owner approval + quality threshold |
| Reporting snapshot | `nexus_snapshot` | Immutable, versioned evidence behind published reports | Generated only from certified curated outputs; release-tagged |

---

## Hub-and-spoke pattern

The Data Lake is the **single integration backbone**. All inter-module data exchange routes through the Lake. Point-to-point links between operational modules are prohibited by default.

Modules own their own MySQL schemas for specialist logic and state. The shared Lake schemas hold only cross-module certified data, MDM, reference data, and snapshots.

---

## End-to-end flow

```
Core Admin DB ──CDC──► nexus_raw
External feeds ─────────────┘
                         ▼
                   nexus_std  (standardise)
                         ▼
                 nexus_curated  (MDM + curate)
                    │         │
              Modules      nexus_snapshot ──► Governance
              (consume)
              Module outputs ──► nexus_raw (controlled intake)
```

The five logical steps:

1. **Source ingestion** — CDC from Core Admin DB; external feeds; controlled module output drops into Raw.
2. **Standardisation** — type coercion, dedup, code-list harmonisation, domain conformance. No specialist business logic injected here.
3. **MDM and curated publication** — golden records assembled, reference versions applied, lineage linked, certified datasets published.
4. **Module computation** — each module applies specialist logic. Cross-module outputs return to the Lake through controlled interfaces only.
5. **Governance consumption** — board packs, compliance workflows, attestations, all backed by immutable Lake snapshots.

---

## Why not a lakehouse (yet)

| Reason | Detail |
|---|---|
| Structured first | Work is dominated by canonical entities and reporting-ready facts, not semi-structured files |
| Control first | MDM, lineage, reconciliation, and audit-stamped snapshots are needed before distributed compute |
| Faster delivery | MySQL-first is quicker to stand up and easier for a small team to reason about |
| Lower burden | Operational cost stays manageable while the team can still tolerate manual scheduling |
| Migration path open | Azure becomes a justified evolution rather than a premature default |

---

## Reporting split

**Governance** owns reporting marts, user-facing surfaces, board packs, attestation, compliance workflows.

**Data Lake** owns the certified, versioned, reproducible datasets and immutable reporting snapshots behind every published output. Every final published figure must be reproducible from a tagged `nexus_snapshot` record.

This split means Governance controls the front-end and workflow context; the Lake controls the evidence trail.

---

## Pipeline and orchestration

First release: scheduled Python jobs with disciplined run IDs, logging, and idempotent load patterns. Every job supports reruns, partial backfills, and replay using extract cutoffs or batch IDs.

Move to an orchestrator (Airflow, Prefect) only when dependency chaining, retries, environment promotion, or monitoring become too fragile to manage manually.

---

## Security and access model

- Separate technical write access from analyst read access.
- Mask PII in non-privileged views and datasets.
- Restrict sensitive domains by role, domain, and business need.
- Log data access to sensitive datasets and report snapshots.
- Customer PII masked at the Core Admin DB extraction boundary — unmasked PII never lands in any Lake schema.
