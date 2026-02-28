import logging
from typing import Tuple

import psycopg

from app.core.config import settings

logger = logging.getLogger(__name__)


def check_db_connection(timeout_seconds: int = 2) -> Tuple[bool, str]:
    """
    Tries to connect and run `SELECT 1`.
    Returns (ok, detail_message).
    """
    try:
        conninfo = settings.database_url
        with psycopg.connect(conninfo, connect_timeout=timeout_seconds) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                _ = cur.fetchone()
        return True, "ok"
    except Exception as e:
        logger.warning("DB health check failed: %s", e)
        return False, str(e)