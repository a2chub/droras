"""Tests for heatlist loading and pilot helpers (heatlist-ingestion spec).

実運用の CSV (GAS の doGet 出力) は 1 行目にヘッダー行を含む。
load_heat_list() はヒート番号列 (row[3]) でグループ化するため、ヘッダー行の
"HeatNo" が by_heat のキーを 1 つ増やし、range(1, len(by_heat)) で
全ヒートが読まれる構造になっている。テストデータは必ずこの形に合わせること
(ヘッダー行を省くと最終ヒートが落ちる — 下の documenting test を参照)。
"""

import csv


def _write_heat_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


# CSV columns: col0=no, col1=pilot_name, col2=class, col3=heat_no
HEADER_ROW = ["No", "Name", "Class", "HeatNo"]


def _pilot_row(pilot_name, class_name, heat_no):
    return ["X", pilot_name, class_name, str(heat_no)]


SAMPLE_PILOTS_HEAT1 = [
    _pilot_row("Alice", "A", 1),
    _pilot_row("Bob",   "A", 1),
    _pilot_row("Carol", "A", 1),
    _pilot_row("Dave",  "A", 1),
]

SAMPLE_PILOTS_HEAT2 = [
    _pilot_row("Eve",   "B", 2),
    _pilot_row("Frank", "B", 2),
    _pilot_row("Grace", "B", 2),
    _pilot_row("Hank",  "B", 2),
]


# ---------------------------------------------------------------------------
# load_heat_list
# ---------------------------------------------------------------------------

def test_load_heat_list_two_heats(monkeypatch, tmp_path):
    """ヘッダー行付き CSV (実運用フォーマット) で全ヒートが 6 要素行として読まれる。"""
    csv_file = tmp_path / "heat_list.csv"
    _write_heat_csv(csv_file, [HEADER_ROW] + SAMPLE_PILOTS_HEAT1 + SAMPLE_PILOTS_HEAT2)

    import droras.convert_heatlist as ch

    monkeypatch.setattr(ch.config, "HEAT_LIST_CSV", str(csv_file))

    result = ch.load_heat_list()

    assert result == [
        ["R2", "F1", "R4", "R5", "HeatNo"],
        ["Alice", "Bob", "Carol", "Dave", 1, "A"],
        ["Eve", "Frank", "Grace", "Hank", 2, "B"],
    ]


def test_load_heat_list_without_header_drops_last_heat(monkeypatch, tmp_path):
    """データ形式の前提を文書化: ヘッダー行が無い CSV では最終ヒートが落ちる.

    range(1, len(by_heat)) はヘッダー行の "HeatNo" キーがキー数を 1 つ
    増やすことを前提としている。GAS 側がヘッダー行を出力しなくなった場合は
    この前提が崩れるため、本テストでその挙動を固定して検知可能にしておく。
    """
    csv_file = tmp_path / "heat_list.csv"
    _write_heat_csv(csv_file, SAMPLE_PILOTS_HEAT1 + SAMPLE_PILOTS_HEAT2)

    import droras.convert_heatlist as ch

    monkeypatch.setattr(ch.config, "HEAT_LIST_CSV", str(csv_file))

    result = ch.load_heat_list()

    # ヘッダー無しではヒート 2 が返らない (既知のデータ形式依存)
    assert result == [
        ["R2", "F1", "R4", "R5", "HeatNo"],
        ["Alice", "Bob", "Carol", "Dave", 1, "A"],
    ]


def test_load_heat_list_file_missing_returns_header_only(monkeypatch, tmp_path):
    """CSV ファイル不在時は例外を出さずヘッダー行のみ返す。"""
    import droras.convert_heatlist as ch

    monkeypatch.setattr(ch.config, "HEAT_LIST_CSV", str(tmp_path / "nonexistent.csv"))

    result = ch.load_heat_list()

    assert result == [["R2", "F1", "R4", "R5", "HeatNo"]]


def test_load_heat_list_cwd_independent(monkeypatch, tmp_path):
    """load_heat_list は CWD に依存せず config.HEAT_LIST_CSV の絶対パスで読む。"""
    csv_file = tmp_path / "heat_list.csv"
    _write_heat_csv(csv_file, [HEADER_ROW] + SAMPLE_PILOTS_HEAT1 + SAMPLE_PILOTS_HEAT2)

    import droras.convert_heatlist as ch

    monkeypatch.setattr(ch.config, "HEAT_LIST_CSV", str(csv_file))
    monkeypatch.chdir(tmp_path / "..")

    result = ch.load_heat_list()

    assert len(result) == 3  # header + 2 heats
    assert result[0] == ["R2", "F1", "R4", "R5", "HeatNo"]


# ---------------------------------------------------------------------------
# get_heat_pilots
# ---------------------------------------------------------------------------

def test_get_heat_pilots_empty_list():
    """空の all_heat_list は空文字列を返す。"""
    from droras.convert_heatlist import get_heat_pilots

    assert get_heat_pilots(1, []) == ""


def test_get_heat_pilots_normal():
    """正常系はヒート行要素のカンマ結合文字列を返す。"""
    from droras.convert_heatlist import get_heat_pilots

    heat_list = [
        ["R2", "F1", "R4", "R5", "HeatNo"],          # index 0: header
        ["Alice", "Bob", "Carol", "Dave", 1, "A"],   # index 1: heat 1
    ]
    assert get_heat_pilots(1, heat_list) == "Alice,Bob,Carol,Dave,1,A"
