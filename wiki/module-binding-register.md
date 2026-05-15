# Module Binding Register

**Sources:** `project-nexus-data-flow-architecture.html`, `project_nexus_handover_updated_sources.md`

---

## Purpose

Reference table for how each module interacts with the Data Lake. Defines what each module owns, what it reads from the Lake, what it writes back, and how Governance relates to its outputs.

---

## Module register

| Module | Owns | Reads from Lake | Writes back to Lake | Governance interaction |
|---|---|---|---|---|
| **Coreflexi / Core Admin DB** | Operational policy admin source records | None required initially | One-way raw feed via extraction only | Indirect — through downstream evidence and control views |
| **Data Lake** | Integration backbone, MDM, quality, lineage, snapshots, Lake Functions | Raw and source loads | Certified datasets into nexus_curated; snapshots into nexus_snapshot | Provides oversight-ready datasets and audit evidence |
| **Cashfluid** | Actuarial liability projection logic | Policy, assumptions, scenarios, expense data, reference data | ECF, scenario outputs, measurement inputs | Provides parity evidence and model output evidence |
| **Sun 2.x** | Posting logic and GL operations | Journal feeds, mapping inputs, reference data | Posted entries, balances, close outputs | Provides close evidence, control outputs, reconciliations |
| **Moody's 2.x** | HKFRS17 measurement and disclosure logic | Cashfluid outputs, expense feeds, reference data | Disclosures, journals, roll-forward outputs | Provides disclosure evidence and approval artefacts |
| **Transactional** | Deal logic and diligence outputs | Portfolio and counterparty reference data | Deal outputs and evidence sets as needed | Provides memo and diligence artefacts |
| **HKRBC Reporting** | Pillar 1 capital calculations and regulatory returns | Actuarial inputs, asset data, regulatory templates | Capital outputs, return data, journal outputs | Provides submission and regulatory evidence |
| **Governance** | Attestation, oversight, board access, reporting surfaces | Certified outputs and report snapshots from nexus_snapshot | Attestation evidence metadata (if required) | Owns all user-facing reporting and oversight surfaces |
| **Compliance** | Regulatory obligations, PDPO, sanctions, RPT filings | Governed outputs and external reference data | TBD — several boundaries still open | Heavy consumer of governed outputs |
| **Strategy** | AI-assisted exploration and FP&A | Governed read access across Lake zones, MDM, Wiki context | None expected | Read-only governance-approved access |

---

## External data ingestion patterns

External data enters the Lake through one of two approved paths. External providers never receive direct read/write access to a Nexus-controlled database.

| Flow | When to use | Examples | Owner |
|---|---|---|---|
| **Flow 1: Direct-to-Module Feed** | Stable, professionally structured, contract-based feeds. Single or few consuming modules. | Asset-manager projections, market data, regulator-published reference rates | Module owner (with Lake team oversight) |
| **Flow 2: External Ingestion Module → Lake → consumers** | Ad hoc, multi-consumer, or quality-variable datasets. | Sanctions lists, experience studies, regulatory documents, ESG datasets, third-party reference tables | Data Lake team |

Flow 2 provides a single extraction, validation, standardisation, versioning, lineage, and curation pass — avoiding reimplementation by each consumer.

---

## Sun 2.x: Delta book design

Sun 2.x is built as a **single event-sourced GL** with `book` as a first-class dimension on every JE line. Books covered: HKFRS / HKFRS17 / HKRBC / Delta / Tax.

The **Delta book** is derived inside Sun 2.x as a book-to-book reconciliation (HKRBC minus HKFRS17 reversing entries) once both HKFRS17 and HKRBC JEs have been posted. This design means **Moody's 2.x and HKRBC Reporting remain independent** and do not cross-read each other's outputs — the Delta is computed by Sun after both upstream modules have posted their JEs.

The **RPT (Related-Party Transaction) dimension** is applied to every JE line in Sun 2.x via the Lake's data-tagging service using the Counterparty MDM entity's `is_related_party` attribute. The RPT Register (owned by Compliance) feeds this tagging.

## Module dependency notes

- **Moody's 2.x depends on Cashfluid outputs.** Cashfluid must write ECF, RA inputs, and scenario outputs back to the Lake before Moody's 2.x can consume them.
- **HKRBC depends on actuarial inputs from Cashfluid** — best-estimate cashflows, 1,000 ESG scenarios, assumption sets.
- **Sun 2.x CoA mapping** is a first-wave MDM domain and must be mastered before Sun 2.x can reliably write back to the Lake.
- **Governance and Compliance are downstream-only** consumers; they do not feed other operational modules (except signals like model validation approvals flowing back to Cashfluid/HKRBC/Moody's).
- **Cashfluid feeds both Moody's 2.x and HKRBC Reporting** independently — these two modules do not cross-read each other's outputs.

---

## Open items

- Per-module Flow 1 vs Flow 2 assignment needs to be documented (see `wiki/open-questions.md`).
- Reinsurance gross/net split routing between Cashfluid and Lake is TBD.
- Compliance module boundaries are partially specified; several Lake vs Module decisions remain open.
- Pillar 2 and Pillar 3 placement across Governance, Compliance, and Strategy is unresolved.
