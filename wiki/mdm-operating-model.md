# MDM Operating Model

**Sources:** `project-nexus-mdm.html`, `project_nexus_handover_updated_sources.md`

---

## Purpose

MDM is the control layer that makes the architecture operational. It defines what is mastered, how versions are governed, how changes are approved, and how curated datasets stay reproducible across modules and reporting outputs.

---

## First-wave mastering domains

| Domain | Why first | Source of record | Immediate consumers |
|---|---|---|---|
| Customer | Cross-module identity, PDPO sensitivity, deduplication requirement | Core Admin DB | Governance, Cashfluid, reporting |
| Policy | Central grain for actuarial, finance, reporting, compliance | Core Admin DB | All major modules |
| Product | Mapping, cohorts, pricing families, disclosures | Core Admin DB / product reference | Cashfluid, Moody's 2.x, Governance |
| Chart of Accounts mapping | Cross-system finance consistency | Sun 2.x | Sun 2.x, Moody's 2.x, reporting |
| Currency and FX calendars | Valuation, retranslation, reporting | Reference data source | Sun 2.x, HKRBC, Moody's 2.x |
| Calendar | Period close, snapshots, time buckets, audit cuts | Reference data source | All modules |

**Second-wave (deferred):** Counterparty and investment reference data, unless immediately required for Transactional or HKRBC work.

---

## Canonical model rules

Every mastered entity must carry:

- `canonical_id` — Lake-issued primary identifier
- `business_key` — natural business identifier
- `source_system_keys` — map of source-system key per upstream system
- `status` — active / inactive / merged
- `effective_from`, `effective_to` — Type 2 SCD effective dating (`effective_to = NULL` means current)
- `created_at`, `updated_at` — audit timestamps
- `provenance` — source system supplying the surviving attributes

Every attribute must be tagged as: required / optional / derived / reference-only / sensitive.

Sensitive fields must have PDPO classification, masking rule, and access restriction defined before the entity is certified.

---

## Zones and certification

| Zone | Allowed content | Promotion rule |
|---|---|---|
| Raw | CDC extracts, external feed payloads, module outputs as received | Ingestion-validated only |
| Standardised | Normalised source tables, mapped code lists, base conformed entities | Schema, format, completeness checks pass |
| Curated / Gold | Mastered entities, shared dimensions, validated facts, reusable data products | Reconciliation + lineage + owner approval + quality threshold |
| Reporting snapshot | Audit-stamped report datasets and point-in-time extracts | From certified curated outputs only; release-tagged |

**Key rule:** Reporting snapshots must remain inside the Data Lake boundary even if reporting marts live in Governance. Every snapshot must store: extract timestamp, source cut, transformation version, approver, release tag.

---

## Governance roles

| Role | Responsibility |
|---|---|
| Data owner | Business accountability for semantic correctness and usage of a domain |
| Data steward | Operates quality rules, definitions, issue management, business glossary upkeep |
| Data custodian | Technical operation of storage, processing, security, recoverability |
| Module owner | Approves downstream impact when a change affects their module's inputs, outputs, or logic |
| Governance reviewer | Approves changes affecting regulatory outputs, PDPO controls, disclosures, or attestation |
| Wiki owner | Ensures documentation is synced to methodology and MDM changes (Michael Alo) |

---

## Change-control workflow

Every schema, semantic, mapping, quality-rule, masking-rule, or reporting-methodology change follows this sequence:

1. **Raise GitLab issue** — every change starts here, no exceptions.
2. **Assess impact** — affected domains, datasets, modules, reports, backfills, controls, approvals.
3. **Update artefacts together** — MDM entry, Wiki page, lineage metadata, quality rules, and Lake Functions Registry must all be in the same change set.
4. **Approve** — domain owner + affected module owner + Data Lake owner. Add Governance reviewer if compliance or reporting is affected.
5. **Implement** — deploy SQL, Python, mapping, and documentation changes as one tagged release.
6. **Validate** — reconciliation checks, regression comparisons, human sign-off.
7. **Version and publish** — mark effective-from dates, retain prior versions, publish changelog entry in Wiki.

**Hard rule:** No data-methodology change is complete until code, Wiki, MDM, lineage metadata, and approvals are all updated in the same controlled release.

---

## Data quality and reconciliation

- Each curated dataset must have named quality checks: completeness, uniqueness, validity, referential integrity, timeliness.
- Every key published metric must reconcile backward to its source system and forward to consuming reports.
- Breaks must be logged, triaged, assigned, and closed with root cause and corrective action.
- Report snapshots store the extract timestamp, source cut, transformation version, approver, and release identifier.

---

## Wiki maintenance model

The Data Wiki is a load-bearing artefact, not passive documentation. It is consumed by Claude Code agents and human contributors to keep definitions of sources, canonical entities, mappings, lineage, and methodology aligned across the programme.

Each major domain, Lake Function, source system, and curated dataset should have a dedicated page with: ownership, refresh cadence, schema summary, quality rules, downstream consumers, change history.

Core Admin DB documentation is maintained separately by Kai Wang but should be referenced from the Data Lake Wiki.
