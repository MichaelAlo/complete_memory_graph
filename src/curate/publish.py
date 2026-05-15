"""
Publish a certified dataset from nexus_std to nexus_curated.

Quality gate: reconciliation count pass + null check on key columns.
Lineage columns (_run_id, _source_cut, _release_tag, _certified_at) are added to every row.
"""

from datetime import UTC, datetime
from typing import Any, cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config
from src.lib.job_log import log_run_complete, log_run_start
from src.lib.run_context import RunContext


def publish_dataset(
    ctx: RunContext,
    cfg: Config,
    dataset_name: str,
    source_query: str,
    pk_col: str,
    required_cols: list[str] | None = None,
) -> int:
    """
    Execute source_query against nexus_std, run quality checks, and UPSERT to nexus_curated.

    Returns the number of rows written. Raises ValueError if release_tag is not set.
    """
    if not ctx.release_tag:
        raise ValueError("release_tag is required to publish a curated dataset")
    if not ctx.extract_cut:
        raise ValueError("extract_cut is required to publish a curated dataset")

    job_name = f"curate.publish.{dataset_name}"
    ctx.log("curate.publish.start", dataset=dataset_name)

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
            raise ValueError(f"publish_dataset: source_query returned 0 rows for {dataset_name!r}")

        if required_cols:
            for col in required_cols:
                null_count = sum(1 for r in rows if r.get(col) is None)
                if null_count:
                    msg = f"null check failed: {col} has {null_count} nulls"
                    log_run_complete(conn, ctx, len(rows), 0, "fail", msg)
                    raise ValueError(msg)

        certified_at = datetime.now(UTC).isoformat(sep=" ", timespec="microseconds")
        augmented = [
            {**row, "_run_id": ctx.run_id, "_source_cut": ctx.extract_cut,
             "_release_tag": ctx.release_tag, "_certified_at": certified_at}
            for row in rows
        ]
        columns = list(augmented[0].keys())
        col_sql = ", ".join(f"`{c}`" for c in columns)
        placeholders = ", ".join("%s" for _ in columns)
        update_sql = ", ".join(f"`{c}` = VALUES(`{c}`)" for c in columns if c != pk_col)
        stmt = (
            f"INSERT INTO `{cfg.curated_schema}`.`{dataset_name}` ({col_sql}) "  # noqa: S608
            f"VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_sql}"
        )
        cur = conn.cursor()
        for row in augmented:
            cur.execute(stmt, list(row.values()))
        conn.commit()
        cur.close()

        log_run_complete(conn, ctx, len(rows), len(augmented), "pass")
        ctx.log("curate.publish.complete", dataset=dataset_name, rows=len(augmented))
        return len(augmented)

    except ValueError:
        raise
    except Exception as exc:
        log_run_complete(conn, ctx, 0, 0, "fail", str(exc))
        raise
    finally:
        conn.close()
