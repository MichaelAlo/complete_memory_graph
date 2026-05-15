"""
MDMProvider protocol — the interface the MDM layer must satisfy.

The colleague's entity-schema work plugs in by implementing this Protocol.
"""

from typing import Protocol

from src.curate.mdm.survivorship import MasteredRecord
from src.lib.run_context import RunContext


class MDMProvider(Protocol):
    def get_golden_records(self, domain: str, as_of: str) -> list[MasteredRecord]: ...

    def upsert_golden_records(
        self, domain: str, records: list[MasteredRecord], ctx: RunContext
    ) -> int: ...
