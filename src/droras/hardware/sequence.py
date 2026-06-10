"""Start sequence: signal + audio playback with timing identical to legacy device.py."""

import logging
from random import randint
from time import sleep

from droras.hardware.base import AudioPlayer, StartSignal

logger = logging.getLogger(__name__)


def run_start_sequence(signal: StartSignal, audio: AudioPlayer) -> None:
    signal.on()
    audio.play("pipipi.wav")
    dur_time = float(randint(30, 50)) / 10.0
    sleep(dur_time)
    logger.info("Sound played for %s seconds", dur_time)
    audio.play("po-n.wav")
    sleep(0.35)
    signal.off()
