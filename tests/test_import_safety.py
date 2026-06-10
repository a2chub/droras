"""Tests that importing droras modules has no hardware side-effects (hardware-abstraction spec)."""

import sys


def test_import_hardware_package():
    import droras.hardware  # noqa: F401


def test_import_hardware_gpio():
    import droras.hardware.gpio  # noqa: F401


def test_import_hardware_audio():
    import droras.hardware.audio  # noqa: F401


def test_import_hardware_null():
    import droras.hardware.null  # noqa: F401


def test_import_hardware_base():
    import droras.hardware.base  # noqa: F401


def test_import_hardware_sequence():
    import droras.hardware.sequence  # noqa: F401


def test_import_server_race_manager_is_none():
    """After importing droras.server (but before lifespan runs), race_manager must be None."""
    import droras.server as srv
    assert srv.race_manager is None
