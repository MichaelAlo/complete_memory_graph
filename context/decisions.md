# Decisions

## 2026-05-06
- Adopt a merged memory architecture: project-local semantic memory, compiled wiki knowledge, and structural code graph.
- Use `/checkpoint` as the canonical end-of-session maintenance command.
- Limit graph refresh scope to `src/` to reduce graph noise and maintenance cost.

## 2026-05-15 — Project Nexus initialization

### ADR-001: MySQL-first over Azure lakehouse
- **Decision:** Build a MySQL-first curated analytics platform, not a cloud-native lakehouse.
- **Rationale:** The immediate problem is governance, traceability, and controlled cross-module reuse — not storage scale. MySQL-first is faster to stand up, easier to maintain, and easier for a small team to reason about. Azure is deferred until MySQL storage, query concurrency, semi-structured data volume, or orchestration complexity genuinely force it.

### ADR-002: Hub-and-spoke integration — no point-to-point
- **Decision:** All inter-module data exchange routes through the Data Lake. No direct module-to-module integrations.
- **Rationale:** Point-to-point links create hidden dependencies, duplicate processing, and make lineage impossible to audit. The Lake is the single certified source of shared data.

### ADR-003: Reporting marts in Governance; snapshots in Data Lake
- **Decision:** Reporting marts live logically in Governance. The underlying published-report datasets are stored as immutable, release-tagged snapshots in `nexus_snapshot` (Data Lake boundary).
- **Rationale:** Governance owns the front-end and workflow context. The Data Lake owns the certified, versioned, reproducible evidence behind every published result. Any published figure must be reproducible from a tagged snapshot.

### ADR-004: Lake Functions vs Module Functions boundary
- **Decision:** Generic, reusable data-engineering and governance controls belong in Lake Functions. Specialist actuarial, accounting, regulatory, compliance, and transactional logic belongs in Module Functions.
- **Tie-break rule:** If two modules would otherwise implement the same thing, default it into the Lake. If the logic depends on domain-specific meaning, keep it in the module.
- **Rationale:** Prevents over-centralisation of specialist logic and keeps the Lake generic and maintainable.

### ADR-005: First-wave MDM domains
- **Decision:** Master Customer, Policy, Product, Chart of Accounts mapping, Currency/FX calendars, and Calendar in the first wave. Counterparty is second-wave unless immediately required.
- **Rationale:** These domains are reused across the most modules and are needed for reconciliation, joins, access control, and downstream reporting.

### ADR-006: Cron-first scheduling
- **Decision:** Use cron or equivalent scheduling for the first release. Move to a heavier orchestrator (Airflow, Prefect) only when dependency chaining, retries, environment promotion, or monitoring become too fragile to manage manually.
- **Rationale:** Keeps operational burden manageable for a small team. Every job is designed to be idempotent and rerunnable, so cron is sufficient initially.

### ADR-007: External data ingestion patterns
- **Decision:** Two approved patterns for external data. Flow 1: direct-to-module for stable, contract-based feeds consumed by one or few modules. Flow 2: External Ingestion Module → Lake → consumers for ad hoc, multi-consumer, or quality-variable datasets.
- **Rationale:** Prevents each consuming module from reimplementing the same external-data extraction, validation, and standardisation independently.

### ADR-008: PII masking at extraction boundary
- **Decision:** Customer PII is masked before any record leaves the Core Admin DB extraction step. Unmasked PII does not exist in any Lake schema.
- **Rationale:** PDPO compliance. Masking at source reduces the blast radius of any Lake access control gap.
