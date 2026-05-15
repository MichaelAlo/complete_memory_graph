"""
Publish harmonised code list reference tables to nexus_curated.ref_codelist.

Code lists are domain-canonical mappings (e.g. policy_status, product_type).
Each entry: list_name, source_code, canonical_code, description.
"""

from datetime import UTC, datetime
from typing import cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config
from src.lib.job_log import log_run_complete, log_run_start
from src.lib.run_context import RunContext

_JOB_NAME = "curate.reference.codelist"
_TARGET_TABLE = "ref_codelist"


def publish(
    ctx: RunContext,
    cfg: Config,
    entries: list[dict[str, object]],
) -> int:
    """
    Publish code list entries to nexus_curated.ref_codelist.

    Each entry must contain: list_name, source_code, canonical_code, description.
    """
    if not ctx.release_tag:
        raise ValueError("release_tag is required to publish curated reference data")
    if not entries:
        return 0

    conn = cast(
        mysql.connector.abstracts.MySQLConnectionAbstract,
        mysql.connector.connect(
            host=cfg.db_host,
            port=cfg.db_port,
            database=cfg.db_name,
            user=cfg.db_user,
            password=cfg.db_password,
        ),
    )
    log_run_start(conn, ctx, _JOB_NAME)

    try:
        certified_at = datetime.now(UTC).isoformat(sep=" ", timespec="microseconds")
        augmented = [
            {**e, "_run_id": ctx.run_id, "_source_cut": ctx.extract_cut or "",
             "_release_tag": ctx.release_tag, "_certified_at": certified_at}
            for e in entries
        ]
        columns = list(augmented[0].keys())
        col_sql = ", ".join(f"`{c}`" for c in columns)
        placeholders = ", ".join("%s" for _ in columns)
        update_sql = ", ".join(
            f"`{c}` = VALUES(`{c}`)" for c in columns
            if c not in ("list_name", "source_code")
        )
        stmt = (
            f"INSERT INTO `{cfg.curated_schema}`.`{_TARGET_TABLE}` ({col_sql}) "  # noqa: S608
            f"VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_sql}"
        )
        cur = conn.cursor()
        for e in augmented:
            cur.execute(stmt, list(e.values()))  # type: ignore[arg-type]
        conn.commit()
        cur.close()

        log_run_complete(conn, ctx, len(entries), len(entries), "pass")
        ctx.log(f"{_JOB_NAME}.complete", rows=len(entries))
        return len(entries)

    except Exception as exc:
        log_run_complete(conn, ctx, 0, 0, "fail", str(exc))
        raise
    finally:
        conn.close()
