from datetime import UTC, datetime
from typing import Any, cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config
from src.lib.job_log import log_run_complete, log_run_start
from src.lib.run_context import RunContext
from src.standardise.errors import StandardisationGateError
from src.standardise.table_config import TABLE_CONFIG


def run(
    ctx: RunContext,
    cfg: Config,
    source_table: str,
    target_table: str,
) -> int:
    """
    Standardise records from nexus_raw into nexus_std.

    Steps: type coercion → deduplication → code-list harmonisation → quality gate.
    Returns the number of rows written to nexus_std.
    Raises StandardisationGateError if the quality gate fails.
    """
    ctx.log("standardise.run.start", source=source_table, target=target_table)
    if not ctx.extract_cut:
        raise ValueError("ctx.extract_cut must be set")

    tcfg = TABLE_CONFIG[source_table]
    job_name = f"standardise.{source_table}"

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
        cur.execute(  # noqa: S608
            f"SELECT * FROM `{cfg.raw_schema}`.`{source_table}` WHERE `_source_cut` = %s",
            (ctx.extract_cut,),
        )
        raw_rows: list[dict[str, Any]] = cur.fetchall()  # type: ignore[assignment]
        cur.close()

        coerced = [_coerce(row, tcfg.type_map) for row in raw_rows]
        deduped = deduplicate(coerced, tcfg.business_key)
        harmonised = [_harmonise(row, tcfg.codelist_maps) for row in deduped]

        failed = _gate(harmonised, tcfg.required_fields)
        if failed:
            log_run_complete(conn, ctx, len(raw_rows), 0, "fail", "; ".join(failed))
            raise StandardisationGateError(source_table, failed)

        _upsert(conn, cfg.std_schema, target_table, harmonised, tcfg.business_key[0], ctx)
        log_run_complete(conn, ctx, len(raw_rows), len(harmonised), "pass")
        return len(harmonised)

    except StandardisationGateError:
        raise
    except Exception as exc:
        log_run_complete(conn, ctx, 0, 0, "fail", str(exc))
        raise
    finally:
        conn.close()


def _coerce(row: dict[str, Any], type_map: dict[str, type]) -> dict[str, Any]:
    out = dict(row)
    for col, typ in type_map.items():
        if col in out and out[col] is not None:
            out[col] = typ(out[col])
    return out


def _harmonise(row: dict[str, Any], codelist_maps: dict[str, dict[str, str]]) -> dict[str, Any]:
    out = dict(row)
    for col, mapping in codelist_maps.items():
        if col in out and isinstance(out[col], str):
            out[col] = harmonise_codelist(out[col], mapping)
    return out


def _gate(rows: list[dict[str, Any]], required_fields: list[str]) -> list[str]:
    failed: list[str] = []
    if not rows:
        failed.append("row_count=0")
    for field in required_fields:
        null_count = sum(1 for r in rows if r.get(field) is None)
        if null_count:
            failed.append(f"nulls:{field}={null_count}")
    return failed


def _upsert(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    schema: str,
    table: str,
    rows: list[dict[str, Any]],
    pk_col: str,
    ctx: RunContext,
) -> None:
    if not rows:
        return
    certified_at = datetime.now(UTC).isoformat(sep=" ", timespec="microseconds")
    augmented = [
        {**row, "_run_id": ctx.run_id, "_source_cut": ctx.extract_cut,
         "_certified_at": certified_at}
        for row in rows
    ]
    columns = list(augmented[0].keys())
    col_sql = ", ".join(f"`{c}`" for c in columns)
    placeholders = ", ".join("%s" for _ in columns)
    update_sql = ", ".join(f"`{c}` = VALUES(`{c}`)" for c in columns if c != pk_col)
    stmt = (
        f"INSERT INTO `{schema}`.`{table}` ({col_sql}) VALUES ({placeholders}) "  # noqa: S608
        f"ON DUPLICATE KEY UPDATE {update_sql}"
    )
    cur = conn.cursor()
    for row in augmented:
        cur.execute(stmt, list(row.values()))
    conn.commit()
    cur.close()


def deduplicate(rows: list[dict[str, object]], key_fields: list[str]) -> list[dict[str, object]]:
    """Remove duplicate rows keeping the most recent by updated_at."""
    seen: dict[tuple[object, ...], dict[str, object]] = {}
    for row in rows:
        key = tuple(row[f] for f in key_fields)
        existing = seen.get(key)
        if existing is None or str(row.get("updated_at", "")) > str(existing.get("updated_at", "")):
            seen[key] = row
    return list(seen.values())


def harmonise_codelist(value: str, mapping: dict[str, str]) -> str:
    """Map a source code to the canonical Lake code. Returns value unchanged if not in mapping."""
    return mapping.get(value, value)
