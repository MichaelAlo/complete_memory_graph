"""
Publish Calendar dimension to nexus_curated.dim_calendar.

Source: nexus_std.dim_calendar (or seed file if not yet extracted).
Generates one row per calendar date for the configured range.
"""

from datetime import UTC, date, datetime, timedelta
from typing import cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config
from src.lib.job_log import log_run_complete, log_run_start
from src.lib.run_context import RunContext

_JOB_NAME = "curate.reference.calendar"
_TARGET_TABLE = "dim_calendar"


def _generate_dates(start: date, end: date) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    current = start
    while current <= end:
        rows.append(
            {
                "calendar_date": current.isoformat(),
                "year": current.year,
                "month": current.month,
                "day": current.day,
                "day_of_week": current.weekday(),
                "is_weekend": current.weekday() >= 5,
                "quarter": (current.month - 1) // 3 + 1,
            }
        )
        current += timedelta(days=1)
    return rows


def publish(
    ctx: RunContext,
    cfg: Config,
    start_date: date,
    end_date: date,
) -> int:
    """Publish calendar rows for [start_date, end_date] to nexus_curated.dim_calendar."""
    if not ctx.release_tag:
        raise ValueError("release_tag is required to publish curated reference data")

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
        rows = _generate_dates(start_date, end_date)
        certified_at = datetime.now(UTC).isoformat(sep=" ", timespec="microseconds")
        augmented = [
            {**row, "_run_id": ctx.run_id, "_source_cut": ctx.extract_cut or "",
             "_release_tag": ctx.release_tag, "_certified_at": certified_at}
            for row in rows
        ]
        columns = list(augmented[0].keys())
        col_sql = ", ".join(f"`{c}`" for c in columns)
        placeholders = ", ".join("%s" for _ in columns)
        update_sql = ", ".join(f"`{c}` = VALUES(`{c}`)" for c in columns if c != "calendar_date")
        stmt = (
            f"INSERT INTO `{cfg.curated_schema}`.`{_TARGET_TABLE}` ({col_sql}) "  # noqa: S608
            f"VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_sql}"
        )
        cur = conn.cursor()
        for row in augmented:
            cur.execute(stmt, list(row.values()))  # type: ignore[arg-type]
        conn.commit()
        cur.close()

        log_run_complete(conn, ctx, len(rows), len(rows), "pass")
        ctx.log(f"{_JOB_NAME}.complete", rows=len(rows))
        return len(rows)

    except Exception as exc:
        log_run_complete(conn, ctx, 0, 0, "fail", str(exc))
        raise
    finally:
        conn.close()
