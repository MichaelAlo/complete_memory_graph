# Architecture

## System overview
[2-3 sentence description of the system shape]

## Components
| Component | Purpose | Location |
|---|---|---|
| [e.g. API layer] | [handles HTTP requests] | [src/api/] |
| [e.g. DB models] | [ORM models] | [src/models/] |
| [e.g. Services] | [business logic] | [src/services/] |

## Data flow
[Describe the main request/data path through the system]
e.g. Request → API router → Service layer → Repository → DB

## External dependencies
| Dependency | Purpose | Version |
|---|---|---|
| [e.g. OpenAI API] | [LLM inference] | [gpt-4o] |
| [e.g. PostgreSQL] | [primary store] | [16] |

## Key invariants
- [Things that must always be true, e.g. "All DB writes go through the service layer"]
- [e.g. "Auth is always validated at the router level, never inside services"]

## Known weak points / tech debt
- [e.g. No retry logic on external API calls yet]
- [e.g. Missing index on users.email]

## Last updated
[YYYY-MM-DD] — [what changed]