from dataclasses import dataclass
from typing import Any

import mysql.connector.abstracts


@dataclass
class ReconciliationResult:
    metric: str
    source_value: object
    target_value: object
    passed: bool
    tolerance: float = 0.0


def _fetch_scalar(cursor: Any) -> Any:
    row = cursor.fetchone()
    assert row is not None
    return row[0]


def reconcile_counts(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    source_schema: str,
    source_table: str,
    target_schema: str,
    target_table: str,
) -> ReconciliationResult:
    """Row-count reconciliation between two tables."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM `{source_schema}`.`{source_table}`")  # noqa: S608
    src = int(_fetch_scalar(cursor))
    cursor.execute(f"SELECT COUNT(*) FROM `{target_schema}`.`{target_table}`")  # noqa: S608
    tgt = int(_fetch_scalar(cursor))
    return ReconciliationResult(
        metric=f"row_count:{source_schema}.{source_table}→{target_schema}.{target_table}",
        source_value=src,
        target_value=tgt,
        passed=src == tgt,
    )


def reconcile_sum(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    source_schema: str,
    source_table: str,
    source_column: str,
    target_schema: str,
    target_table: str,
    target_column: str,
    tolerance: float = 0.0,
) -> ReconciliationResult:
    """Numeric sum reconciliation between a source and target column."""
    cursor = conn.cursor()
    sql_src = (
        f"SELECT COALESCE(SUM(`{source_column}`), 0) FROM `{source_schema}`.`{source_table}`"
    )
    cursor.execute(sql_src)  # noqa: S608
    src = float(_fetch_scalar(cursor))
    sql_tgt = (
        f"SELECT COALESCE(SUM(`{target_column}`), 0) FROM `{target_schema}`.`{target_table}`"
    )
    cursor.execute(sql_tgt)  # noqa: S608
    tgt = float(_fetch_scalar(cursor))
    diff = abs(src - tgt)
    return ReconciliationResult(
        metric=(
            f"sum:{source_schema}.{source_table}.{source_column}"
            f"→{target_schema}.{target_table}.{target_column}"
        ),
        source_value=src,
        target_value=tgt,
        passed=diff <= tolerance,
        tolerance=tolerance,
    )
