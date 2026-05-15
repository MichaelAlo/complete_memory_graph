from dataclasses import dataclass
from typing import Any

import mysql.connector.abstracts


@dataclass
class QualityResult:
    check: str
    passed: bool
    detail: str | None = None


def _fetch_int(cursor: Any) -> int:
    row = cursor.fetchone()
    assert row is not None
    return int(row[0])


def check_row_count(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    schema: str,
    table: str,
    min_rows: int = 1,
) -> QualityResult:
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM `{schema}`.`{table}`")  # noqa: S608
    count = _fetch_int(cursor)
    return QualityResult(
        check=f"row_count:{schema}.{table}",
        passed=count >= min_rows,
        detail=f"{count} rows (min={min_rows})",
    )


def check_nulls(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    schema: str,
    table: str,
    column: str,
) -> QualityResult:
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM `{schema}`.`{table}` WHERE `{column}` IS NULL")  # noqa: S608
    count = _fetch_int(cursor)
    return QualityResult(
        check=f"nulls:{schema}.{table}.{column}",
        passed=count == 0,
        detail=f"{count} null values" if count else None,
    )


def check_uniqueness(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    schema: str,
    table: str,
    key_columns: list[str],
) -> QualityResult:
    cols = ", ".join(f"`{c}`" for c in key_columns)
    cursor = conn.cursor()
    cursor.execute(  # noqa: S608
        f"SELECT COUNT(*) FROM (SELECT {cols}, COUNT(*) AS n FROM `{schema}`.`{table}` "
        f"GROUP BY {cols} HAVING n > 1) dupes"
    )
    dup_count = _fetch_int(cursor)
    return QualityResult(
        check=f"uniqueness:{schema}.{table}({','.join(key_columns)})",
        passed=dup_count == 0,
        detail=f"{dup_count} duplicate key combinations" if dup_count else None,
    )


def run_all(checks: list[QualityResult]) -> bool:
    """Return True only if every check passed."""
    return all(c.passed for c in checks)
