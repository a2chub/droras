"""Tests for RaceManager (race-control spec)."""

import asyncio
import logging


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class FakeSignal:
    def on(self): pass
    def off(self): pass


class FakeAudio:
    def play(self, name): pass


def _make_rm(monkeypatch, signal=None, audio=None):
    """Create a RaceManager with Firestore and event_logger faked out."""
    import droras.race_manager as rm_mod
    import droras.event_logger as el_mod

    def fake_connect(self):
        return None

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.race_manager import RaceManager
    return RaceManager(signal or FakeSignal(), audio or FakeAudio())


# ---------------------------------------------------------------------------
# Normal start
# ---------------------------------------------------------------------------

def test_start_runs_sequence_and_logs(monkeypatch):
    """Normal start(): sequence runs then log_heat_start is called with heat_index and pilots."""
    import droras.race_manager as rm_mod
    import droras.event_logger as el_mod

    call_log = []

    def fake_connect(self):
        return None

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)

    def fake_sequence(signal, audio):
        call_log.append("sequence")

    monkeypatch.setattr(rm_mod, "run_start_sequence", fake_sequence)

    def fake_log_start(heat_index, pilots):
        call_log.append(("log_heat_start", heat_index, pilots))

    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start", fake_log_start)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.race_manager import RaceManager

    # Supply a heat list so get_heat_pilots returns something
    rm = RaceManager(FakeSignal(), FakeAudio())
    rm.all_heat_list = [["R2", "F1", "R4", "R5", "HeatNo"], ["Alice", "Bob", "Carol", "Dave", 1, "A"]]
    rm.current_heat_index = 1

    result = asyncio.run(rm.start())

    assert result == {"status": 200}
    assert "sequence" in call_log
    # log_heat_start must come after sequence
    seq_pos = call_log.index("sequence")
    start_entries = [i for i, e in enumerate(call_log) if isinstance(e, tuple) and e[0] == "log_heat_start"]
    assert start_entries, "log_heat_start was never called"
    assert start_entries[0] > seq_pos, "log_heat_start must be called after sequence"


def test_start_log_includes_pilot_string(monkeypatch):
    """log_heat_start must receive the correct (heat_index, pilots_csv) arguments."""
    import droras.race_manager as rm_mod

    logged = []

    def fake_connect(self):
        return None

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)
    monkeypatch.setattr(rm_mod, "run_start_sequence", lambda sig, aud: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start", lambda hi, p: logged.append((hi, p)))
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.race_manager import RaceManager

    rm = RaceManager(FakeSignal(), FakeAudio())
    rm.all_heat_list = [["R2", "F1", "R4", "R5", "HeatNo"], ["Alice", "Bob", "Carol", "Dave", 1, "A"]]
    rm.current_heat_index = 1

    asyncio.run(rm.start())

    assert logged, "log_heat_start not called"
    heat_idx, pilots = logged[0]
    assert heat_idx == 1
    assert "Alice" in pilots


# ---------------------------------------------------------------------------
# Double-start guard
# ---------------------------------------------------------------------------

def test_double_start_guard(monkeypatch, caplog):
    """While sequence is running, a second start() must not start a new sequence."""
    import threading
    import droras.race_manager as rm_mod

    seq_start_count = [0]
    # Use a threading.Event so we can block the worker thread without
    # touching the asyncio event loop from within the thread.
    thread_gate = threading.Event()

    def fake_connect(self):
        return None

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)

    def blocking_sequence(sig, aud):
        seq_start_count[0] += 1
        thread_gate.wait()  # blocks the to_thread worker

    monkeypatch.setattr(rm_mod, "run_start_sequence", blocking_sequence)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.race_manager import RaceManager

    rm = RaceManager(FakeSignal(), FakeAudio())

    async def run_test():
        # Start first — sequence will block in worker thread
        task1 = asyncio.create_task(rm.start())
        # Yield to let to_thread start and set _sequence_running = True
        await asyncio.sleep(0.05)

        # Second start while first is still running
        with caplog.at_level(logging.WARNING, logger="droras.race_manager"):
            result2 = await rm.start()

        assert result2 == {"status": 200}, "double start should return 200"
        assert seq_start_count[0] == 1, "sequence should only have started once"
        assert any(
            "already running" in r.getMessage().lower() or "ignoring" in r.getMessage().lower()
            for r in caplog.records if r.levelno >= logging.WARNING
        )

        # Release the first sequence
        thread_gate.set()
        await task1

        assert rm._sequence_running is False

        # After completion a new start should work
        thread_gate.clear()
        thread_gate.set()
        result3 = await rm.start()
        assert result3 == {"status": 200}
        assert seq_start_count[0] == 2

    asyncio.run(run_test())


