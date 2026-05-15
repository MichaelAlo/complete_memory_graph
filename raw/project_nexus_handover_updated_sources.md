# Project Nexus handover for Claude Code

## TL;DR

Project Nexus should currently be treated as a **MySQL-first curated analytics platform** rather than a true lakehouse. The stable architecture position across the latest architecture HTML, the detailed data-flow HTML, and the MDM HTML is: Data Lake as the single integration backbone; modules own specialist logic; Governance owns reporting access surfaces; immutable reporting snapshots remain in the Data Lake; Azure is a later evolution only if MySQL scale, semi-structured data volume, or orchestration complexity genuinely force it.[cite:46][cite:47][cite:48]

This handover captures the latest architecture stance, the source files in play, the work already done in this thread, unresolved questions, and the practical next actions for continuing in Claude Code.[cite:46][cite:47][cite:48][cite:44]

## Source set

Only these three files should be treated as current source of truth for the next Claude Code session:[cite:46][cite:47][cite:48]

- `nexus_architecture.html`.[cite:46]
- `project-nexus-data-flow-architecture.html`.[cite:47]
- `project-nexus-mdm.html`.[cite:48]

The earlier PDF versions and the earlier collaboration DOCX are now secondary artifacts, useful mainly for traceability or comparison, not for setting the current baseline.[cite:44][cite:46][cite:47][cite:48]

## Current architecture position

The current baseline is a **MySQL-first curated analytics platform** with Python jobs and Git-managed definitions and documentation, not a cloud-native Azure lakehouse. The architecture is explicitly framed this way to avoid overpromising and to optimize for a practical, maintainable operating model for the near term.[cite:47][cite:48]

The Data Lake is the hub-and-spoke integration backbone for inter-system exchange, and point-to-point integrations between operational modules are disallowed by default. Modules remain on the same MySQL platform in their own schemas or databases for specialist logic and state, while the shared Data Lake schemas hold raw, standardised, curated, reference, audit, and reporting-snapshot data.[cite:46][cite:47]

The platform should be described honestly as a controlled curated analytics backbone that behaves operationally like a Data Lake because it centralizes ingestion, standardisation, MDM, lineage, access control, reusable datasets, and immutable reporting snapshots. The immediate objective is operability, traceability, auditability, and maintainability, not distributed compute or object-storage-first architecture.[cite:47][cite:48]

## Core design principles

The following principles are the current working baseline:

- Data Lake is the single integration backbone and MDM enforcement point.[cite:46]
- Core Admin DB remains outside Nexus and feeds the Lake one-way only.[cite:46][cite:48]
- PII is masked on the Core Admin DB to Lake sync; raw PII does not live in the Lake.[cite:46]
- Reporting marts live logically in Governance, but the official published-report data remains stored as immutable reporting snapshots in the Data Lake.[cite:46][cite:47][cite:48]
- Lake Functions are only generic, reusable data engineering and governance controls; specialist actuarial, accounting, regulatory, compliance, and transactional logic remains in modules.[cite:46][cite:47][cite:48]
- Azure migration is deferred until there is a real trigger such as MySQL storage pressure, query concurrency pain, semi-structured volume growth, or orchestration complexity beyond what a lightweight stack can handle.[cite:46][cite:47][cite:48]

## Layer model

The current Lake layer model is consistent across the detailed architecture and MDM drafts.[cite:46][cite:47][cite:48]

| Layer | Purpose | Typical content | Owner |
|---|---|---|---|
| Raw | Faithful ingestion landing | CDC extracts, external feed payloads, module output drops | Data Lake team [cite:47][cite:48] |
| Standardised | Typed, cleaned, deduplicated, conformed staging | Normalised tables, harmonised code lists, base conformed entities | Data Lake team [cite:47][cite:48] |
| Curated | Certified reusable business-ready datasets | Mastered entities, shared dimensions, validated facts, reusable data products | Data Lake team with domain owners [cite:47][cite:48] |
| Reporting snapshot | Immutable evidence behind published reports | Audit-stamped report datasets and point-in-time versions | Data Lake team and Governance [cite:47][cite:48] |

The promotion logic is also important: Raw is ingestion-validated only; Standardised requires schema, format, and completeness checks; Curated requires reconciliation, lineage, owner approval, and quality thresholds; Reporting snapshot is generated only from certified curated outputs and tagged releases.[cite:48]

