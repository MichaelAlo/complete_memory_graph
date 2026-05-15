from collections.abc import Generator
from contextlib import contextmanager
from typing import cast

import mysql.connector
import mysql.connector.abstracts

from src.config.settings import Config


@contextmanager
def get_connection(
    cfg: Config,
) -> Generator[mysql.connector.abstracts.MySQLConnectionAbstract, None, None]:
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
    try:
        yield conn
    finally:
        conn.close()
