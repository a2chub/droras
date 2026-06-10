"""Manual test entry point: python -m droras.hardware"""

import logging

from droras.hardware import create_audio_player, create_start_signal
from droras.hardware.sequence import run_start_sequence

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    signal = create_start_signal()
    audio = create_audio_player()
    run_start_sequence(signal, audio)
