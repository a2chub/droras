import os
import pprint
import subprocess
import logging

from convert_heatlist import get_heat_list, get_heat_pilots, load_heat_list
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from starlette.responses import FileResponse
import jdl_lib.event_logger as event_logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


current_script_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_script_path)
BASE_DIR = os.path.dirname(current_dir_path)
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI()
CURRENT_HEAT_INDEX = 1
all_heat_list = []

try:
    db = firestore.Client()
    race_ref = db.collection("race").document("current")
    logger.info("Successfully connected to Firestore")
except:
    logger.error("Failed to connect to Firestore")
    db = ""
    pass


def load_heat():
    global all_heat_list
    try:
        all_heat_list = load_heat_list()
        logger.info("Successfully loaded heat list")
    except:
        logger.error("Failed to load heat list")
        all_heat_list = []


# リレーの制御とスター音を鳴らす
@app.get("/api/start")
async def start():
    global CURRENT_HEAT_INDEX, all_heat_list
    await count_down()
    try:
        current_pilots = get_heat_pilots(CURRENT_HEAT_INDEX, all_heat_list)
        logger.info(str(current_pilots))
    except:
        event_logger.log_heat_error(CURRENT_HEAT_INDEX, current_pilots)
    event_logger.log_heat_start(CURRENT_HEAT_INDEX, current_pilots)
    return {"status": 200}


async def count_down():
    import platform

    if platform.system() != "Darwin":
        from webapp import start_sound

        start_sound()


@app.get("/api/{heat_index}")
async def set_current_heat(heat_index: int = 1):
    global CURRENT_HEAT_INDEX, all_heat_list
    CURRENT_HEAT_INDEX = heat_index
    current_pilots = get_heat_pilots(CURRENT_HEAT_INDEX, all_heat_list)
    logger.info(str(current_pilots))
    event_logger.log_heat_change(CURRENT_HEAT_INDEX, current_pilots)
    try:
        logger.info("Calling set_cur_heat_fb")
        await set_current_heat_on_firestore(str(heat_index))
    except:
        logger.error("Failed to send to Firestore")
    return {"heat_id": heat_index}


async def set_current_heat_on_firestore(heat_id: int = 1):
    logger.info("Sending to Firestore")
    race_ref.set({"heat": str(heat_id)})


@app.get("/reload-csv")
async def reload_csv():
    load_heat()
    logger.info("CSV reload completed")
    return {"success": True}


@app.get("/download-csv")
async def download_csv():
    logger.info("CSV download started")
    get_heat_list()
    heat_list = load_heat_list()
    pprint.pprint(heat_list, indent=4)
    return {"success": True}


@app.get("/upload-log")
async def upload_log():
    logger.info("Starting log upload")
    try:
        subprocess.call("../0_log_upload.sh", shell=True)
    except:
        logger.error("Failed to upload log file")


@app.get("/")
@app.get("/{heat_index}")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


app.mount("/", StaticFiles(directory=STATIC_DIR), name="static")

load_heat()
