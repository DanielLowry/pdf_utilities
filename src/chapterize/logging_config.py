"""
logging_config.py — Shared logging setup for chapterize.

Expose helpers to wire up logging via environment variables so debug output can be captured
during interactive runs without changing the CLI behavior.
"""
import logging
import os
import sys

DEFAULT_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging() -> logging.Logger:
    """
    Configure the root logger based on `CHAPTERIZE_LOG_LEVEL` and optional `CHAPTERIZE_LOG_FILE`.
    Returns a logger named `chapterize` for downstream use.
    """
    root = logging.getLogger()
    level_name = os.getenv("CHAPTERIZE_LOG_LEVEL", DEFAULT_LEVEL).upper()
    level = getattr(logging, level_name, logging.WARNING)
    log_file = os.getenv("CHAPTERIZE_LOG_FILE")
    handler = logging.FileHandler(log_file) if log_file else logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(handler)
    return logging.getLogger("chapterize")
