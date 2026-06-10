import asyncio
import logging

from google.cloud.firestore import AsyncClient

from . import event_logger
from .convert_heatlist import get_heat_pilots, load_heat_list
from .hardware.base import AudioPlayer, StartSignal
from .hardware.sequence import run_start_sequence

logger = logging.getLogger(__name__)


class RaceManager:
    def __init__(self, start_signal: StartSignal, audio_player: AudioPlayer):
        self.current_heat_index = 1
        self.all_heat_list = []
        self.race_ref = self.connect_to_firestore()
        self._start_signal = start_signal
        self._audio_player = audio_player
        self._sequence_running = False

    def connect_to_firestore(self):
        try:
            db = AsyncClient()
            logger.info("Successfully connected to Firestore")
            return db.collection("race").document("current")
        except Exception:
            logger.error("Failed to connect to Firestore", exc_info=True)
            return None

    def load_heat(self):
        self.all_heat_list = []
        try:
            self.all_heat_list = load_heat_list()
            logger.info("Successfully loaded heat list")
        except Exception:
            logger.error("Failed to load heat list", exc_info=True)

    # リレーの制御とスター音を鳴らす
    async def start(self):
        if self._sequence_running:
            logger.warning("Start sequence already running; ignoring new start request")
            return {"status": 200}

        self._sequence_running = True
        try:
            await asyncio.to_thread(
                run_start_sequence, self._start_signal, self._audio_player
            )
        finally:
            self._sequence_running = False

        # シーケンス完了後にログ記録 (CSV タイムスタンプ = スタート音発火後の実時刻)
        current_pilots = ""
        try:
            current_pilots = get_heat_pilots(self.current_heat_index, self.all_heat_list)
            logger.info(str(current_pilots))
        except Exception:
            logger.error("Failed to get heat pilots", exc_info=True)
            event_logger.log_heat_error(self.current_heat_index, current_pilots)
        event_logger.log_heat_start(self.current_heat_index, current_pilots)
        return {"status": 200}

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

    def get_current_pilots(self):
        current_pilots_csv = get_heat_pilots(self.current_heat_index, self.all_heat_list)
        current_pilots_array = current_pilots_csv.split(",")
        return current_pilots_array
