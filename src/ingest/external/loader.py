from enum import Enum

from src.config.settings import Config
from src.lib.run_context import RunContext


class IngestFlow(Enum):
    FLOW_1 = "flow_1"   # Direct-to-module: stable, contract-based, single consumer
    FLOW_2 = "flow_2"   # Lake-mediated: ad hoc, multi-consumer, or quality-variable


def load_external_feed(
    ctx: RunContext,
    cfg: Config,
    feed_name: str,
    flow: IngestFlow,
    source_path: str,
) -> int:
    """
    Load an external data feed into nexus_raw.

    Flow 1: direct-to-module feeds pass through with minimal transformation.
    Flow 2: multi-consumer feeds undergo full Lake validation, standardisation, and versioning.

    Returns the number of rows landed.
    """
    ctx.log("external.load.start", feed=feed_name, flow=flow.value, source=source_path)
    raise NotImplementedError(f"Implement loader for feed '{feed_name}' ({flow.value})")
