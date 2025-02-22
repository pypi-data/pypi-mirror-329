import logging
import os
import sys
import json
from logging.handlers import RotatingFileHandler

# Define log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def setup_logger(log_name="bcsd", log_level="INFO", log_dir="logs"):
    """
    Set up structured logging with JSON formatting.

    Args:
        log_name (str): Name of the log file.
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_dir (str): Directory to store log files.

    Returns:
        logging.Logger: Configured logger instance.
    """

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{log_name}.log")

    # Configure root logger
    logger = logging.getLogger(log_name)
    logger.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))

    # JSON formatter for structured logging
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
                "level": record.levelname,
                "module": record.module,
                "message": record.getMessage()
            }
            if record.exc_info:
                log_record["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_record)

    formatter = JSONFormatter()

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Console handler for debugging
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger