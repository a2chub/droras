import logging
import os
import pprint
import subprocess

import socketio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from . import config
from .convert_heatlist import get_heat_list, load_heat_list
from .race_manager import RaceManager

logger = logging.getLogger(__name__)

# app main
origins = ["*", "http://localhost:5173", "http://localhost:8000"]
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
sio_app = socketio.ASGIApp(socketio_server=sio, static_files={"/": config.STATIC_DIR})
app = FastAPI()

race_manager = RaceManager()


# API endpoints
@app.get("/api/start")
def start():
    return race_manager.start()


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
        script_path = os.path.join(config.BASE_DIR, "0_log_upload.sh")
        subprocess.call(script_path, shell=True)
    except:
        logger.error("Failed to upload log file")


# SocketIO events
@sio.event
async def connect(sid, environ, auth):
    logger.info(f"Connected: {sid}")
    await sio.emit("heat_list", race_manager.all_heat_list[1:], room=sid)
    await sio.emit("current_heat", race_manager.current_heat_index, room=sid)


@sio.event
def disconnect(sid):
    logger.info(f"Disconnect: {sid}")


@sio.on("start_heat")
def start_heat_socket(sid):
    logger.info(f"Start heat: {sid}")
    race_manager.start()


@sio.on("set_current_heat")
async def set_current_heat_socket(sid, data):
    heat_index = int(data)
    logger.info(f"Set current heat: {heat_index}")
    await race_manager.set_current_heat(heat_index)
    await sio.emit("current_heat", heat_index)


# static files
@app.get("/")
def index():
    return FileResponse(os.path.join(config.STATIC_DIR, "index.html"))


@app.get("/telop/")
def index():
    return FileResponse(os.path.join(config.STATIC_DIR, "telop", "index.html"))


@app.get("/{heat_index}")
async def index(heat_index: int):
    await race_manager.set_current_heat(heat_index)
    return FileResponse(os.path.join(config.STATIC_DIR, "index.html"))


app.mount("/", sio_app)


race_manager.load_heat()
