"""
logging_config.py — Shared logging setup for chapterize.

Expose helpers to wire up logging via environment variables so debug output can be captured
during interactive runs without changing the CLI behavior.
"""
import logging
import os
import sys

DEFAULT_LEVEL = "WARNING"
DEFAULT_LOG_FILE = "chapterize.log"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


class ChapterizeFilter(logging.Filter):
    """Allow only records from the `chapterize` namespace to pass through."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith("chapterize")


def configure_logging() -> logging.Logger:
    """
    Configure logging for chapterize and write to a file.
    Third-party loggers are kept at WARNING level by the root logger to avoid noise.
    """
    root = logging.getLogger()
    level_name = os.getenv("CHAPTERIZE_LOG_LEVEL", DEFAULT_LEVEL).upper()
    chapterize_level = getattr(logging, level_name, logging.INFO)
    log_file = os.getenv("CHAPTERIZE_LOG_FILE", DEFAULT_LOG_FILE)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler.addFilter(ChapterizeFilter())
    root.handlers.clear()
    root.setLevel(logging.WARNING)
    root.addHandler(handler)
    chapterize_logger = logging.getLogger("chapterize")
    chapterize_logger.setLevel(chapterize_level)
    return chapterize_logger