## External data pattern

The latest architecture HTML introduced a more explicit and stronger external-data pattern than the earlier drafts. External providers must never receive direct read or write access to a Nexus-controlled database.[cite:46]

There are now two approved ingestion paths:

- **Flow 1: Direct-to-Module Feed** for stable, professionally structured, contract-based feeds consumed by one or a small number of modules, such as asset-manager projections, market data, or regulator-published reference rates.[cite:46]
- **Flow 2: External Data Ingestion Module -> Data Lake -> consuming modules** for ad hoc, multi-consumer, or quality-variable datasets such as sanctions lists, experience studies, regulatory documents, ESG datasets, and third-party reference tables.[cite:46]

The Flow 2 route is owned by the Data Lake team and is intended to provide one extraction, validation, standardisation, versioning, lineage, and curation layer rather than having each consumer reimplement the same external-data processing independently.[cite:46]

## Lake Functions vs Module Functions

This boundary is one of the central unresolved design areas, but the working principle is already well defined.[cite:46][cite:47][cite:48]

### Lake Functions

These belong in the Lake when they are generic and reusable across multiple modules:

- Ingestion and intake control.[cite:47][cite:48]
- Standardisation and deduplication.[cite:47][cite:48]
- Code-list harmonisation.[cite:46][cite:47][cite:48]
- MDM survivorship and golden-record assembly.[cite:46][cite:47][cite:48]
- Reference-data versioning.[cite:46][cite:47][cite:48]
- Snapshotting.[cite:46][cite:47][cite:48]
- Lineage capture.[cite:46][cite:47][cite:48]
- Data quality controls and reconciliation support.[cite:46][cite:47][cite:48]
- Access governance and masking.[cite:46][cite:47][cite:48]
- Generic reusable aggregations only.[cite:47]

### Module Functions

These remain in modules when they depend on specialist business logic:

- Cashfluid liability cash-flow projection and scenario logic.[cite:46][cite:47][cite:48]
- Sun 2.x journal validation, posting-rule logic, close, allocations, and consolidation.[cite:46][cite:47][cite:48]
- Moodys 2.x contract grouping, CSM roll-forward, RA disclosure, and HKFRS17 packaging.[cite:46][cite:47][cite:48]
- HKRBC Reporting BEL, PCR, MCR, MOCE, TVOG, and return generation logic.[cite:46][cite:47][cite:48]
- Transactional deal modelling and carve-out logic.[cite:46][cite:47][cite:48]
- Governance attestation and workflow logic.[cite:47][cite:48]

### Tie-break rule

If the logic is generic and reusable, keep it in the Lake. If it depends on actuarial, accounting, regulatory, or transaction-specific meaning, keep it in the module. If two modules would otherwise implement the same thing, default it into the Lake.[cite:46][cite:48]

A practical exception exists for urgent reporting-period needs: some functions that would architecturally belong in the Lake may temporarily remain in Coreflexi if deadlines or capacity make that the only realistic short-term option.[cite:46][cite:47][cite:44]

## Reporting stance

The reporting split is now quite stable across the documents. Governance owns the user-facing reporting, board, compliance, attestation, and oversight surfaces, while the Data Lake owns the certified, versioned, reproducible datasets and immutable reporting snapshots behind every published output.[cite:46][cite:47][cite:48]

This split matters because it clarifies that reporting marts are consumption products, not the system of record for the evidence behind a published number. Any final published result should be reproducible from a tagged Data Lake snapshot.[cite:46][cite:47][cite:48]

## MDM position

The Draft MDM Plan is now the clearest concise source for the MDM control model. It treats MDM as the control layer that makes the architecture operational by defining what is mastered, how versions work, how changes are approved, and how curated datasets remain reproducible across modules and reporting outputs.[cite:48]

### First-wave domains

The current first-wave mastering recommendation is:

