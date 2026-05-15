# Open Questions

**Sources:** `project-nexus-data-flow-architecture.html` (section 13), `project_nexus_handover_updated_sources.md`

This page tracks questions that were open in the source documents and have not yet been resolved by an ADR in `context/decisions.md`. Move items to decisions.md once resolved.

---

## Key deadlines

| Deliverable | Owner | Deadline |
|---|---|---|
| Per-module project plans (all 10 modules) | Each module lead | **2026-05-18** |
| MDM first draft | Shanshan Gu & Michael Alo | **2026-05-22** |
| Final Lake Functions vs Module Functions per module | Data Lake team + module owners (after plans land) | After 2026-05-18 |

## Architectural and boundary questions

| Question | Current position | Owner | Deadline / Status |
|---|---|---|---|
| Final per-module Lake Function vs Module Function split | Working principle defined (§4.5, §2); formal per-module confirmation pending | Each module lead + Shanshan/Michael/Matt | After 2026-05-18 |
| Policy-level derived fields: Lake (uniform) or Cashfluid (with actuarial logic)? | TBD; Phase 5 steps written basis-agnostic | Shanshan / Michael / Matt | Open |
| Expense allocation pre-aggregation (GL data → HKFRS17 cohort buckets): Lake or Cashfluid? | Assumed Lake Function — to be confirmed | Shanshan / Michael / Matt | Open |
| Reinsurance gross/net split | TBD; intentionally excluded from current Cashfluid scope | Matt Burlage / actuarial | Open — separate discussion |
| Governance app-to-module binding in practice | Governance owns reporting/oversight surface; detailed workflow not yet designed | Bill Nichol / Betty Pun | Not started |
| Pillar 2 (ORSA governance) placement: HKRBC vs Governance | May sit more naturally in Governance (Bill/Betty) | Matt Burlage / Bill Nichol | Open |
| Pillar 3 (public disclosure templates) placement | Across Governance / Compliance / Strategy | Matt Burlage / Bill Nichol | Open |
| Management reporting aggregations boundary in Sun 2.x | Grey area — Sun vs Lake; check with Sun and Data Lake leads | Shanshan / Betty | Open |
| Which urgent Coreflexi Lake Functions need to be done short-term | Triage required; who (Luke/Coreflexi, Data Lake, or elsewhere) has bandwidth | Luke Lai + Shanshan + Michael | **Urgent — by 2026-05-18** |

---

## Reporting and governance questions

| Question | Current position | Owner | Status |
|---|---|---|---|
| Governance-side workflow details (board packs, conduct workflow, attestation flow) | Not started — slower timeline with a task to build out app ideas | Bill Nichol / Betty Pun | Open |
| Review cadence between project leads and tech reviewers | Resolved: project leads engage reviewers at their own discretion at sensible checkpoints. No enforced per-PR gate. | Matt Burlage | Resolved |

---

## Delivery and implementation questions

| Question | Current position | Owner | Status |
|---|---|---|---|
| Which urgent reporting-period functions must temporarily remain in Coreflexi | Explicitly deferred to triage; must be logged as GitLab issues when identified | Matt Burlage | Open — triage required |
| Per-dataset Flow 1 vs Flow 2 assignment | Needs to be recorded in MDM per external feed | Data Lake team | Open |
| Compliance module boundaries | Several Lake vs Module decisions still open | Compliance module owner | Open |
| Per-module detailed architecture and project timelines | Need to be completed by each module owner | Module owners | Open |

---

## Questions answered in the source documents

These were open questions that the architecture documents explicitly addressed:

| Question | Answer | Source |
|---|---|---|
| Which functions are generic Lake Functions vs module functions? | Generic data-engineering and governance → Lake; specialist actuarial, accounting, regulatory, compliance, transactional → modules | data-flow-architecture.html §7 |
| Should reporting marts sit in Governance or the Data Lake? | Governance owns the marts; the Data Lake retains immutable reporting snapshots behind them | data-flow-architecture.html §6 |
| Which source data must be mastered first in MDM? | Customer, Policy, Product, CoA mapping, Currency, Calendar are first-wave; Counterparty is likely second-wave | mdm.html §4 |

---

## How to resolve an open question

1. Raise a GitLab issue.
2. Gather input from the relevant owner.
3. Record the decision via `/decision` → appends to `context/decisions.md`.
4. Update this page: move the item to the "answered" table or delete it.
5. Update affected wiki pages (`lake-functions-registry.md`, `module-binding-register.md`, etc.).
