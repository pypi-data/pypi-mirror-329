import logging.handlers
import sys

from multiprocessing import Queue
from pathlib import Path

from hylog import formatters


class QueueHandler(logging.handlers.QueueHandler):
    def __init__(self, queue: Queue) -> None:
        super().__init__(queue)


class QueueListener(logging.handlers.QueueListener):
    def __init__(self, queue,  *handlers: logging.Handler) -> None:
        super().__init__(queue, *handlers, respect_handler_level=True)


class FileLastRun(logging.FileHandler):
    _formatter: logging.Formatter = formatters.Detailed()
    _mode: str = "w"
    _level: int = logging.DEBUG

    def __init__(self, filename: str | Path) -> None:
        super().__init__(filename, mode=self._mode)
        self.setLevel(self._level)
        self.setFormatter(self._formatter)


class FileRotating(logging.handlers.RotatingFileHandler):
    _formatter: logging.Formatter = formatters.Detailed()
    _level: int = logging.DEBUG
    _max_bytes: int = 3_000_000
    _backup_count: int = 3

    def __init__(self, filename: str | Path) -> None:
        super().__init__(
            filename, maxBytes=self._max_bytes, backupCount=self._backup_count
        )

        self.setLevel(self._level)
        self.setFormatter(self._formatter)


class JSONHandler(logging.handlers.RotatingFileHandler):
    _formatter: logging.Formatter = formatters.JSON()
    _level: int = logging.DEBUG
    _max_bytes: int = 3_000_000
    _backup_count: int = 3

    def __init__(self, filename: str | Path) -> None:
        super().__init__(
            filename, maxBytes=self._max_bytes, backupCount=self._backup_count
        )
        self.setLevel(self._level)
        self.setFormatter(self._formatter)


class StandardOutput(logging.StreamHandler):
    _formatter: logging.Formatter = formatters.Simple()
    _level: int = logging.WARNING

    def __init__(self) -> None:
        super().__init__(stream=sys.stdout)
        self.setFormatter(self._formatter)
        self.setLevel(self._level)