| Domain | Why first | Likely source of record | Immediate consumers |
|---|---|---|---|
| Customer | Cross-module identity, PDPO sensitivity, deduplication | Core Admin DB | Governance, Cashfluid, reporting [cite:48] |
| Policy | Central grain for actuarial, finance, reporting, compliance | Core Admin DB | All major modules [cite:48] |
| Product | Needed for mapping, cohorts, pricing families, disclosures | Core Admin DB / product reference | Cashfluid, Moodys 2.x, Governance [cite:48] |
| Counterparty | Needed for investment, reinsurance, transactional work | External / transactional reference | Transactional, HKRBC, Governance [cite:48] |
| Chart of Accounts mapping | Needed for finance consistency | Sun 2.x | Sun 2.x, Moodys 2.x, reporting [cite:48] |
| Currency and FX calendars | Needed for valuation and reporting | Reference data source | Sun 2.x, HKRBC, Moodys 2.x [cite:48] |
| Calendar | Needed for closes, snapshots, time buckets, audit cuts | Reference data source | All modules [cite:48] |

### Canonical model rules

Every mastered entity should have a canonical identifier, business key, source-system key set, status, effective-from, effective-to, created timestamp, updated timestamp, and provenance fields. Attributes should be tagged as required, optional, derived, reference-only, or sensitive, and historical states must be queryable via effective-dated or Type-2-style history.[cite:48]

### Governance and change control

The MDM draft sets out a concrete change-control workflow: every semantic, schema, mapping, masking, quality-rule, or methodology change starts as a GitLab issue; impacts are assessed; code, MDM, Wiki, lineage metadata, and quality rules are updated together; approvals are gathered; the change is implemented as a tagged release; validation and sign-off occur; then the updated version is published with effective dates and changelog entry.[cite:48]

The strongest control rule in the draft is that no data-methodology change is complete until code, Wiki, MDM, lineage metadata, and approvals are all updated in the same controlled release.[cite:48]

## Wiki position

The Data Wiki is not meant to be passive documentation. It is a load-bearing artefact intended to be consumed by Claude Code agents and human contributors so that definitions of data sources, canonical entities, mappings, lineage, and methodology stay aligned across the programme.[cite:46]

Michael Alo is the owner of the Wiki and is responsible for proposing the maintenance model, including ownership, review cadence, and change-control workflow. Core Admin DB documentation is maintained separately by Kai Wang but should be referenced from the Data Lake Wiki.[cite:46][cite:44]

## Module summary

The latest architecture HTML defines ten modules or module areas. The key ones for current Data Lake/MDM work are summarized below.[cite:46]

| Module | Primary role | Key interaction with the Lake |
|---|---|---|
| Coreflexi / Core Admin DB | Operational policy admin source system | One-way upstream feed into Raw; some urgent reporting functions may remain here temporarily [cite:46] |
| Data Lake / MDM / Wiki | Integration backbone and control plane | Hosts Lake Functions, MDM, certified datasets, snapshots, and documentation [cite:46][cite:48] |
| Cashfluid | Actuarial liability platform | Consumes policy, assumptions, scenarios, reference data; writes projections and measurement inputs back [cite:46][cite:47] |
| Sun 2.x | General ledger and posting logic | Consumes journal feeds and mapping inputs; writes posted entries, balances, and close outputs back [cite:46][cite:47] |
| Moodys 2.x | HKFRS17 measurement and disclosure engine | Consumes Cashfluid outputs, expense/GL feeds, reference data; writes disclosures and journals back [cite:46][cite:47] |
| Transactional | Deal modelling and diligence | Consumes portfolio/counterparty data; writes deal outputs and evidence sets as needed [cite:46][cite:47] |
| HKRBC Reporting | Pillar 1 capital and return generation | Consumes actuarial, asset, template, and reference data; writes capital outputs, journals, and return data back [cite:46][cite:47] |
| Governance | Oversight, attestation, board/reporting access | Consumes certified outputs and report snapshots; owns user-facing reporting and oversight surfaces [cite:46][cite:47] |
| Compliance | Regulatory obligations, filings, PDPO, sanctions, RPT | Heavy consumer of governed outputs and external data; several boundaries still open [cite:46] |
| Strategy | AI-assisted exploration and future FP&A | Governed read access across Lake zones plus MDM and Wiki context [cite:46] |

## Roles and ownership

The thread-established collaboration model is:

