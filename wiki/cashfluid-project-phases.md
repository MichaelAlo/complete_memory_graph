# Cashfluid Project Phases

**Sources:** `nexus_architecture.html` (§5.3) — Cashfluid is the reference implementation for module project plans.

---

## Overview

Cashfluid is the actuarial liability platform. It produces best-estimate cash flows, HKFRS17 measurement components, and Pillar 1 capital inputs (BEL, 1,000 ESG scenarios) for HKRBC Reporting. Pre-Phase-5 it runs on local CSV; post-Phase-5 it reads from and writes to the Data Lake Curated zone.

**Current performance baseline:** 0.1–0.2s per policy for per-policy liability projections. This is the core first optimisation step since all downstream ALM and reporting rely on it.

**Reinsurance** is intentionally excluded from the current scope pending a dedicated discussion.

---

## Phase status

| Phase | Name | Status |
|---|---|---|
| Phase A | Foundations (infrastructure) | **Complete** |
| Phase B | Foundations (core projection) | **Complete** |
| Phase 2 | Model Running & ALM | In build |
| Phase 3 | AI Integration | Planned |
| Phase 4 | Assumption Authoring | Planned |
| Phase 5 | Data Lake Integration | Planned (post-Phase-2) |
| Phase 1 (FE) | Front End | Planned |

---

## Phase A & B — complete

- RunSpec + multi-tenant / per-acquisition-block isolation
- PolicyModelPoint schema + pluggable DataConnector Protocol (CSV today, Lake later)
- Assumption framework: SchemaMetadata, AssumptionTable + interpolation, lookups, GovernanceWorkflow
- Projection calendar + DecrementEngine (UDD / constant-force / Balducci)
- CashflowComponent Protocol + components: premium, death, surrender, tax, expense, dividend, PUA
- Valuation: precomputed DiscountCurve + PV rollups; 41-col Parquet + 17-col reserves output schemas
- ScenarioLibrary; ValidationHarness; ModelComparisonFramework (pluggable legacy adapters)

---

## Phase 2 — Model Running & ALM

Key deliverables:
- **CapitalConstraint hierarchy:** PCRStub → PCROnly → PCRPlusPillar2Scalar → PCRPlusPillar2Computed → PCRPlusAccountingReserve → EconomicCapital (ADR-031)
- **BEL cashflow contract** — stable, semver-controlled — published for downstream module consumption
- SAA optimisation loop: mean-variance → stochastic; RN-ESG wrap; Reserve Requirement engine
- HKRBC-INT consumption client (stub then live)
- Convergence orchestrator (damped fixed-point; non-convergence escalation per ADR-032)
- Daily SAA scheduler (cron-style; M3 MVP)
- Asset-curve schema + liability selector + KRD matching engine (LP/QP)

---

## Phase 3 — AI Integration

- YAML product SDK + State Machine framework; RAG knowledge base; document parsing pipeline
- AI codegen + parity automation (tolerance + classification per ADR-033)
- Assisted onboarding: 10-stage flow with chief actuary in the loop (M5)
- From-scratch design: archetype-driven wizard (M6)

---

## Phase 4 — Assumption Authoring

- Statistical infrastructure: credibility, graduation, GLM, survival, advisor, validation (ADR-030)
- External adapter framework (iPACE / Flow 2 — ingestion may migrate to the External Data Ingestion Module under Section 4.6)
- Candidate authoring → statistical fit → internal review → regulatory justification pack (HKIA-ready; M7)

---

## Phase 5 — Data Lake Integration

Lake Functions the Data Lake team owns (post-Phase-5, currently Cashfluid runs on CSV):

- One-way PII-masked daily sync from Coreflexi Core Admin DB into Raw zone
- Standardisation: typing, dedup, code-list harmonisation against MDM
- Curated `policy_model_point` table on the Cashfluid-shape contract (Phase 5 Step a co-sign; semver)
- Per-block onboarding template — source-mapping + ETL extension + Curated partition per new block (~10 cal-wks per block)
- Reference-data versioning for assumption sets and scenario sets
- Curated-zone publication API for Cashfluid-authored assumption tables
- Snapshotting of projection runs (point-in-time, audit-stamped)
- Lineage capture (source field through measurement output)
- Data quality validation on inputs and outputs
- Reporting snapshot zone for Cashfluid reporting outputs (cross-module reuse)

**Open question (Shanshan / Michael / Matt):** where do policy-level derived fields live — Lake (uniform across modules) or Cashfluid (kept with actuarial logic)? Phase 5 steps are written basis-agnostic until resolved.

---

## Milestones

| Milestone | Content |
|---|---|
| M2 | Lake live |
| M3 | SAA MVP (daily SAA scheduler) |
| M5 | Onboarding alpha (10-stage AI flow) |
| M5.5 | Wizard FE alpha |
| M6 | From-scratch design |
| M7 | Assumption authoring + HKIA regulatory justification pack |
| M8 | Live PCR/MCR/MOCE cutover for daily SAA cycle |

---

## Key inputs and outputs

### Inputs
- **From Data Lake (Curated):** Policy data on `policy_model_point` schema; assumption tables (mortality/lapse/discount/expense/dividend/PUA/morbidity) with provenance; scenario sets (HKFRS17, HKRBC, stress)
- **From HKRBC Reporting:** Pillar 1 output contract draft (Phase 2); live PCR/MCR/MOCE for daily SAA cycle (M8)
- **From Governance (transitional):** Board-set PCRStub figure (Phase 2); investment guidelines
- **External (Flow 1 — direct):** Public market data (rates/FX/indices/proxy ESG); in-house RN-ESG codebase; asset-manager metric conventions; real-world asset projections (future)
- **External (Flow 2 — via Ingestion Module):** Experience studies (SOA, HKIA mortality, reinsurer); legacy product documentation and parity outputs

### Outputs
- **To Data Lake (Curated):** Best-estimate liability cashflows (41-col Parquet); projection results + reserves; HKFRS17 measurement components (CF, RA inputs); 1,000-scenario stochastic outputs; approved assumption tables with provenance
- **To HKRBC Reporting:** Stable BEL cashflow contract (semver); 1,000 ESG scenarios + RA inputs for PCR/MCR/MOCE
- **To Moody's 2.x:** BEL cashflow contract (CF, Assumptions, RA inputs) for HKFRS17 measurement
- **To Sun 2.x:** BEL cashflow contract published as stable downstream consumable
- **To Governance:** Convergence-failure review-queue entries; onboarding decision logs (audit-grade, signed by chief actuary)
- **To Compliance:** Regulatory justification pack for HKIA submission (Phase 4)
- **To Risk/Capital/Investment:** Daily SAA artefact — weights, reserve requirement, dividend scale (from M3)
