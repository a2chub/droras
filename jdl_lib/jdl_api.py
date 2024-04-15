import logging
import os
import pprint
import subprocess

from convert_heatlist import get_heat_list, load_heat_list
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from jdl_lib.race_manager import RaceManager

# directory structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
LOG_DIR = os.path.join(BASE_DIR, "log")

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# app main
app = FastAPI()
race_manager = RaceManager()


# API endpoints
@app.get("/api/start")
async def start():
    return await race_manager.start()


@app.get("/api/{heat_index}")
async def set_current_heat(heat_index: int = 1):
    return await race_manager.set_current_heat(heat_index)


@app.get("/api/reload-csv")
async def reload_csv():
    race_manager.load_heat()
    logger.info("CSV reload completed")
    return {"success": True}


@app.get("/api/download-csv")
async def download_csv():
    logger.info("CSV download started")
    get_heat_list()
    heat_list = load_heat_list()
    pprint.pprint(heat_list, indent=4)
    return {"success": True}


@app.get("/api/upload-log")
async def upload_log():
    logger.info("Starting log upload")
    try:
        script_path = os.path.join(BASE_DIR, "0_log_upload.sh")
        subprocess.call(script_path, shell=True)
    except:
        logger.error("Failed to upload log file")


# static files
@app.get("/")
@app.get("/{heat_index}")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


app.mount("/", StaticFiles(directory=STATIC_DIR), name="static")

race_manager.load_heat()
