# Module: Sun 2.x

**Lead:** Shanshan Gu
**Tech reviewer:** Luke Lai
**Status:** In-build
**Last reviewed:** 2026-05-15

---

## What this module owns

Sun 2.x is the GL (General Ledger) system for Project Nexus. It owns:
- Journal entry (JE) posting logic and GL operations
- Multi-book GL: HKFRS / HKFRS17 / HKRBC / Delta / Tax books on every JE line
- Financial close processing and balance production
- CoA (Chart of Accounts) application to journal lines
- RPT (Related-Party Transaction) dimension applied per JE line (via Lake's data-tagging service using MDM Counterparty `is_related_party` attribute)
- Delta book derivation: HKRBC minus HKFRS17 reversing entries (computed inside Sun after both modules have posted their JEs)

---

## Reads from Lake

| Dataset | Schema | Purpose |
|---|---|---|
| Journal feeds from Moody's 2.x | nexus_curated | HKFRS17 JE inputs |
| Journal feeds from HKRBC Reporting | nexus_curated | Capital JE inputs |
| CoA mapping (MDM) | nexus_curated | Account code harmonisation for posting |
| dim_calendar | nexus_curated | Period-close date anchoring |
| dim_currency | nexus_curated | FX retranslation |
| Counterparty MDM (is_related_party) | nexus_curated | RPT dimension tagging |
| ref_codelist | nexus_curated | Code list validation |

---

## Writes back to Lake

| Dataset | Schema | Content |
|---|---|---|
| Posted JE lines | nexus_curated | Validated journal entries with book dimension |
| Period balances | nexus_curated | GL balances by account, book, period |
| Close outputs | nexus_curated | Period-close run outputs |
| Reconciliation evidence | nexus_snapshot | Close reconciliation evidence with release tag |

---

## Lake Functions this module depends on

- **CoA mapping MDM** — canonical account codes must be mastered before Sun 2.x can post reliably
- **Reference data publication** — Calendar and Currency/FX required for close processing
- **RPT tagging service** — Lake's data-tagging service applies `is_related_party` from Counterparty MDM to every JE line
- **Snapshot publication** — close outputs frozen to nexus_snapshot
- **Lineage capture** — run_id traceability from source JE to posted balance

---

## Governance interaction

Sun 2.x outputs feed:
- Management reporting aggregations (boundary with Sun is an open question — see below)
- HKFRS17 disclosures (via Moody's 2.x)
- HKRBC capital returns
- Board packs and audit evidence (via Governance)

---

## Delta book design

Sun 2.x uses a **single event-sourced GL** with `book` as a first-class dimension on every JE line. Books: HKFRS / HKFRS17 / HKRBC / Delta / Tax.

The **Delta book** is derived inside Sun as: HKRBC minus HKFRS17 reversing entries. It is computed by Sun after both Moody's 2.x and HKRBC Reporting have posted their JEs — Moody's 2.x and HKRBC do not cross-read each other's outputs.

---

## Module dependency notes

- **Sun 2.x depends on Moody's 2.x and HKRBC Reporting outputs** — both must post their JEs before Sun 2.x can derive the Delta book
- **CoA mapping MDM must be mastered first** — first-wave MDM prerequisite for Sun 2.x

---

## Open items

<!-- stub: update after module plan lands 2026-05-18 -->

- Management reporting aggregations: Sun vs Lake boundary is grey — confirm with Shanshan and Betty (see open-questions.md)
- Full Sun 2.x module plan due 2026-05-18

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub from module-binding-register.md | Michael Alo | — |
