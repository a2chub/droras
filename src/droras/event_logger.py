import logging
import os
from logging.handlers import TimedRotatingFileHandler

from . import config

logger = logging.getLogger("heatStartLog")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    os.path.join(config.LOG_DIR, "heat_start.csv"), when="MIDNIGHT", interval=1, backupCount=100
)

logger.addHandler(handler)

format = logging.Formatter("%(asctime)s,%(message)s", datefmt="%Y/%m/%d,%H:%M:%S")
handler.setFormatter(format)


def log_heat_start(heat_index, pilots):
    logger.info(f"{heat_index},start_heat,{pilots}")


def log_heat_change(heat_index, pilots):
    logger.info(f"{heat_index},change_heat,{pilots}")


def log_heat_error(heat_index, pilots):
    logger.error(f"{heat_index},firebase_send_error,{pilots}")
