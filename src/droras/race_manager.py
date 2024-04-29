import asyncio
import logging

from google.cloud.firestore import AsyncClient

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
            db = AsyncClient()
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
    def start(self):
        self.count_down()
        try:
            current_pilots = get_heat_pilots(self.current_heat_index, self.all_heat_list)
            logger.info(str(current_pilots))
        except:
            event_logger.log_heat_error(self.current_heat_index, current_pilots)
        event_logger.log_heat_start(self.current_heat_index, current_pilots)
        return {"status": 200}

    def count_down(self):
        import platform

        if platform.system() != "Darwin":
            from .device import start_sound

            start_sound()

    def set_current_heat(self, heat_index):
        self.current_heat_index = heat_index
        current_pilots = get_heat_pilots(self.current_heat_index, self.all_heat_list)
        logger.debug(str(current_pilots))
        event_logger.log_heat_change(self.current_heat_index, current_pilots)
        asyncio.create_task(self.update_current_heat_on_firestore(str(heat_index)))
        return {"heat_id": heat_index}

    async def update_current_heat_on_firestore(self, heat_id):
        try:
            await self.race_ref.set({"heat": heat_id})
            logger.info(f"Heat {heat_id} successfully updated on Firestore")
        except Exception as e:
            logger.error(f"Failed to update heat {heat_id} on Firestore: {e}")
