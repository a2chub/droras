## MODIFIED Requirements

### Requirement: 最大 4 パイロットの横並び表示
画面は取得したパイロット名配列から、最大 4 名を横並びで SHALL 表示する。

#### Scenario: 4 名以上の場合
- **WHEN** `pilots` 配列の長さが 4 以上である
- **THEN** index 0, 1, 2, 3 の要素がそれぞれ 4 つの `<div>` に表示される

#### Scenario: 4 名未満の場合
- **WHEN** `pilots` 配列の長さが 4 未満である
- **THEN** 不足分の位置には空文字列が表示される
- **AND** 各 `<div>` のレイアウト (幅・中央揃え) は維持される
- **AND** `flex justify-around` により 4 枠の均等配置は維持される
