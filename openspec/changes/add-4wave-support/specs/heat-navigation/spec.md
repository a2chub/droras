## MODIFIED Requirements

### Requirement: カレントパイロットの HTTP 参照
システムは HTTP `GET /current_pilots` にてカレントヒートの行全体を `","` 分割した文字列配列を JSON で返 SHALL す。返却される配列は 6 要素: `[pilot1, pilot2, pilot3, pilot4, heat_no_as_string, class_name]`。

#### Scenario: カレントパイロット取得
- **WHEN** クライアントが `GET /current_pilots` を要求する
- **THEN** レスポンスはカレントヒート行を `","` で分割した 6 要素の文字列配列である
- **AND** 先頭 4 要素 (index 0〜3) がパイロット名である
- **AND** index 4 はヒート番号の文字列表現、index 5 はクラス名である
- **AND** `Content-Type: application/json` で返される
