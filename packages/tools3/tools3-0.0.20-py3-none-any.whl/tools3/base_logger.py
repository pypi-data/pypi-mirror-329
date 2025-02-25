"""Module for configuring and managing logging functionality.

This module provides a flexible logging configuration utility that supports
file-based and stream-based logging with customizable formatting.
"""

import logging
import os
from typing import Optional
import inspect
import json
from loguru import logger
from typing import Optional, Union



class BaseLogger:
    """A class to manage different types of logging configurations.

    This class provides methods to configure and manage different types of loggers,
    including null logger, file logger, and stream logger.

    Attributes:
        _logger: The configured logging.Logger instance.
    """
    _logger: logger = None

    def __init__(self):
        """Initializes the BaseLogger with no logger configured."""
    def get_logger(self) -> logger:
        """Returns the current logger instance.

        If no logger is configured, initializes and returns a null logger.

        Returns:
            logging.Logger: The configured logger instance.
        """
        if self._logger is None:
            # self.configure_null_logger()
            self.configure_file_logger("tool3-cli.json")
        return self._logger

    def set_logger(self, log: logger) -> 'BaseLogger':
        """Sets the logger instance.

        Args:
            log: The logger instance to be used (can be either standard logging.Logger or loguru.logger).

        Returns:
            BaseLogger: The current BaseLogger instance for method chaining.
        """
        self._logger = log
        return self

    def configure_null_logger(self) -> 'BaseLogger':
        """Configures a null logger that discards all log messages.

        Returns:
            BaseLogger: The current BaseLogger instance for method chaining.
        """
        null_logger = logging.getLogger('null_logger')
        null_logger.addHandler(logging.NullHandler())
        self.set_logger(null_logger)
        return self

    def configure_file_logger(
        self,
        log_file_path: str,
        log_level: int = logging.DEBUG
    ) -> 'BaseLogger':
        """Configures a file-based logger.

        Args:
            log_file_path: The path where log files will be written.
            log_level: The logging level to use. Defaults to DEBUG.

        Returns:
            BaseLogger: The current BaseLogger instance for method chaining.
        """
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logger.remove()
        logger.add(
            log_file_path,
            level="DEBUG",
            rotation="10 MB",
            encoding="utf-8",
            serialize=True,
        )
        # 移除默认的 logger
        self.set_logger(logger)
        return self

    def configure_stream_logger(
        self,
        log_level: int = logging.DEBUG
    ) -> 'BaseLogger':
        """Configures a console-based stream logger.

        Args:
            log_level: The logging level to use. Defaults to DEBUG.

        Returns:
            BaseLogger: The current BaseLogger instance for method chaining.
        """
        # Configure stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)

        # Configure formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s.%(funcName)s - %(message)s'
        )
        stream_handler.setFormatter(formatter)

        # Configure logger
        stream_logger = logging.getLogger('stream_logger')
        stream_logger.setLevel(logging.DEBUG)
        stream_logger.addHandler(stream_handler)

        self.set_logger(stream_logger)
        return self