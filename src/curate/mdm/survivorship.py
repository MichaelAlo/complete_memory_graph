"""
MDM survivorship contract.

Input:  list[dict] from nexus_std (one row per source candidate, same business key)
Output: list[MasteredRecord] with Type 2 SCD effective-dated versioning

Implementation is deferred until colleague's entity schema outputs land.
Each domain (Customer, Policy, Product, CoA, Currency, Calendar) will have a
separate survivorship function plugged in via MDMProvider (see contracts.py).

# MDM: implement with colleague's outputs
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class MasteredRecord:
    canonical_id: str
    business_key: str
    source_keys: dict[str, str]
    status: str                  # "active" | "inactive" | "merged"
    effective_from: date
    effective_to: date | None    # None = current open version
    provenance: str              # source system that won survivorship for this version


def assemble_golden_record(
    candidates: list[dict[str, object]],
    key_field: str,
    source_priority: list[str],
) -> MasteredRecord:
    """
    Apply survivorship rules to produce a golden record from candidate source rows.

    source_priority defines which source wins on attribute conflicts (index 0 = highest).
    Returns a MasteredRecord with effective_to=None (open/current version).

    # MDM: implement with colleague's outputs
    """
    raise NotImplementedError("Implement survivorship logic for domain entity")
