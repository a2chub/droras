"""Tests for hardware factory (hardware-abstraction spec)."""

import asyncio
import logging
import os

import pytest

from droras.hardware.null import NullAudioPlayer, NullStartSignal


# ---------------------------------------------------------------------------
# create_start_signal
# ---------------------------------------------------------------------------

def test_droras_gpio_off_returns_null(monkeypatch):
    """DRORAS_GPIO=off must return NullStartSignal without touching GPIO."""
    monkeypatch.setenv("DRORAS_GPIO", "off")
    # Re-import to bypass any module-level caching; factory reads env at call time
    import droras.hardware as hw
    signal = hw.create_start_signal()
    assert isinstance(signal, NullStartSignal)


def test_droras_gpio_mock_returns_gpio(monkeypatch):
    """DRORAS_GPIO=mock must return GpioStartSignal (via gpiozero MockFactory)."""
    monkeypatch.setenv("DRORAS_GPIO", "mock")
    monkeypatch.setenv("GPIOZERO_PIN_FACTORY", "mock")

    import droras.hardware as hw
    from droras.hardware.gpio import GpioStartSignal

    signal = hw.create_start_signal()
    assert isinstance(signal, GpioStartSignal)
    # on() / off() must not raise
    signal.on()
    signal.off()


def test_droras_gpio_auto_falls_back_on_failure(monkeypatch, caplog):
    """DRORAS_GPIO=auto: if GpioStartSignal raises, fall back to Null + WARNING log."""
    monkeypatch.setenv("DRORAS_GPIO", "auto")

    import droras.hardware as hw
    import droras.hardware.gpio as gpio_mod

    def bad_init(self, pin=26):
        raise RuntimeError("no GPIO hardware")

    monkeypatch.setattr(gpio_mod.GpioStartSignal, "__init__", bad_init)

    with caplog.at_level(logging.WARNING, logger="droras.hardware"):
        signal = hw.create_start_signal()

    assert isinstance(signal, NullStartSignal)
    assert any("WARNING" in r.levelname or r.levelno >= logging.WARNING for r in caplog.records)


def test_droras_gpio_on_propagates_exception(monkeypatch):
    """DRORAS_GPIO=on: if GPIO init fails, the exception must propagate (no fallback)."""
    monkeypatch.setenv("DRORAS_GPIO", "on")

    import droras.hardware as hw
    import droras.hardware.gpio as gpio_mod

    def bad_init(self, pin=26):
        raise RuntimeError("forced GPIO failure")

    monkeypatch.setattr(gpio_mod.GpioStartSignal, "__init__", bad_init)

    with pytest.raises(RuntimeError, match="forced GPIO failure"):
        hw.create_start_signal()


def test_droras_gpio_invalid_value_warns_and_falls_back(monkeypatch, caplog):
    """Unknown DRORAS_GPIO value must emit WARNING and use auto/fallback behaviour."""
    monkeypatch.setenv("DRORAS_GPIO", "banana")

    import droras.hardware as hw
    import droras.hardware.gpio as gpio_mod

    def bad_init(self, pin=26):
        raise RuntimeError("no GPIO")

    monkeypatch.setattr(gpio_mod.GpioStartSignal, "__init__", bad_init)

    with caplog.at_level(logging.WARNING, logger="droras.hardware"):
        signal = hw.create_start_signal()

    assert isinstance(signal, NullStartSignal)
    warning_messages = " ".join(r.message for r in caplog.records if r.levelno >= logging.WARNING)
    assert "banana" in warning_messages or any(
        "banana" in r.getMessage() for r in caplog.records if r.levelno >= logging.WARNING
    )


# ---------------------------------------------------------------------------
# create_audio_player
# ---------------------------------------------------------------------------

def test_create_audio_player_falls_back_on_failure(monkeypatch, caplog):
    """If PygameAudioPlayer init fails, fall back to NullAudioPlayer + WARNING."""
    import droras.hardware as hw
    import droras.hardware.audio as audio_mod

    def bad_init(self):
        raise RuntimeError("no audio device")

    monkeypatch.setattr(audio_mod.PygameAudioPlayer, "__init__", bad_init)

    with caplog.at_level(logging.WARNING, logger="droras.hardware"):
        player = hw.create_audio_player()

    assert isinstance(player, NullAudioPlayer)
    assert any(r.levelno >= logging.WARNING for r in caplog.records)


# ---------------------------------------------------------------------------
# Null implementations don't raise
# ---------------------------------------------------------------------------

def test_null_start_signal_no_exception():
    sig = NullStartSignal()
    sig.on()
    sig.off()


def test_null_audio_player_no_exception():
    player = NullAudioPlayer()
    player.play("pipipi.wav")
    player.play("po-n.wav")
