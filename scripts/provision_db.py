"""
Provision the four Nexus MySQL schemas and audit tables.

Usage:
    python scripts/provision_db.py

Reads NEXUS_DB_* environment variables (same as the pipeline).
Runs sql/01_schemas.sql then sql/02_audit.sql in order.
Prints PASS / FAIL for each statement.
"""

import os
import re
import sys
from pathlib import Path

import mysql.connector

ROOT = Path(__file__).parent.parent
SQL_FILES = [ROOT / "sql" / "01_schemas.sql", ROOT / "sql" / "02_audit.sql"]


def _connect() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect(
        host=os.environ["NEXUS_DB_HOST"],
        port=int(os.environ.get("NEXUS_DB_PORT", "3306")),
        user=os.environ["NEXUS_DB_USER"],
        password=os.environ["NEXUS_DB_PASSWORD"],
    )


def _statements(sql: str) -> list[str]:
    return [s.strip() for s in re.split(r";\s*\n", sql) if s.strip()]


def main() -> int:
    try:
        conn = _connect()
    except Exception as exc:
        print(f"FAIL  connection: {exc}", file=sys.stderr)
        return 1

    cursor = conn.cursor()
    failures = 0

    for path in SQL_FILES:
        sql = path.read_text()
        for stmt in _statements(sql):
            label = stmt[:60].replace("\n", " ")
            try:
                cursor.execute(stmt)
                print(f"PASS  {label}")
            except Exception as exc:
                print(f"FAIL  {label}\n      {exc}", file=sys.stderr)
                failures += 1

    cursor.close()
    conn.close()
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
