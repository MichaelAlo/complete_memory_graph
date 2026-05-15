# Module: Coreflexi / Core Admin DB

**Lead:** Wenbo (Coreflexi 2.x lead)
**Documentation owner:** Kai Wang (Core Admin DB documentation and upstream source context)
**Tech reviewer:** Kai Wang (upstream code reviews)
**Status:** Operational (outside Project Nexus boundary)
**Last reviewed:** 2026-05-15

---

## What this module owns

Coreflexi is the operational policy administration system. It is the **source of record** for all insurance policy, customer, and product data. Coreflexi sits **outside the Project Nexus boundary** — the Data Lake extracts from it but does not govern it.

Coreflexi owns:
- Policy lifecycle management (new business, amendments, claims, surrenders, maturities)
- Customer record management
- Product catalogue management
- Operational business rules and actuarial functions (some functions may be temporarily retained in Coreflexi if migration deadlines require it — must be explicitly triaged and logged as GitLab issues)

---

## Reads from Lake

None required initially. Coreflexi is a source-only system from the Lake's perspective.

---

## Writes back to Lake (extraction only)

| Dataset | Schema | Content |
|---|---|---|
| nexus_raw.customers | nexus_raw | Customer records (PII masked at extraction) |
| nexus_raw.policies | nexus_raw | Policy records |
| nexus_raw.products | nexus_raw | Product records |

Extraction is **one-way**: Core Admin DB → nexus_raw. The Lake does not write back to Coreflexi.

---

## Lake Functions this module depends on

N/A — Coreflexi is an upstream source only. The Lake extracts from it; Coreflexi does not consume Lake outputs.

---

## Governance interaction

Indirect — Coreflexi data flows through the Lake and is consumed by downstream modules. Audit evidence links back to Coreflexi records via the `customer_id` and `policy_id` source keys preserved in the Lake.

---

## Extraction from Core Admin DB

See [sources/core-admin-db.md](../sources/core-admin-db.md) for full extraction detail:
- Date-windowed batch extraction (`WHERE updated_at > last_cut AND <= extract_cut`)
- PII masking applied at extraction boundary (PDPO — ADR-008)
- Implemented in `src/ingest/core_admin/extract.py`

---

## Open items

- CDC mechanism for Core Admin DB to be confirmed with Kai Wang
- Urgent Lake Functions currently in Coreflexi: triage required by 2026-05-18 (who — Luke/Coreflexi/Data Lake — has bandwidth to migrate)
- Full table list to extract: only customers, policies, products configured so far — module plans will determine if additional tables are needed

---

## Change history

| Date | Change | Author | Release |
|---|---|---|---|
| 2026-05-15 | Initial stub from module-binding-register.md and handover docs | Michael Alo | — |