| Person / role | Current responsibility |
|---|---|
| Michael Alo | Draft owner for Wiki, MDM maintenance model, canonical domain definitions, change-control workflow, and collaboration documents [cite:44][cite:46] |
| Shanshan Gu | Co-leads Data Lake / MDM build and reviews architecture and Lake-vs-module boundaries [cite:44][cite:46] |
| Kai Wang | Owns Core Admin DB documentation and upstream source/extraction context; reviews upstream code [cite:44][cite:46] |
| Matt Burlage | Owns architecture proposal and detailed data-flow architecture; aligns module-level design [cite:44][cite:46] |
| Luke Lai | Reviews downstream Data Lake implementation and interim Coreflexi functions; covers downstream code review [cite:44][cite:46] |
| Module owners | Validate source-of-record decisions and specialist-boundary assumptions in their domains [cite:44][cite:46] |

## What was done in this thread

Several document-building steps were completed before the newest HTML files were declared the only source set.

### Documents created earlier in the thread

A live collaboration DOCX was created to act as a shared commentable working artifact for inline MDM and data-flow review. That document included sections on roles, architecture summary, Data Lake layers, MDM responsibilities, MDM operating model, Wiki maintenance, Lake Functions vs Module Functions, boundary decisions, open questions, and residual gaps.[cite:44]

The thread then established that exact parity with the HTML drafts required fuller transcription, and a later DOCX was produced with full transcription sections for the two HTML files. However, once the source set changed, the HTML files became the only current baseline and the earlier PDF-based comparisons should be treated as historical context only.[cite:42][cite:43][cite:44][cite:46][cite:47][cite:48]

### Practical implication

Do not assume the existing DOCX is the final truth source. It is a collaboration artefact, but the newest HTML files supersede earlier assumptions where they differ.[cite:44][cite:46][cite:47][cite:48]

## Current source hierarchy

For future Claude Code work, the recommended source priority is now just these three HTML files:[cite:46][cite:47][cite:48]

1. `nexus_architecture.html` as the broad master architecture reference, including module descriptions, confirmed decisions, open questions, and next steps.[cite:46]
2. `project-nexus-data-flow-architecture.html` as the concise technical architecture and operating-model reference for Lake structure, flow, controls, and sequencing.[cite:47]
3. `project-nexus-mdm.html` as the concise control-model reference for mastering, change control, roles, certification, and MDM operating logic.[cite:48]

The earlier PDFs and the earlier collaboration DOCX are now secondary artifacts, useful mainly for traceability or comparison, not for setting the current baseline.[cite:44][cite:46][cite:47][cite:48]

## Open questions that still matter

The HTML drafts still leave several questions unresolved.

### Architectural and boundary questions

- Exact per-module architecture and project timelines still need to be completed by module owners.[cite:46]
- The final per-module Lake Function vs Module Function split still needs explicit confirmation.[cite:46][cite:47][cite:48]
- Some grey-area aggregations remain unresolved, especially where specialist definitions drive the logic.[cite:46][cite:47]
- The exact Governance app-to-module binding remains intentionally under-specified.[cite:46][cite:47][cite:48]

### Reporting and governance questions

- Pillar 2 and Pillar 3 placement across Governance, Compliance, and Strategy remains open.[cite:46]
- Governance-side workflow details are not fully designed yet.[cite:46]
- The exact review cadence between project leads and tech reviewers still needs agreement, though the lead-build / reviewer-check split is clear.[cite:46][cite:47][cite:48]

### Delivery and implementation questions

- Which urgent reporting-period functions must stay in Coreflexi temporarily still needs explicit triage.[cite:46][cite:47][cite:48]
- Dataset-by-dataset Flow 1 vs Flow 2 assignment needs to be recorded in the MDM.[cite:46]
- Reinsurance gross/net split logic remains TBD in some downstream areas.[cite:46]
- Some module-level dependency tables and detailed timelines remain incomplete or preliminary.[cite:46]

## Recommended implementation posture

For near-term engineering work, the practical posture should be:

- Use MySQL schemas for raw, standardised, curated, reference, audit, and reporting snapshot layers.[cite:47]
- Use Python jobs for extraction, standardisation, validation, promotion, snapshotting, and dataset publication.[cite:47]
- Start with cron or equivalent scheduling plus disciplined logging, run IDs, rerun/backfill support, and idempotent patterns; only move to a heavier orchestrator when dependency management and monitoring become fragile.[cite:47]
- Build lineage, quality controls, and reporting-snapshot mechanics early, before broadening consumption significantly.[cite:47][cite:48]
- Keep module state and specialist logic in module-owned schemas rather than over-centralizing into the shared Lake.[cite:46][cite:47]

