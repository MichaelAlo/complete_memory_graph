"""
Batch extractor: Core Admin DB → nexus_raw.

Date-windowed pattern: WHERE updated_at > last_cut AND updated_at <= extract_cut.
last_cut is the source_cut of the last successful run for this table; on first run
uses Config.initial_extract_from. PII is masked before any row is written.
"""

from datetime import UTC, datetime
from typing import Any, cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config
from src.ingest.core_admin.table_config import TABLES, TableConfig
from src.lib.job_log import log_run_complete, log_run_start
from src.lib.run_context import RunContext

_JOB_PREFIX = "core_admin.extract"


def _source_connection(cfg: Config) -> mysql.connector.abstracts.MySQLConnectionAbstract:
    return cast(
        mysql.connector.abstracts.MySQLConnectionAbstract,
        mysql.connector.connect(
            host=cfg.source_db_host,
            port=cfg.source_db_port,
            database=cfg.source_db_name,
            user=cfg.source_db_user,
            password=cfg.source_db_password,
        ),
    )


def _lake_connection(cfg: Config) -> mysql.connector.abstracts.MySQLConnectionAbstract:
    return cast(
        mysql.connector.abstracts.MySQLConnectionAbstract,
        mysql.connector.connect(
            host=cfg.db_host,
            port=cfg.db_port,
            database=cfg.db_name,
            user=cfg.db_user,
            password=cfg.db_password,
        ),
    )


def _last_cut(
    lake_conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    job_name: str,
    fallback: str,
) -> str:
    cur = lake_conn.cursor()
    cur.execute(
        "SELECT source_cut FROM nexus_raw.job_runs "
        "WHERE job_name = %s AND validation_result = 'pass' "
        "ORDER BY completed_at DESC LIMIT 1",
        (job_name,),
    )
    row = cur.fetchone()
    cur.close()
    return str(row[0]) if row else fallback  # type: ignore[index]


def _mask_pii(row: dict[str, object], pii_fields: frozenset[str]) -> dict[str, object]:
    return {k: "***" if k in pii_fields else v for k, v in row.items()}


def _upsert_rows(
    lake_conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    schema: str,
    table: str,
    rows: list[dict[str, object]],
    pk_col: str,
    run_id: str,
    source_cut: str,
) -> None:
    if not rows:
        return
    loaded_at = datetime.now(UTC).isoformat(sep=" ", timespec="microseconds")
    augmented = [
        {**row, "_run_id": run_id, "_source_cut": source_cut, "_loaded_at": loaded_at}
        for row in rows
    ]
    columns = list(augmented[0].keys())
    col_sql = ", ".join(f"`{c}`" for c in columns)
    placeholders = ", ".join("%s" for _ in columns)
    update_sql = ", ".join(
        f"`{c}` = VALUES(`{c}`)" for c in columns if c != pk_col
    )
    stmt = (
        f"INSERT INTO `{schema}`.`{table}` ({col_sql}) VALUES ({placeholders}) "  # noqa: S608
        f"ON DUPLICATE KEY UPDATE {update_sql}"
    )
    cur = lake_conn.cursor()
    for row in augmented:
        cur.execute(stmt, list(row.values()))  # type: ignore[arg-type]
    lake_conn.commit()
    cur.close()


def extract_table(
    ctx: RunContext,
    cfg: Config,
    table_name: str,
) -> int:
    """
    Extract one Core Admin DB table into nexus_raw for ctx.extract_cut.

    Returns the number of rows landed. Raises if ctx.extract_cut is not set.
    """
    if not ctx.extract_cut:
        raise ValueError("ctx.extract_cut must be set before calling extract_table")

    tcfg: TableConfig = TABLES[table_name]
    job_name = f"{_JOB_PREFIX}.{table_name}"

    lake_conn = _lake_connection(cfg)
    log_run_start(lake_conn, ctx, job_name)

    try:
        last = _last_cut(lake_conn, job_name, cfg.initial_extract_from)
        source_conn = _source_connection(cfg)
        try:
            cur = source_conn.cursor(dictionary=True)
            cur.execute(  # noqa: S608
                f"SELECT * FROM `{tcfg.source_table}` "
                f"WHERE `{tcfg.updated_at_col}` > %s "
                f"AND `{tcfg.updated_at_col}` <= %s "
                f"ORDER BY `{tcfg.updated_at_col}`",
                (last, ctx.extract_cut),
            )
            raw_rows: list[dict[str, Any]] = cur.fetchall()  # type: ignore[assignment]
            cur.close()
        finally:
            source_conn.close()

        masked = [_mask_pii(row, tcfg.pii_fields) for row in raw_rows]
        _upsert_rows(
            lake_conn, cfg.raw_schema, tcfg.raw_table, masked,
            tcfg.pk_col, ctx.run_id, ctx.extract_cut,
        )

        log_run_complete(lake_conn, ctx, len(raw_rows), len(masked), "pass")
        ctx.log(f"{job_name}.complete", rows=len(masked))
        return len(masked)

    except Exception as exc:
        log_run_complete(lake_conn, ctx, 0, 0, "fail", str(exc))
        raise
    finally:
        lake_conn.close()


def extract_batch(ctx: RunContext, cfg: Config, extract_cut: str) -> dict[str, int]:
    """Extract all configured Core Admin DB tables for the given extract_cut."""
    ctx.extract_cut = extract_cut
    return {name: extract_table(ctx, cfg, name) for name in TABLES}
