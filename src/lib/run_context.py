import logging
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class RunContext:
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    extract_cut: str | None = None   # ISO date or source batch ID
    release_tag: str | None = None

    def log(self, msg: str, **extra: object) -> None:
        logging.info({"run_id": self.run_id, "msg": msg, **extra})

    def log_error(self, msg: str, **extra: object) -> None:
        logging.error({"run_id": self.run_id, "msg": msg, **extra})

    def as_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at.isoformat(),
            "extract_cut": self.extract_cut,
            "release_tag": self.release_tag,
        }