# ---------------------------------------------------------------------------
# Exception guard release
# ---------------------------------------------------------------------------

def test_exception_in_sequence_releases_guard(monkeypatch):
    """If sequence raises, _sequence_running must be reset to False."""
    import droras.race_manager as rm_mod

    def fake_connect(self):
        return None

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)

    def exploding_sequence(sig, aud):
        raise RuntimeError("boom")

    monkeypatch.setattr(rm_mod, "run_start_sequence", exploding_sequence)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.race_manager import RaceManager

    rm = RaceManager(FakeSignal(), FakeAudio())

    # First start raises but _sequence_running should be cleared
    # asyncio.to_thread propagates the exception through the coroutine
    try:
        asyncio.run(rm.start())
    except Exception:
        pass

    assert rm._sequence_running is False, "_sequence_running must be False after exception"

    # Second start should work (replaces sequence with a no-op for this check)
    monkeypatch.setattr(rm_mod, "run_start_sequence", lambda s, a: None)
    result = asyncio.run(rm.start())
    assert result == {"status": 200}


# ---------------------------------------------------------------------------
# Error path: get_heat_pilots raises
# ---------------------------------------------------------------------------

def test_error_path_logs_error_then_start(monkeypatch):
    """When get_heat_pilots raises, log_heat_error then log_heat_start must both be called.

    get_heat_pilots returns "" for an empty list (no exception). To trigger
    the exception path we patch get_heat_pilots in the race_manager namespace
    to raise directly.
    """
    import droras.race_manager as rm_mod

    call_log = []

    def fake_connect(self):
        return None

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)
    monkeypatch.setattr(rm_mod, "run_start_sequence", lambda s, a: None)

    # Make get_heat_pilots raise so the error branch is taken
    def raising_get_heat_pilots(heat_id, all_heat_list):
        raise IndexError("heat not found")

    monkeypatch.setattr(rm_mod, "get_heat_pilots", raising_get_heat_pilots)

    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start",
                        lambda hi, p: call_log.append(("log_heat_start", hi, p)))
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error",
                        lambda hi, p: call_log.append(("log_heat_error", hi, p)))
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.race_manager import RaceManager

    rm = RaceManager(FakeSignal(), FakeAudio())
    rm.all_heat_list = [["R2", "F1", "R4", "R5", "HeatNo"]]
    rm.current_heat_index = 1

    asyncio.run(rm.start())

    ops = [e[0] for e in call_log]
    assert "log_heat_error" in ops, "log_heat_error must be called on pilot lookup failure"
    assert "log_heat_start" in ops, "log_heat_start must still be called even after error"
    assert ops.index("log_heat_error") < ops.index("log_heat_start")


# ---------------------------------------------------------------------------
# set_current_heat writes to Firestore
# ---------------------------------------------------------------------------

def test_set_current_heat_writes_string_to_firestore(monkeypatch):
    """set_current_heat must write {"heat": "3"} (string) to the Firestore ref."""
    import droras.race_manager as rm_mod

    firestore_writes = []

    class FakeRef:
        async def set(self, data):
            firestore_writes.append(data)

    def fake_connect(self):
        return FakeRef()

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.race_manager import RaceManager

    rm = RaceManager(FakeSignal(), FakeAudio())
    # all_heat_list needs index 0..3 since we call set_current_heat(3)
    rm.all_heat_list = [
        ["R2", "F1", "R4", "R5", "HeatNo"],   # 0: header
        ["A", "B", "C", "D", 1, "X"],          # 1
        ["E", "F", "G", "H", 2, "X"],          # 2
        ["I", "J", "K", "L", 3, "X"],          # 3
    ]

    async def run():
        rm.set_current_heat(3)
        # Yield once so create_task starts
        await asyncio.sleep(0)
        # Drain all remaining tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if tasks:
            await asyncio.gather(*tasks)

    asyncio.run(run())

    assert firestore_writes, "Firestore set() was never called"
    assert firestore_writes[0] == {"heat": "3"}, f"Expected {{heat: '3'}}, got {firestore_writes[0]}"
