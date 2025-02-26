from pathlib import Path

from hylog import get_app_logger


log = get_app_logger("app", Path(__file__).parent / "logs")

if __name__ == "__main__":
    log.debug("DEBUG message")
    log.debug("DEBUG message with extra", extra={"extra_key": "extra_value"})
    log.info("INFO message")
    log.warning("WARNING message")
    log.error("ERROR message")
    log.critical("CRITICAL message")

    log.info(Path().cwd())
    log.info(Path().home())

    try:
        1 / 0

    except ZeroDivisionError as e:
        log.exception("Exception occurred", exc_info=e)
