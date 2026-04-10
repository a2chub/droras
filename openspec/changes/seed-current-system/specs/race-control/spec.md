## ADDED Requirements

### Requirement: レース開始トリガーの提供
システムは、Socket.IO 経由でオペレーターからのレース開始要求 (`start_heat` イベント) を受信し、レース開始シーケンスを発火 SHALL する。

#### Scenario: オペレーターが開始を要求する
- **WHEN** クライアントが Socket.IO `start_heat` イベントを送信する
- **THEN** サーバーは `RaceManager.start()` を呼び出す
- **AND** その呼び出しのログ (`Start heat: {sid}`) を記録する

### Requirement: カウントダウンシーケンスの発火
レース開始時、システムは `device-signals` capability を通じて LED 点灯・カウントダウン音・ランダム遅延・スタート音・LED 消灯から成る一連のシーケンスを発火 SHALL する。

#### Scenario: 本番環境 (非 Darwin) での開始
- **WHEN** `RaceManager.start()` が呼ばれ、実行プラットフォームが Darwin 以外である
- **THEN** `droras.device.start_sound()` が呼び出される
- **AND** `device-signals` capability が定義するシーケンスが実行される

### Requirement: 開発環境における GPIO/音声スキップ
macOS (Darwin) 環境では、ハードウェア依存のため、システムは GPIO および音声処理を SHALL NOT 実行する。

#### Scenario: macOS (Darwin) での開始
- **WHEN** `RaceManager.start()` が呼ばれ、実行プラットフォームが Darwin である
- **THEN** `droras.device` モジュールの import は行われない
- **AND** GPIO 操作および音声再生は一切発生しない
- **AND** イベントログ記録は通常通り行われる

### Requirement: 開始イベントのログ記録
システムは、`start()` 呼び出しのたびに、現在ヒート index と対応するパイロット情報をイベントログに記録 SHALL する。

#### Scenario: 正常な開始
- **WHEN** `get_heat_pilots(current_heat_index, all_heat_list)` が例外を投げずに結果を返す
- **THEN** `event_logger.log_heat_start(current_heat_index, current_pilots)` が呼び出される
- **AND** パイロット情報が `INFO` レベルでログ出力される

#### Scenario: パイロット情報取得失敗
- **WHEN** `get_heat_pilots()` が例外を投げる
- **THEN** `event_logger.log_heat_error(current_heat_index, current_pilots)` が呼び出される
- **AND** 続けて `event_logger.log_heat_start(...)` も呼び出される (現行実装の忠実な再現)

### Requirement: 開始呼び出しの戻り値
`RaceManager.start()` は HTTP ステータス 200 を示す辞書 `{"status": 200}` を SHALL 返す。

#### Scenario: start() の戻り値
- **WHEN** `RaceManager.start()` が完了する
- **THEN** 戻り値は `{"status": 200}` である
