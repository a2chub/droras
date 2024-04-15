import logging

from google.cloud import firestore

from . import event_logger
from .convert_heatlist import get_heat_pilots, load_heat_list

logger = logging.getLogger(__name__)


class RaceManager:
    def __init__(self):
        self.current_heat_index = 1
        self.all_heat_list = []
        self.race_ref = self.connect_to_firestore()

    def connect_to_firestore(self):
        try:
            db = firestore.Client()
            logger.info("Successfully connected to Firestore")
            return db.collection("race").document("current")
        except:
            logger.error("Failed to connect to Firestore")
            return None

    def load_heat(self):
        self.all_heat_list = []
        try:
            self.all_heat_list = load_heat_list()
            logger.info("Successfully loaded heat list")
        except:
            logger.error("Failed to load heat list")

    # リレーの制御とスター音を鳴らす
    async def start(self):
        await self.count_down()
        try:
            current_pilots = get_heat_pilots(self.current_heat_index, self.all_heat_list)
            logger.info(str(current_pilots))
        except:
            event_logger.log_heat_error(self.current_heat_index, current_pilots)
        event_logger.log_heat_start(self.current_heat_index, current_pilots)
        return {"status": 200}

    async def count_down():
        import platform

        if platform.system() != "Darwin":
            from device import start_sound

            start_sound()

    async def set_current_heat(self, heat_index):
        self.current_heat_index = heat_index
        current_pilots = get_heat_pilots(self.current_heat_index, self.all_heat_list)
        logger.info(str(current_pilots))
        event_logger.log_heat_change(self.current_heat_index, current_pilots)
        try:
            logger.info("Calling set_cur_heat_fb")
            await self.set_current_heat_on_firestore(str(heat_index))
        except:
            logger.error("Failed to send to Firestore")
        return {"heat_id": heat_index}

    async def set_current_heat_on_firestore(self, heat_id):
        logger.info("Sending to Firestore")
        self.race_ref.set({"heat": str(heat_id)})
