import logging
import os

from . import config

if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(os.path.join(config.LOG_DIR, "app.log")), logging.StreamHandler()],
)
