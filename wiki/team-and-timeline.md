# Team, Timelines, and Review Workflow

**Sources:** `nexus_architecture.html` (§2, §3, §6)

---

## Company context

- **PACE Solution Limited** — the organisation running Project Nexus.
- **MPL** (MyPace Life Limited) — the Hong Kong licensed insurance carrier. Regulatory authority: **HKIA** (Hong Kong Insurance Authority).

---

## Module leads and status

| Module | Lead(s) | Support | Status |
|---|---|---|---|
| Coreflexi 2.x | Wenbo | Mark | In active build |
| Data Lake & MDM & Wiki | Shanshan Gu & Michael Alo | Luke Lai | New build |
| Cashfluid | Matt Burlage | KJ Lin | In active build |
| Sun 2.x | Shanshan Gu | Betty Pun | In active build |
| Moody's 2.x | Betty Pun & KJ Lin | Matt Burlage | In active build |
| Transactional | Alex Moore & Rui Huang | — | In active build |
| HKRBC Reporting | KJ Lin | Matt Burlage | In active build |
| Governance | Bill Nichol & Betty Pun | Yang Mingyang | Not started |
| Compliance | Betty Pun & Yang Mingyang | Bill Nichol | Not started |
| Strategy | Matt Burlage & Bill Nichol & Betty Pun | — | Not started |

**Wiki owner:** Michael Alo — responsible for building the Wiki and proposing the maintenance model.
**Core Admin DB documentation:** Kai Wang — maintained separately from the Data Lake Wiki, but the Data Lake Wiki references it.

---

## Key deadlines

| Deliverable | Owner | Deadline |
|---|---|---|
| Per-module project plans (phased, with inputs/outputs/timeline) | Each module lead | **2026-05-18** |
| MDM first draft | Data Lake team (Shanshan, Michael) | **2026-05-22** |
| Final Lake Functions vs Module Functions list per module | Data Lake team + module owners, after plans land | After 2026-05-18 |
| External Data Ingestion Module design (Section 4.6) folded into Data Lake architecture and MDM | Data Lake team | With MDM delivery |
| Data Lake architecture review | Shanshan Gu & Luke Lai | Concurrent with MDM |

The Cashfluid project plan is explicitly the **structural reference** for what a module plan should look like (not a template — each module's phasing will differ).

---

## Tech review workflow

**Project leads build; tech team reviews.** The split is:

- **Kai Wang** — covers all *upstream* code: Coreflexi, Core Admin DB extraction, source-system integrations (pre-Data-Lake).
- **Luke Lai** — covers all *downstream* code: Data Lake and everything inside the Project Nexus boundary.
- **Mark Chen** — also performs tech reviews.

There is no enforced per-PR or per-gate cadence. Project leads reach out at their own discretion when they feel a review is needed. The operating principle: the project lead is responsible for engaging the reviewer at sensible checkpoints.

---

## Confirmed cross-cutting decisions (from §2)

- **ALM computation priority.** Computation stress points must be identified and prioritised, especially for interdependent calculations. Competitive advantage in ALM comes from configurable and rapid recalculation of asset allocations and reserve impacts. All data dependencies the ALM has must be understood and optimised.
- **Human-in-the-loop validation required on every project.** Every module plan must explicitly lay out where the human-in-the-loop validation step is. Example: Cashfluid requires a parity-check dashboard and an actuary sign-off checklist. Governance requires a chief compliance officer (or equivalent) to validate that structured data extracted from policies or HKIA guidelines is comprehensive.
- **All inputs and outputs must be thoroughly understood** before broader system development continues.
