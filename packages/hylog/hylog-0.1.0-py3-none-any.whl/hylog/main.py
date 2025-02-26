import atexit
import logging.config
import logging.handlers

from multiprocessing import Queue
from pathlib import Path

from hylog import handlers


def _close_logger(logger_name: str) -> None:
    logger = logging.getLogger(logger_name)
    logger.debug(f"Logging Complete...{'\n' * 2}")


def _setup_handlers(
    output_dir: Path, name: str, stdout_level: str | None = None
) -> None:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = handlers.StandardOutput()
    if stdout_level:
        stream_handler.setLevel(getattr(logging, stdout_level.upper()))
    file_last_handler = handlers.FileLastRun(output_dir / f"{name}_last.log")
    file_rotating_handler = handlers.FileRotating(output_dir / f"{name}_rotating.log")
    json_handler = handlers.JSONHandler(output_dir / f"{name}_json.jsonl")

    log_queue = Queue(-1)
    queue_handler = handlers.QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    queue_listener = handlers.QueueListener(
        log_queue,
        *[stream_handler, file_last_handler, file_rotating_handler, json_handler],
    )
    queue_listener.start()
    atexit.register(queue_listener.stop)
    atexit.register(_close_logger, name)

    logger.debug("Logging Started...")


def get_app_logger(
    name: str,
    output_dir: str | Path,
    stdout_level: str | None = None,
) -> logging.Logger:
    _setup_handlers(Path(output_dir), name, stdout_level)

    return logging.getLogger(name)
