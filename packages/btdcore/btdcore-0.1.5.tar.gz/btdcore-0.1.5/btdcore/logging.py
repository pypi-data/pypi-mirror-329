import logging
import os


def setup_logging():
    LOG_FMT = (
        f"%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s"
    )

    logging.basicConfig(
        level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")),
        format=LOG_FMT,
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    return
