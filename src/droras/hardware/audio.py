"""Pygame implementation of AudioPlayer."""

import logging
import os

from droras import config

logger = logging.getLogger(__name__)


class PygameAudioPlayer:
    def __init__(self) -> None:
        import pygame  # delayed import to avoid pygame init at module load
        pygame.init()
        pygame.mixer.init()
        self._pygame = pygame
        self._sounds: dict = {}  # cache per sound name; also prevents GC stopping playback

    def play(self, sound_name: str) -> None:
        snd = self._sounds.get(sound_name)
        if snd is None:
            path = os.path.join(config.SOUND_DIR, sound_name)
            snd = self._pygame.mixer.Sound(path)
            self._sounds[sound_name] = snd
        snd.play()
