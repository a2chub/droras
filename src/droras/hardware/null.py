"""Null implementations of StartSignal and AudioPlayer for non-GPIO/non-audio environments."""

import logging

logger = logging.getLogger(__name__)


class NullStartSignal:
    def on(self) -> None:
        logger.info("NullStartSignal: on")

    def off(self) -> None:
        logger.info("NullStartSignal: off")


class NullAudioPlayer:
    def play(self, sound_name: str) -> None:
        logger.info("NullAudioPlayer: play %s", sound_name)
