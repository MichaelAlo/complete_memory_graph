# People and Stakeholders

## Team

| Person | Role | Owns | Notes |
|---|---|---|---|
| Michael Alo | Data Lake lead | Wiki, MDM maintenance model, canonical domain definitions, change-control workflow | Primary Claude Code user |
| Shanshan Gu | Data Lake co-lead; Sun 2.x lead | Data Lake / MDM build; Sun 2.x GL system | Reviews Data Lake architecture |
| Kai Wang | Core Admin DB owner | Core Admin DB documentation; upstream source and extraction context | Tech reviewer: upstream code (Coreflexi, Core Admin DB extraction) |
| Luke Lai | Downstream tech reviewer | Data Lake implementation review; interim Coreflexi functions | Tech reviewer: downstream code (Data Lake + all inside Nexus boundary) |
| Mark Chen | Tech reviewer | Code reviews | Third tech reviewer alongside Kai and Luke |
| Matt Burlage | Architecture owner; Cashfluid lead | Architecture; Cashfluid actuarial platform; HKRBC support; Strategy co-lead | Sets the architecture baseline |
| KJ Lin | Cashfluid support; Moody's 2.x co-lead; HKRBC lead | HKRBC Reporting | Pillar 1 capital calculations |
| Betty Pun | Sun 2.x support; Moody's 2.x co-lead; Compliance co-lead; Governance co-lead | HKFRS17 measurement; Compliance; Governance | Across multiple modules |
| Alex Moore | Transactional lead | Deal evaluation, structuring, governance | Portfolio transfers and M&A |
| Rui Huang | Transactional co-lead | Deal logic and document generation | |
| Bill Nichol | Governance co-lead; Compliance support; Strategy co-lead | Board/committee governance; risk governance | |
| Yang Mingyang | Governance support; Compliance co-lead | Compliance regulatory and data/privacy | |
| Wenbo | Coreflexi 2.x lead | Core policy administration system | Outside Project Nexus boundary |

## Module owners

Each module (Cashfluid, Sun 2.x, Moody's 2.x, HKRBC, Transactional, Governance) has an owner responsible for:
- Validating source-of-record decisions.
- Confirming the Lake Function vs Module Function boundary for their domain.
- Approving changes that affect their module's inputs, outputs, or logic.

## Approval model

| Change type | Required approvers |
|---|---|
| Schema or semantic change | Domain data owner + affected module owner + Data Lake owner |
| Reporting or compliance impact | Add: Governance reviewer |
| PDPO / masking rule change | Add: Governance reviewer |
| Release tagging | Data Lake owner |

## Communication notes

- Architecture issues: raise as GitLab issues first.
- Escalation path: Michael Alo → Matt Burlage for architecture questions; Michael Alo → Kai Wang for upstream source questions.
- Wiki changes: Michael Alo proposes, Shanshan Gu reviews.
