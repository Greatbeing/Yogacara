"""
Yogacara Logger Module

Provides structured logging capabilities for the Yogacara framework.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class YogacaraLogger:
    """
    Structured logger for Yogacara framework.
    
    Features:
    - Configurable log levels
    - File and console output
    - Structured formatting
    - Rotation support
    """
    
    DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    def __init__(
        self,
        name: str = "yogacara",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        console: bool = True,
    ) -> None:
        """
        Initialize Yogacara logger.
        
        Args:
            name: Logger name
            level: Logging level
            log_file: Optional file path for log output
            console: Whether to output to console
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers = []
        
        formatter = logging.Formatter(self.DEFAULT_FORMAT, self.DATE_FORMAT)
        
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)
    
    def seed_planted(self, seed_id: str, seed_type: str) -> None:
        """Log seed planting event."""
        self.info(f"Seed planted: {seed_id} (type={seed_type})")
    
    def seed_activated(self, seed_id: str, vasana: int) -> None:
        """Log seed activation event."""
        self.debug(f"Seed activated: {seed_id} (vasana={vasana})")
    
    def emergence_detected(self, emergence_type: str, strength: float) -> None:
        """Log emergence detection event."""
        self.info(
            f"Emergence detected: {emergence_type} (strength={strength:.2f})"
        )
    
    def level_up(self, old_level: str, new_level: str) -> None:
        """Log awakening level up event."""
        self.info(f"Level up: {old_level} → {new_level}")
    
    def exception(self, message: str) -> None:
        """Log exception with traceback."""
        self.logger.exception(message)


# Default logger instance
_default_logger: Optional[YogacaraLogger] = None


def get_logger(
    name: str = "yogacara",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True,
) -> YogacaraLogger:
    """
    Get or create the default logger instance.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional file path
        console: Whether to output to console
        
    Returns:
        YogacaraLogger instance
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = YogacaraLogger(
            name=name,
            level=level,
            log_file=log_file,
            console=console,
        )
    return _default_logger


def configure_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: Optional[str] = None,
) -> YogacaraLogger:
    """
    Configure logging with string level.
    
    Args:
        level: Log level as string (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file name (will be placed in log_dir if specified)
        log_dir: Optional log directory
        
    Returns:
        Configured YogacaraLogger instance
    """
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = level_map.get(level.upper(), logging.INFO)
    
    if log_dir and log_file:
        log_path = str(Path(log_dir) / log_file)
    elif log_file:
        log_path = log_file
    else:
        log_path = None
    
    return get_logger(level=log_level, log_file=log_path)
