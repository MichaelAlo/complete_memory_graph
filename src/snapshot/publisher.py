"""
Publish an immutable reporting snapshot from nexus_curated to nexus_snapshot.

Snapshots are append-only (INSERT, not upsert). Each call produces a new snapshot_id.
release_tag is required and must be set on ctx before calling.
"""

import uuid
from datetime import UTC, datetime
from typing import Any, cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config
from src.lib.job_log import log_run_complete, log_run_start
from src.lib.run_context import RunContext


def publish_snapshot(
    ctx: RunContext,
    cfg: Config,
    report_name: str,
    source_query: str,
    approver: str = "",
) -> str:
    """
    Freeze certified curated data into nexus_snapshot as an immutable evidence record.

    source_query runs against nexus_curated.
    Returns the snapshot_id (UUID) for the new snapshot.
    Raises ValueError if release_tag is not set.
    """
    if not ctx.release_tag:
        raise ValueError("release_tag is required to publish a reporting snapshot")

    ctx.log("snapshot.publish.start", report=report_name)
    job_name = f"snapshot.publish.{report_name}"
    snapshot_id = str(uuid.uuid4())
    snapshotted_at = datetime.now(UTC).isoformat(sep=" ", timespec="microseconds")

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
    log_run_start(conn, ctx, job_name)

    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(source_query)
        rows: list[dict[str, Any]] = cur.fetchall()  # type: ignore[assignment]
        cur.close()

        if not rows:
            log_run_complete(conn, ctx, 0, 0, "fail", "source_query returned 0 rows")
            raise ValueError(f"publish_snapshot: source_query returned 0 rows for {report_name!r}")

        augmented = [
            {
                **row,
                "snapshot_id": snapshot_id,
                "report_name": report_name,
                "run_id": ctx.run_id,
                "source_cut": ctx.extract_cut or "",
                "release_tag": ctx.release_tag,
                "approver": approver,
                "snapshotted_at": snapshotted_at,
            }
            for row in rows
        ]
        columns = list(augmented[0].keys())
        col_sql = ", ".join(f"`{c}`" for c in columns)
        placeholders = ", ".join("%s" for _ in columns)
        stmt = (
            f"INSERT INTO `{cfg.snapshot_schema}`.`{report_name}` "  # noqa: S608
            f"({col_sql}) VALUES ({placeholders})"
        )
        cur = conn.cursor()
        for row in augmented:
            cur.execute(stmt, list(row.values()))
        conn.commit()
        cur.close()

        log_run_complete(conn, ctx, len(rows), len(augmented), "pass")
        ctx.log("snapshot.publish.complete", report=report_name, snapshot_id=snapshot_id)
        return snapshot_id

    except ValueError:
        raise
    except Exception as exc:
        log_run_complete(conn, ctx, 0, 0, "fail", str(exc))
        raise
    finally:
        conn.close()
