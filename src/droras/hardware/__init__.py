"""Hardware abstraction layer: factory functions for StartSignal and AudioPlayer."""

import logging
import os

from droras.hardware.base import AudioPlayer, StartSignal

logger = logging.getLogger(__name__)


def create_start_signal() -> StartSignal:
    """Return a StartSignal implementation selected by DRORAS_GPIO env var."""
    mode = os.environ.get("DRORAS_GPIO", "auto")

    if mode == "off":
        from droras.hardware.null import NullStartSignal
        return NullStartSignal()

    if mode == "on":
        from droras.hardware.gpio import GpioStartSignal
        return GpioStartSignal()

    if mode == "mock":
        os.environ["GPIOZERO_PIN_FACTORY"] = "mock"
        from droras.hardware.gpio import GpioStartSignal
        return GpioStartSignal()

    # "auto" or unrecognised value
    if mode not in ("auto",):
        logger.warning("Unknown DRORAS_GPIO value %r; falling back to auto", mode)

    try:
        from droras.hardware.gpio import GpioStartSignal
        return GpioStartSignal()
    except Exception as exc:
        logger.warning("GPIO unavailable, falling back to NullStartSignal: %s", exc)
        from droras.hardware.null import NullStartSignal
        return NullStartSignal()


def create_audio_player() -> AudioPlayer:
    """Return an AudioPlayer implementation, falling back to Null if pygame init fails."""
    try:
        from droras.hardware.audio import PygameAudioPlayer
        return PygameAudioPlayer()
    except Exception as exc:
        logger.warning("Audio unavailable, falling back to NullAudioPlayer: %s", exc)
        from droras.hardware.null import NullAudioPlayer
        return NullAudioPlayer()
