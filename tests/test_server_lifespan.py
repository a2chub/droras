"""Integration test: server lifespan startup (heatlist-ingestion + race-control HAL injection)."""

import csv
import os


def _write_heat_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def test_lifespan_creates_race_manager_and_current_pilots(monkeypatch, tmp_path):
    """
    After TestClient context opens (lifespan fires):
    - droras.server.race_manager must be a RaceManager instance
    - GET /current_pilots must return a 6-element array
    """
    # 実運用フォーマット (GAS 出力) はヘッダー行を含む。load_heat_list の
    # range(1, len(by_heat)) はヘッダー行の "HeatNo" キーを前提にしている。
    csv_file = tmp_path / "heat_list.csv"
    rows = [
        ["No", "Name", "Class", "HeatNo"],
        ["X", "Alice", "A", "1"],
        ["X", "Bob",   "A", "1"],
        ["X", "Carol", "A", "1"],
        ["X", "Dave",  "A", "1"],
        ["X", "Eve",   "B", "2"],
        ["X", "Frank", "B", "2"],
        ["X", "Grace", "B", "2"],
        ["X", "Hank",  "B", "2"],
    ]
    _write_heat_csv(csv_file, rows)

    # --- env: DRORAS_GPIO=off to skip GPIO entirely ---
    monkeypatch.setenv("DRORAS_GPIO", "off")

    # --- patch HEAT_LIST_CSV before server module is evaluated ---
    import droras.convert_heatlist as ch
    import droras.config as cfg

    monkeypatch.setattr(cfg, "HEAT_LIST_CSV", str(csv_file))
    monkeypatch.setattr(ch.config, "HEAT_LIST_CSV", str(csv_file))

    # --- patch Firestore to avoid real connection ---
    import droras.race_manager as rm_mod

    def fake_connect(self):
        return None

    monkeypatch.setattr(rm_mod.RaceManager, "connect_to_firestore", fake_connect)

    # --- patch event_logger to avoid CSV writes ---
    import droras.event_logger as el_mod

    monkeypatch.setattr(el_mod, "log_heat_start", lambda *a: None)
    monkeypatch.setattr(el_mod, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(el_mod, "log_heat_change", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_start", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_error", lambda *a: None)
    monkeypatch.setattr(rm_mod.event_logger, "log_heat_change", lambda *a: None)

    from droras.hardware.null import NullAudioPlayer, NullStartSignal

    # server.py does `from .hardware import create_audio_player`, so we must
    # patch the name in the droras.server module namespace, not in hardware.
    import droras.server as srv
    monkeypatch.setattr(srv, "create_audio_player", lambda: NullAudioPlayer())

    from fastapi.testclient import TestClient
    from droras.race_manager import RaceManager

    with TestClient(srv.app) as client:
        # race_manager must be set inside lifespan
        assert srv.race_manager is not None
        assert isinstance(srv.race_manager, RaceManager)

        # /current_pilots returns a 6-element list
        # (4 pilot names + heat_no + class as strings after comma-join and split)
        response = client.get("/current_pilots")
        assert response.status_code == 200
        data = response.json()
        assert data == ["Alice", "Bob", "Carol", "Dave", "1", "A"]
