from datetime import UTC, datetime

import mysql.connector.abstracts

from src.lib.run_context import RunContext

_INSERT = """
INSERT INTO nexus_raw.job_runs
    (run_id, job_name, source_cut, release_tag, started_at)
VALUES
    (%(run_id)s, %(job_name)s, %(source_cut)s, %(release_tag)s, %(started_at)s)
ON DUPLICATE KEY UPDATE started_at = VALUES(started_at)
"""

_UPDATE = """
UPDATE nexus_raw.job_runs
SET completed_at      = %(completed_at)s,
    row_count_in      = %(row_count_in)s,
    row_count_out     = %(row_count_out)s,
    validation_result = %(validation_result)s,
    error_detail      = %(error_detail)s
WHERE run_id = %(run_id)s
"""


def log_run_start(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    ctx: RunContext,
    job_name: str,
) -> None:
    cur = conn.cursor()
    cur.execute(
        _INSERT,
        {
            "run_id": ctx.run_id,
            "job_name": job_name,
            "source_cut": ctx.extract_cut or "",
            "release_tag": ctx.release_tag,
            "started_at": ctx.started_at,
        },
    )
    conn.commit()
    cur.close()


def log_run_complete(
    conn: mysql.connector.abstracts.MySQLConnectionAbstract,
    ctx: RunContext,
    row_count_in: int,
    row_count_out: int,
    result: str,
    error: str | None = None,
) -> None:
    cur = conn.cursor()
    cur.execute(
        _UPDATE,
        {
            "run_id": ctx.run_id,
            "completed_at": datetime.now(UTC),
            "row_count_in": row_count_in,
            "row_count_out": row_count_out,
            "validation_result": result,
            "error_detail": error,
        },
    )
    conn.commit()
    cur.close()