## What to build first

The concise detailed data-flow HTML gives the clearest recommended build order:[cite:47]

1. Raw and standardised ingestion from Core Admin DB and the highest-priority external feeds.[cite:47]
2. First-wave MDM domains: Customer, Policy, Product, CoA mapping, Currency, Calendar.[cite:47][cite:48]
3. Lineage, quality, and snapshot controls before onboarding too many consumers.[cite:47]
4. Certified curated datasets for the most urgent downstream consumers.[cite:47]
5. Governance-facing reporting snapshot handoff and audit-trail model.[cite:47]

## What to postpone

The latest HTMLs are very clear that several things should not be over-engineered yet.[cite:47]

- Azure-native lakehouse tooling should be postponed unless MySQL storage, query concurrency, or binary/object scale becomes painful.[cite:47]
- Heavy orchestration should wait until cron-style scheduling becomes operationally unsafe.[cite:47]
- Broad document-repository functions inside MySQL should be limited to metadata and structured tracking for now.[cite:47]
- Real-time streaming should be avoided unless an actual freshness requirement appears.[cite:47]

## Document state and known gaps

The current collaboration DOCX is useful but incomplete as an exact master source. It does not necessarily contain every paragraph, table, or diagram from the HTML, and some visual content cannot be losslessly reproduced in text-only sections.[cite:44]

Now that the newest HTML files are the only source set, any future merged live-collaboration document should reconcile the earlier DOCX and transcription work against `nexus_architecture.html`, `project-nexus-data-flow-architecture.html`, and `project-nexus-mdm.html` only.[cite:44][cite:46][cite:47][cite:48]

## Suggested next tasks for Claude Code

A useful next-session plan in Claude Code would be:

1. Read the three HTMLs first and treat them as the current baseline.[cite:46][cite:47][cite:48]
2. Compare the HTMLs against the existing collaboration DOCX and identify drift, omissions, and outdated statements.[cite:44][cite:46][cite:47][cite:48]
3. Produce a new consolidated live-collaboration master document in Markdown first, then generate DOCX/PDF if needed.[cite:44][cite:46][cite:47][cite:48]
4. Merge only the wording-level parity content still needed from the HTML sources into the working artifact.[cite:42][cite:43]
5. Create a per-module Lake Function vs Module Function decision register with owner, status, rationale, and deadline.[cite:46][cite:47][cite:48]
6. Create a dataset register for Flow 1 vs Flow 2 external-data routing, with consumer count, source quality, refresh cadence, and owner.[cite:46]
7. Create a first-wave MDM schema pack covering Customer, Policy, Product, CoA mapping, Currency/FX, and Calendar.[cite:48]
8. Draft a practical MySQL/Python implementation plan with tables, job boundaries, validation checks, logging fields, access model, and release process.[cite:47][cite:48]

## Suggested file set for Claude Code context

These are the files that should be loaded first into the next Claude Code session:[cite:46][cite:47][cite:48]

| Priority | File | Why it matters |
|---|---|---|
| 1 | `nexus_architecture.html` | Master architecture source, latest broad system view [cite:46] |
| 2 | `project-nexus-data-flow-architecture.html` | Concise technical operating model [cite:47] |
| 3 | `project-nexus-mdm.html` | Concise MDM/control model [cite:48] |
| 4 | `project-nexus-mdm-live-collaboration-final.docx` | Existing collaboration artifact to be reconciled, not blindly trusted as source of truth [cite:44] |

## Bottom line for the next session

The project is no longer in the “what is the architecture?” stage. The higher-value work now is to convert the current consistent stance into a cleaner operating blueprint: exact source hierarchy, per-module boundary decisions, external-data routing register, first-wave MDM schema and governance definitions, and a maintainable MySQL/Python delivery plan with strong controls.[cite:46][cite:47][cite:48]

The main risk in the next Claude Code session is not lack of direction; it is drifting back into outdated draft assumptions or over-designing a lakehouse too early. The most defensible next move is a consolidated, latest-source-aligned master document plus a set of decision registers that turn the architecture into implementable work packages.[cite:46][cite:47][cite:48]
