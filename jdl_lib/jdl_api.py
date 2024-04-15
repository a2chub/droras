import os
import pprint
import subprocess

from convert_heatlist import get_heat_list, get_heat_pilots, load_heat_list
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from starlette.responses import FileResponse
from start_log import logger

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
    print("connected firestore complete")
except:
    print(" no firestore")
    db = ""
    pass


def load_heat():
    global all_heat_list
    try:
        all_heat_list = load_heat_list()
        logger.info(f"load csv heat list")
    except:
        print("no load heat list")
        all_heat_list = []


# リレーの制御とスター音を鳴らす
@app.get("/api/start")
async def start():
    global CURRENT_HEAT_INDEX, all_heat_list
    await count_down()
    try:
        current_pilots = get_heat_pilots(CURRENT_HEAT_INDEX, all_heat_list)
        print(current_pilots)
    except:
        logger.err(f"{CURRENT_HEAT_INDEX},firebase_send_error,{current_pilots}")
    logger.info(f"{CURRENT_HEAT_INDEX},start_heat,{current_pilots}")
    return {"status": 200}


async def count_down():
    import platform

    if platform.system() != "Darwin":
        from webapp import start_sound

        start_sound()


@app.get("/api/{heat_index}")
async def set_current(heat_index: int = 1):
    global CURRENT_HEAT_INDEX, all_heat_list
    CURRENT_HEAT_INDEX = heat_index
    current_pilots = get_heat_pilots(CURRENT_HEAT_INDEX, all_heat_list)
    print(current_pilots)
    logger.info(f"{CURRENT_HEAT_INDEX},change_heat,{current_pilots}")
    try:
        print("call set_cur_heat_fb")
        await set_cur_heat_fb(str(heat_index))
    except:
        print("no send firestore")
    return {"heat_id": heat_index}


async def set_cur_heat_fb(heat_id=1):
    print("send firebase")
    race_ref.set({"heat": "%s" % (heat_id)})


@app.get("/csv_reload")
async def reload_csv():
    load_heat()
    print("CSVファイルの再読み込みが完了しました")
    return {"success": True}


@app.get("/csv_download")
async def reload_csv():
    print("CSVダウンロードが開始しました")
    logger.info(f"Download csv file")
    get_heat_list()
    h_list = load_heat_list()
    pprint.pprint(h_list, indent=4)
    return {"success": True}


@app.get("/log_upload")
async def log_upload():
    print("logファイルのアップロード開始")
    logger.info(f"Upload Log file")
    _script_path = "../0_log_upload.sh"
    try:
        subprocess.call(_script_path, shell=True)
    except:
        print("file upload fail")


@app.get("/")
@app.get("/{heat_index}")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


app.mount("/", StaticFiles(directory=STATIC_DIR), name="static")

load_heat()
