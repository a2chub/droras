## MODIFIED Requirements

### Requirement: 送信されるヒートリストの形式
クライアントに送信される `heat_list` の各行は、ヘッダー行を除いた二次元配列である SHALL 。

#### Scenario: heat_list payload 形式
- **WHEN** `heat_list` イベントが emit される
- **THEN** payload は `race_manager.all_heat_list[1:]` (固定ヘッダー `["R2", "F1", "R4", "R5", "HeatNo"]` を除外したリスト) である
- **AND** 各行は `[pilot1, pilot2, pilot3, pilot4, heat_number, class_name]` 形式 (6 要素) である
