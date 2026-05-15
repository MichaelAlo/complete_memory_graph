# Module: Moody's 2.x

**Lead:** Betty Pun (co-lead), Shanshan Gu (co-lead)
**Tech reviewer:** Luke Lai
**Status:** In-build
**Last reviewed:** 2026-05-15

---

## What this module owns

Moody's 2.x is the HKFRS17 insurance contract measurement and disclosure engine. It owns:
- HKFRS17 measurement logic: BBA (Building Blocks Approach), VFA (Variable Fee Approach), PAA (Premium Allocation Approach)
- CSM (Contractual Service Margin) roll-forward
- RA (Risk Adjustment) calculation
- OCI (Other Comprehensive Income) presentation
- HKFRS17 disclosures and journal generation
- Experience variance analysis (ECF vs ACF)

---

## Reads from Lake

| Dataset | Schema | Purpose |
|---|---|---|
| ECF outputs from Cashfluid | nexus_curated | HKFRS17 BBA/VFA measurement inputs |
| ACF (Actual Cashflows) | nexus_curated | Experience variance analysis (ECF vs ACF) |
| dim_policy (mastered) | nexus_curated | Policy cohort grouping for measurement |
| dim_product (mastered) | nexus_curated | HKFRS17 model classification (BBA/VFA/PAA) |
| Expense feeds | nexus_curated | Expense allocation to HKFRS17 groups |
| dim_calendar | nexus_curated | Reporting period anchoring |
| dim_currency | nexus_curated | Foreign currency translation |
| ref_codelist | nexus_curated | Code list validation |

---

## Writes back to Lake

| Dataset | Schema | Content |
|---|---|---|
| HKFRS17 disclosures | nexus_curated | Disclosure tables for financial statements |
| Journal feeds to Sun 2.x | nexus_curated | HKFRS17 JEs for GL posting |
| CSM roll-forward | nexus_curated | CSM movement tables |
| Disclosure evidence | nexus_snapshot | Immutable disclosure artefacts with release tag |

---

## Lake Functions this module depends on

- **Ingestion + standardisation** — Policy, Product, ACF data landed and standardised
- **MDM survivorship** — golden-record Policy and Product consumed for cohort grouping
- **Cashfluid outputs** — ECF must be published to Lake before Moody's 2.x can run
- **Reference data publication** — Calendar, Currency/FX
- **Snapshot publication** — disclosure artefacts frozen with release tag

---

## Governance interaction

Moody's 2.x produces:
- HKFRS17 disclosure tables consumed by Governance for financial statement preparation
- Journal feeds to Sun 2.x for GL posting
- Approval artefacts frozen to nexus_snapshot as evidence

---

## Module dependency notes

- **Moody's 2.x depends on Cashfluid outputs** — ECF must be published to nexus_curated before Moody's 2.x can run
- **Moody's 2.x does not depend on HKRBC Reporting** — the two run independently; Sun 2.x derives the Delta book from both post-posting
- **Sun 2.x depends on Moody's 2.x JE outputs** for Delta book derivation

---

## Open items

<!-- stub: update after module plan lands 2026-05-18 -->

- Full Moody's 2.x module plan due 2026-05-18
- Expense allocation pre-aggregation: Lake Function vs Moody's 2.x? (see open-questions.md)

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub from module-binding-register.md | Michael Alo | — |
