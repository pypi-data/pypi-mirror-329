# MIT License
#
# Copyright (c) 2025 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import logging


class Logger:
    """Custom logger class with configurable handlers."""

    loggers = {}

    def __init__(self):
        """Initialize logger with environment-based configuration."""
        self.log_level = os.environ.get("APP_LOGGING_LEVEL", "info").upper()
        self.log_handlers = (
            os.environ.get("APP_LOGGING_HANDLERS", "console").lower().split(",")
        )

    def get_logger(self, name=__name__):
        """Get or create a logger instance.

        Args:
            name (str): Logger name (default: calling module's name).

        Returns:
            logging.Logger: Configured logger instance.
        """
        if name not in self.loggers:
            logger = logging.getLogger(name)
            logger.setLevel(self._get_log_level())
            if not logger.handlers:
                self._setup_handlers(logger)
            self.loggers[name] = logger
        return self.loggers[name]

    def _get_log_level(self):
        """Get logging level from environment or default to INFO."""
        return getattr(logging, self.log_level, logging.INFO)

    def _setup_handlers(self, logger):
        """Set up logging handlers based on configuration."""
        if "console" in self.log_handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            logger.addHandler(console_handler)


def get_logger() -> Logger:
    """Create and return a logger instance for the calling module.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return Logger().get_logger(__name__)
