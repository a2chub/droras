
import logging
from logging.handlers import TimedRotatingFileHandler  # この行を追加

logger = logging.getLogger("heatStartLog")
logger.setLevel( logging.INFO )

handler = logging.handlers.TimedRotatingFileHandler("./log/heat_start.csv", when="MIDNIGHT", interval=1, backupCount=100)

logger.addHandler(handler)

fmt = logging.Formatter('%(asctime)s,%(message)s', datefmt="%Y/%m/%d,%H:%M:%S")
handler.setFormatter(fmt)

