# Domain Notes

## Terms

| Term | Meaning |
|---|---|
| PACE | PACE Solution Limited — the organisation running Project Nexus |
| MPL | MyPace Life Limited — the Hong Kong licensed insurance carrier; regulatory authority is HKIA |
| ACF | Actual Cashflows — realised cash flows from the period just closed (premiums, claims, surrenders, commissions); sourced from Coreflexi via the Data Lake; consumed by Moody's 2.x for experience-variance analysis against ECF |
| ESG (actuarial) | Economic Scenario Generator — produces stochastic and deterministic scenarios for actuarial/capital projections. Not Environmental/Social/Governance in this context |
| SAA | Strategic Asset Allocation — longer-term Cashfluid workstream optimising asset mix against reserve/capital requirements |
| VDR | Virtual Data Room — used by Transactional for M&A and Section 24 deal materials |
| ALM | Asset-Liability Management — pairing liability cash flows with asset projections to optimise capital, reserves, and risk |
| AML/CFT | Anti-Money Laundering / Combating the Financing of Terrorism |
| ORSA | Own Risk & Solvency Assessment — HKRBC Pillar 2 governance process |
| DOA | Delegation of Authority — approval matrices; owned by Governance, consumed by every module |
| Delta book | Sun 2.x book derived as HKRBC minus HKFRS17 reversing entries; computed inside Sun after both Moody's 2.x and HKRBC Reporting have posted their JEs |
| RPT | Related-Party Transaction — a JE dimension applied by the Lake's data-tagging service using the Counterparty `is_related_party` attribute; feeds HKIA RPT disclosure |
| OCI | Other Comprehensive Income — HKFRS17 presentation option |
| BBA/VFA/PAA | HKFRS17 measurement models: Building Blocks Approach / Variable Fee Approach / Premium Allocation Approach |
| GL36 | HKIA Guideline 36 — the technical standard governing HKRBC Pillar 1 calculations |
| PCA | Prescribed Capital Assessment — modular approach under GL36 Section 10 |
| KRD | Key Rate Duration — used in Cashfluid's asset-liability KRD matching engine |
| MDM | Master Data Management — governance of canonical business entities across systems |
| CDC | Change Data Capture — mechanism to extract changed records from a source DB |
| CoA | Chart of Accounts — finance account code structure used across Sun 2.x and reporting |
| PDPO | Personal Data Privacy Ordinance — Hong Kong privacy regulation governing customer PII |
| ECF | Expected Cash Flows — actuarial output from Cashfluid used in HKFRS17 measurement |
| CSM | Contractual Service Margin — HKFRS17 balance representing unearned profit on insurance contracts |
| RA | Risk Adjustment — HKFRS17 non-financial risk adjustment on insurance liabilities |
| BEL | Best Estimate Liabilities — HKRBC present value of expected future insurance cash flows |
| PCR | Prescribed Capital Requirement — HKRBC solvency capital requirement |
| MCR | Minimum Capital Requirement — HKRBC minimum solvency threshold |
| MOCE | Margin Over Current Estimate — HKRBC prudential margin above BEL |
| TVOG | Time Value of Options and Guarantees — stochastic valuation adjustment in capital models |
| HKFRS17 | Hong Kong Financial Reporting Standard 17 — insurance contract accounting standard |
| HKRBC | Hong Kong Risk-Based Capital — HKIA Pillar 1 capital adequacy framework |
| Flow 1 | Direct-to-Module Feed — stable, contract-based external data consumed by one/few modules |
| Flow 2 | External Ingestion Module → Lake → consumers — ad hoc or multi-consumer external data |
| Golden record | The MDM-mastered, deduplicated, single authoritative version of an entity |
| Type 2 SCD | Slowly Changing Dimension type 2 — versioned history using effective-from/effective-to dates |
| Run ID | UUID assigned to each pipeline job execution for full lineage and replay traceability |
| Extract cut | The date or batch identifier used as the source boundary for an ingestion run |
| Release tag | GitLab tag marking a controlled deployment of pipeline code and MDM definitions |

## Rules

- PII (especially Customer fields) must be masked before leaving Core Admin DB extraction; raw PII never lands in any Lake schema.
- Every curated dataset must reconcile backward to its source system and forward to consuming reports.
- No data-methodology change is complete until code, Wiki, MDM, lineage metadata, and approvals are all updated together.
- Reporting snapshots must store: extract timestamp, source cut, transformation version, approver, release tag.
- External providers may never receive direct read or write access to a Nexus-controlled database.

## Edge cases

- Urgent reporting-period functions may temporarily remain in Coreflexi if deadlines make that the only realistic short-term option — must be explicitly triaged and logged.
- Some aggregations that appear generic may depend on actuarial or regulatory meaning (e.g. grouping logic driven by HKFRS17 cohort rules). Default to Module Function unless confirmed generic by domain owner.
- Reinsurance gross/net split logic — placement in Lake vs module is TBD; do not centralise until explicitly confirmed.
