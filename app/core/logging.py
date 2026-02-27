import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """
    Minimal, production-friendly logging:
    - single formatter
    - stdout output (container best practice)
    - level controlled via env (APP_LOG_LEVEL)
    """
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(level)

    # Remove any existing handlers to avoid duplicates in reload environments
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)