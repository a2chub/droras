## MODIFIED Requirements

### Requirement: ヒート行の正規化フォーマット
各ヒート行は `[pilot1, pilot2, pilot3, pilot4, heat_number, class_name]` の順で SHALL 構築する。

#### Scenario: ヒート行の構築
- **WHEN** ヒート番号 `i` に対応する行群 `pilots` が存在する (4 行)
- **THEN** 各 `pilots[ii][1]` (パイロット名) が順に配列に追加される (4 回)
- **AND** 続けてヒート番号 `i` が追加される
- **AND** 続けて `pilots[0][2]` (class 名) が追加される
- **AND** 最終的な行の長さは 6 要素となる

### Requirement: 固定ヘッダーの先頭行
返却される配列の先頭行は、固定のラベル行 `["R2", "F1", "R4", "R5", "HeatNo"]` で SHALL ある。

#### Scenario: ヘッダー行の存在
- **WHEN** `load_heat_list()` が結果を返す
- **THEN** 結果の index 0 は常に `["R2", "F1", "R4", "R5", "HeatNo"]` である
- **AND** この行はクライアント送信時 (realtime-sync) に除外される前提で維持される
- **AND** この行は `get_heat_pilots(heat_id=1)` で `all_heat_list[1]` からヒート 1 の行を取得できるようにするための 1-based index sentinel として機能する
