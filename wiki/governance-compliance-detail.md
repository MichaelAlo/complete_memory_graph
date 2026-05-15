# Governance and Compliance — Sub-domain Detail

**Sources:** `nexus_architecture.html` (§5.8, §5.9, §3 cards 8–9)

---

## Governance module

**Leads:** Bill Nichol & Betty Pun | **Support:** Yang Mingyang | **Status:** Not started

Internal governance backbone across the organisation. Five sub-domains:

### 1. Risk & Capital Governance

**Inputs:** Cashfluid (cash flows, ESG, stress runs); HKRBC Reporting (PCR/MCR/MOCE, sensitivities); Sun 2.x (financials by book); model inventory feeds from Cashfluid/HKRBC/Moody's; internal incident/breach data.

**Processes:** Risk Register + Risk Appetite Statement maintenance; ORSA governance and narrative assembly (**Pillar 2 placement: OPEN QUESTION**); Model Risk Management (inventory, validation cadence, sign-off); Capital Management Policy oversight; stress testing governance.

**Lake Functions:** Ingestion of cross-module risk + capital data; snapshotting of stress scenarios and model runs; lineage from model output through validation evidence; MDM for Risk and Model entities.

**Outputs:** Risk Register and Model Risk register (to Lake); ORSA artefacts (to HKIA via Compliance); model validation approvals (signals back to Cashfluid, HKRBC, Moody's 2.x); KRI dashboards (via Reporting marts).

### 2. Conduct & Ethics

**Inputs:** HR records (training, F&P attestations, conduct events); Coreflexi customer interactions and complaints; whistleblower reports (manual intake); breach data from across modules.

**Processes:** Staff Conduct (Code of Conduct, Fit & Proper, training & attestations); Conduct/breach workflow; Whistleblowing register; Anti-bribery/Gifts & Entertainment register; Complaints handling oversight.

**Lake Functions:** Ingestion of HR + complaints data; MDM for Staff entity; access governance for sensitive conduct/whistleblower data; snapshotting of incidents and dispositions.

**Outputs:** Whistleblowing register and Anti-bribery register (to Lake); conduct/breach disposition records; complaints handling outputs (back to Coreflexi for customer-side closure); staff conduct attestations.

### 3. Operational Governance

**Inputs:** Policy library; procurement requests + vendor data; BCP/DR test results; security incident data; internal audit findings.

**Processes:** Policy/Procedure Management; DOA (Delegation of Authority) & approval matrices; Procurement governance; Third-party/outsourcing register; BCP/DR governance; Information Security governance.

**Lake Functions:** MDM for Policy, Vendor, Outsourcing entities; access governance for sensitive operational evidence; snapshotting of policy versions and DOA matrices.

**Outputs:** Policy Register, Vendor/Outsourcing Register (to Lake); DOA matrices (**consumed by every module for workflow approvals**); BCP/DR test evidence; InfoSec controls evidence.

### 4. Board & Committee Governance

**Inputs:** Reporting marts (financials, capital, risk, conduct); Sun 2.x and HKRBC Reporting outputs; Risk Register and ORSA artefacts; Director records.

**Processes:** Committee charters & calendars (Board, Audit, Risk, Par, Investment); board reporting pack assembly; Resolutions register; Director appointments & training; Attestations/sign-offs.

**Lake Functions:** Snapshotting of board-pack datasets (audit trail); MDM for Resolutions and Director entities; access governance.

**Outputs:** Board/committee packs (to Reporting marts front-end); Resolutions Register, Director Register (to Lake); signed attestations (audit trail).

### 5. Audit & Attestation Backbone *(cross-cutting: supports Governance, Compliance, and Strategy)*

**Inputs:** Evidence from sub-domains 1–4 plus Compliance and Strategy; system logs across all Nexus modules; transaction-level data from all modules via Lake Standardised; external auditor working-paper requirements.

**Processes:** Internal audit coordination; external audit support; attestation evidence repository.

**Lake Functions:** End-to-end lineage capture across all modules; immutable evidence storage (audit trail Lake Function); access governance for audit/regulator queries.

**Outputs:** Audit working papers/evidence packs (to internal and external auditors); attestation registers (to Lake); audit findings tracking (consumed by every module for remediation).

---

## Compliance module

**Leads:** Betty Pun & Yang Mingyang | **Support:** Bill Nichol | **Status:** Not started

External regulatory compliance — discharging regulator-facing obligations across HKIA, HKFRS, AML/CFT, PDPO, and adjacent frameworks. Four sub-domains:

### 1. Regulatory Compliance

**Inputs:** External regulatory feeds (HKIA GLs, CIRs, IIC papers; HKFRS updates); tax tables and statutory deadlines; licence registers; Reporting marts; Sun 2.x financial-statement inputs.

**Processes:** Obligation Register (HKIA general + MPL-specific); licence management (HKIA insurer, ICB, HKFI, intermediaries); Monthly Attestation Program; Companies Ordinance filings (Annual Return, SCR, AGM, statutory books); tax compliance oversight (profits tax, employer's return, agent/broker return); regulatory horizon scanning; AML/CFT policy oversight.

**Lake Functions:** Ingestion of regulatory text feeds and statutory deadlines; structured-data extraction from regulatory text into obligation entities; MDM for Obligation Register and Licence Register; reference-data versioning for regulatory text.

**Outputs:** Obligation Register, Licence Register, AML/CFT policy register (to Lake); statutory filings (Companies Registry, IRD); monthly attestation evidence.

### 2. Data & Privacy

**Inputs:** Customer PII flows (Coreflexi → Lake); data retention schedules; Sanctions/PEP lists (external); Lake access logs and data-quality breach reports.

**Processes:** PDPO/data privacy oversight; data retention/records management; Sanctions/PEP screening governance.

**Lake Functions:** Access governance Lake Function operationalises PDPO policy; ingestion of sanctions/PEP lists; MDM for Customer (with PII attributes flagged); lineage capture for data subject access requests.

**Outputs:** PDPO controls evidence; data retention policy; Sanctions/PEP Register (to Lake); access policy back to Lake (enforcement loop).

### 3. RPT Register (Related-Party Transactions)

**Inputs:** Definition of related-party criteria (HKFRS 24, HKIA expectations); intra-group entity register (PSL, MPL, planned IoM entity); Director/KMP register (from Governance Board sub-domain).

**Processes:** RPT register maintenance (related-party definitions, approval workflow); transfer-pricing documentation oversight.

**Lake Functions:** MDM for Counterparty entity (with `is_related_party` attribute); **Lake's data-tagging service applies the RPT flag to every JE line via Counterparty lookup.**

**Outputs:** RPT Register (to Lake); RPT dimension on every Sun 2.x JE line (carved out for disclosure); RPT disclosure submissions to HKIA.

### 4. Non-Pillar-1 HKIA Returns

**Inputs:** HKRBC Reporting (Pillar-1 capital figures); Sun 2.x (financials); Cashfluid (actuarial figures); RPT register; Risk and ORSA artefacts from Governance.

**Processes:** Quarterly Management Report composition; Annual Business Plan composition; RPT submission composition; filing workflow and attestation.

**Lake Functions:** Reporting marts consolidate data across Sun, HKRBC, Cashfluid for composite returns; snapshotting of submitted returns in Reporting snapshot zone.

**Outputs:** HKIA non-Pillar-1 submissions; attestation evidence (to Lake).

---

## Pillar 2 / 3 open question

**Pillar 2** (ORSA governance, stress orchestration) and **Pillar 3** (public disclosure templates) placement remains an open question across Governance / Compliance / Strategy. Pillar 2 in particular may sit more naturally inside Governance (Bill/Betty). See `wiki/open-questions.md`.

---

## Notes on Compliance as external-data consumer

Compliance is the **heaviest consumer** of external feeds: sanctions lists, PEP lists, regulatory text (HKIA GLs, CIRs), HKFRS updates, HKIA templates, tax updates. Whether these should arrive via a single external-data ingestion layer (Flow 2) rather than module-direct is a particularly relevant open question.
