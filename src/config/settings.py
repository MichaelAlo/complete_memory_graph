import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    # Lake DB (nexus_raw / nexus_std / nexus_curated / nexus_snapshot)
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # Source DB (Core Admin DB — separate connection, read-only)
    source_db_host: str = ""
    source_db_port: int = 3306
    source_db_name: str = ""
    source_db_user: str = ""
    source_db_password: str = ""

    initial_extract_from: str = "2020-01-01"

    raw_schema: str = "nexus_raw"
    std_schema: str = "nexus_std"
    curated_schema: str = "nexus_curated"
    snapshot_schema: str = "nexus_snapshot"


def load() -> Config:
    return Config(
        db_host=os.environ["NEXUS_DB_HOST"],
        db_port=int(os.environ.get("NEXUS_DB_PORT", "3306")),
        db_name=os.environ["NEXUS_DB_NAME"],
        db_user=os.environ["NEXUS_DB_USER"],
        db_password=os.environ["NEXUS_DB_PASSWORD"],
        source_db_host=os.environ.get("NEXUS_SOURCE_DB_HOST", ""),
        source_db_port=int(os.environ.get("NEXUS_SOURCE_DB_PORT", "3306")),
        source_db_name=os.environ.get("NEXUS_SOURCE_DB_NAME", ""),
        source_db_user=os.environ.get("NEXUS_SOURCE_DB_USER", ""),
        source_db_password=os.environ.get("NEXUS_SOURCE_DB_PASSWORD", ""),
        initial_extract_from=os.environ.get("NEXUS_INITIAL_EXTRACT_FROM", "2020-01-01"),
    )
