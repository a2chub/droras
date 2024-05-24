import logging
import os
from logging.handlers import TimedRotatingFileHandler
import re

from . import config

logger = logging.getLogger("heatStartLog")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    os.path.join(config.LOG_DIR, "heat_start.csv"), when="MIDNIGHT", interval=1, backupCount=100
)
handler.namer = lambda x: re.sub(r"\.([^.]+)\.(\d{4})-(\d{2})-(\d{2})$", r"_\2-\3-\4.\1", x)

format = logging.Formatter("%(asctime)s,%(message)s", datefmt="%Y/%m/%d,%H:%M:%S")
handler.setFormatter(format)

logger.addHandler(handler)


def log_heat_start(heat_index, pilots):
    logger.info(f"{heat_index},start_heat,{pilots}")


def log_heat_change(heat_index, pilots):
    logger.info(f"{heat_index},change_heat,{pilots}")


def log_heat_error(heat_index, pilots):
    logger.error(f"{heat_index},firebase_send_error,{pilots}")
