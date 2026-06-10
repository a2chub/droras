"""Tests for run_start_sequence (device-signals spec)."""

import asyncio


def test_sequence_call_order_and_timing(monkeypatch):
    """
    Verify exact call order: signal.on → audio.play(pipipi) → sleep(d)
    → audio.play(po-n) → sleep(0.35) → signal.off.
    Also verify randint(30,50) is called and d = result/10.0.
    """
    import droras.hardware.sequence as seq_mod

    recorder = []

    # --- monkeypatch randint in the sequence module namespace ---
    RAND_RETURN = 42

    def fake_randint(a, b):
        recorder.append(("randint", a, b))
        return RAND_RETURN

    def fake_sleep(seconds):
        recorder.append(("sleep", seconds))

    monkeypatch.setattr(seq_mod, "randint", fake_randint)
    monkeypatch.setattr(seq_mod, "sleep", fake_sleep)

    # --- fake hardware ---
    class _Sig:
        def on(self):  recorder.append(("signal.on", None))
        def off(self): recorder.append(("signal.off", None))

    class _Audio:
        def play(self, name): recorder.append(("audio.play", name))

    from droras.hardware.sequence import run_start_sequence
    run_start_sequence(_Sig(), _Audio())

    # Extract operation types in order
    ops = [(r[0], r[1]) for r in recorder]

    expected_d = RAND_RETURN / 10.0  # 4.2

    assert ops[0] == ("signal.on", None)
    assert ops[1] == ("audio.play", "pipipi.wav")
    assert ops[2] == ("randint", 30)          # randint(30, 50)
    assert ops[3] == ("sleep", expected_d)    # sleep(42/10.0)
    assert ops[4] == ("audio.play", "po-n.wav")
    assert ops[5] == ("sleep", 0.35)
    assert ops[6] == ("signal.off", None)


def test_sequence_randint_args(monkeypatch):
    """randint must be called with args (30, 50)."""
    import droras.hardware.sequence as seq_mod

    calls = []

    def fake_randint(a, b):
        calls.append((a, b))
        return 35

    monkeypatch.setattr(seq_mod, "randint", fake_randint)
    monkeypatch.setattr(seq_mod, "sleep", lambda s: None)

    class _NoOp:
        def on(self): pass
        def off(self): pass
        def play(self, name): pass

    from droras.hardware.sequence import run_start_sequence
    run_start_sequence(_NoOp(), _NoOp())

    assert calls == [(30, 50)]


def test_sequence_delay_is_randint_divided_by_10(monkeypatch):
    """d must equal randint_result / 10.0 and that value is passed to first sleep call."""
    import droras.hardware.sequence as seq_mod

    sleep_calls = []

    def fake_randint(a, b):
        return 47

    def fake_sleep(s):
        sleep_calls.append(s)

    monkeypatch.setattr(seq_mod, "randint", fake_randint)
    monkeypatch.setattr(seq_mod, "sleep", fake_sleep)

    class _NoOp:
        def on(self): pass
        def off(self): pass
        def play(self, name): pass

    from droras.hardware.sequence import run_start_sequence
    run_start_sequence(_NoOp(), _NoOp())

    assert sleep_calls[0] == 47 / 10.0
    assert sleep_calls[1] == 0.35
