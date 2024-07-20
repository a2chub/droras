import logging
import os
import pprint
import subprocess

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from . import config
from . import convert_heatlist
from .race_manager import RaceManager

logger = logging.getLogger(__name__)

# app main
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(socketio_server=sio, static_files={"/": config.STATIC_DIR})
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

race_manager = RaceManager()


# SocketIO events
@sio.event
async def connect(sid, environ, auth):
    logger.info(f"Connected: {sid}")
    await sio.emit("heat_list", race_manager.all_heat_list[1:], room=sid)
    await sio.emit("current_heat", race_manager.current_heat_index, room=sid)


@sio.event
def disconnect(sid):
    logger.info(f"Disconnect: {sid}")


@sio.event
def start_heat(sid):
    logger.info(f"Start heat: {sid}")
    race_manager.start()


@sio.event
async def set_current_heat(sid, data):
    heat_index = int(data)
    logger.info(f"Set current heat: {heat_index}")
    race_manager.set_current_heat(heat_index)
    await sio.emit("current_heat", heat_index)


@sio.event
async def reload_heat_list(sid, data):
    race_manager.load_heat()
    logger.info("Heat list reloaded")
    await sio.emit("heat_list", race_manager.all_heat_list[1:])
    return True


@sio.event
async def download_heat_list(sid, data):
    logger.info("Heat list download started")
    heat_list = convert_heatlist.download_heat_list()
    logger.info(f"Heat list download completed: {pprint.pformat(heat_list)}")
    await sio.emit("heat_list", race_manager.all_heat_list[1:])
    return True


@sio.event
def upload_log(sid, data):
    logger.info("Starting log upload")
    try:
        script_path = os.path.join(config.BASE_DIR, "0_log_upload.sh")
        subprocess.call(script_path, shell=True)
        return True
    except:
        logger.error("Failed to upload log file")
        return False


# static files
@app.get("/")
def index():
    return FileResponse(os.path.join(config.STATIC_DIR, "index.html"))


@app.get("/current_pilots")
async def current_pilots():
    return race_manager.get_current_pilots()


@app.get("/{heat_index}")
async def index(heat_index: int):
    race_manager.set_current_heat(heat_index)
    return FileResponse(os.path.join(config.STATIC_DIR, "index.html"))


app.mount("/", sio_app)


race_manager.load_heat()
