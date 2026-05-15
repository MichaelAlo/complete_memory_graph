"""
Publish Currency/FX rates to nexus_curated.dim_currency.

Flow 1 pattern: rates arrive as a structured feed from the asset manager.
Caller loads the feed into a list[dict] and passes it here for curation.
"""

from datetime import UTC, datetime
from typing import cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config
from src.lib.job_log import log_run_complete, log_run_start
from src.lib.run_context import RunContext

_JOB_NAME = "curate.reference.currency"
_TARGET_TABLE = "dim_currency"


def publish(
    ctx: RunContext,
    cfg: Config,
    rates: list[dict[str, object]],
) -> int:
    """
    Publish FX rates to nexus_curated.dim_currency.

    Each rate dict must contain: currency_code, rate_date, rate_to_hkd.
    """
    if not ctx.release_tag:
        raise ValueError("release_tag is required to publish curated reference data")
    if not rates:
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
            {**row, "_run_id": ctx.run_id, "_source_cut": ctx.extract_cut or "",
             "_release_tag": ctx.release_tag, "_certified_at": certified_at}
            for row in rates
        ]
        columns = list(augmented[0].keys())
        col_sql = ", ".join(f"`{c}`" for c in columns)
        placeholders = ", ".join("%s" for _ in columns)
        update_sql = ", ".join(
            f"`{c}` = VALUES(`{c}`)" for c in columns
            if c not in ("currency_code", "rate_date")
        )
        stmt = (
            f"INSERT INTO `{cfg.curated_schema}`.`{_TARGET_TABLE}` ({col_sql}) "  # noqa: S608
            f"VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_sql}"
        )
        cur = conn.cursor()
        for row in augmented:
            cur.execute(stmt, list(row.values()))  # type: ignore[arg-type]
        conn.commit()
        cur.close()

        log_run_complete(conn, ctx, len(rates), len(rates), "pass")
        ctx.log(f"{_JOB_NAME}.complete", rows=len(rates))
        return len(rates)

    except Exception as exc:
        log_run_complete(conn, ctx, 0, 0, "fail", str(exc))
        raise
    finally:
        conn.close()
