## MODIFIED Requirements

### Requirement: カウントダウンシーケンスの発火
レース開始時、システムは注入された HAL デバイス (`StartSignal` / `AudioPlayer`) を通じて、device-signals capability が定義するスタートシーケンスを発火 SHALL する。実行環境 (RasPi / macOS / Linux) によらず同一コードパスを SHALL 使用し、環境差は HAL の実装選択 (hardware-abstraction) のみに SHALL 閉じる。

#### Scenario: レース開始シーケンスの発火
- **WHEN** `RaceManager.start()` が呼ばれる (シーケンス非実行中)
- **THEN** device-signals capability が定義するシーケンスが、注入済みデバイスで実行される
- **AND** OS 種別 (`platform.system()`) による分岐は行われない

#### Scenario: 非ブロッキング実行
- **WHEN** Socket.IO `start_heat` イベントによりシーケンスが実行中である
- **THEN** シーケンス本体はワーカースレッド (`asyncio.to_thread`) で実行され、イベントループはブロックされない
- **AND** シーケンス実行中も他クライアントの Socket.IO イベント・HTTP リクエストは通常通り処理される

### Requirement: 開始イベントのログ記録
システムは、`start()` 呼び出しのたびに、現在ヒート index と対応するパイロット情報をイベントログに記録 SHALL する。パイロット情報の取得失敗時も未定義変数参照を SHALL NOT 発生させる。

#### Scenario: 正常な開始
- **WHEN** `get_heat_pilots(current_heat_index, all_heat_list)` が例外を投げずに結果を返す
- **THEN** `event_logger.log_heat_start(current_heat_index, current_pilots)` が呼び出される
- **AND** パイロット情報が `INFO` レベルでログ出力される

#### Scenario: パイロット情報取得失敗
- **WHEN** `get_heat_pilots()` が例外を投げる
- **THEN** 例外は具体的にログ記録され (`Exception` 捕捉 + 原因情報)、`current_pilots` は空文字列として扱われる
- **AND** `event_logger.log_heat_error(current_heat_index, current_pilots)` が呼び出される
- **AND** 続けて `event_logger.log_heat_start(...)` も呼び出される (エラー時もヒート開始の記録は残す)

## ADDED Requirements

### Requirement: 二重スタートガード
スタートシーケンスの実行中に新たな開始要求を受けた場合、システムは新規シーケンスを開始 SHALL NOT せず、無視した旨を WARNING レベルでログに記録 SHALL する。

#### Scenario: 実行中の開始要求
- **WHEN** シーケンス実行中に `start_heat` イベントを受信する
- **THEN** 新規シーケンスは開始されない
- **AND** WARNING ログが記録される
- **AND** 実行中のシーケンスは影響を受けず継続する

#### Scenario: シーケンス完了後の開始要求
- **WHEN** 前回シーケンスが完了 (またはエラー終了) した後に `start_heat` イベントを受信する
- **THEN** 新規シーケンスが通常通り開始される (エラー終了時もガードが解放されている)

### Requirement: HAL デバイスの注入
`RaceManager` は、使用する `StartSignal` / `AudioPlayer` をコンストラクタで SHALL 受け取る。デバイスの生成 (能力検出・実装選択) は `RaceManager` の外 (サーバー起動処理) の責務 SHALL とする。

#### Scenario: サーバー起動時の注入
- **WHEN** サーバーの lifespan startup で `RaceManager` が生成される
- **THEN** `create_start_signal()` / `create_audio_player()` で生成されたデバイスがコンストラクタに渡される

#### Scenario: テスト時の差し替え
- **WHEN** テストコードが `RaceManager` を生成する
- **THEN** Null 実装やテストダブルをコンストラクタ引数として注入できる

## REMOVED Requirements

### Requirement: 開発環境における GPIO/音声スキップ
**Reason**: `platform.system()` による OS 分岐は Linux 開発機 / CI でクラッシュし、macOS では音声テストを不可能にしていた。能力検出ベースの実装選択 (hardware-abstraction) に置換される。
**Migration**: macOS では `DRORAS_GPIO` 未設定 (auto) のままシグナルが Null 実装となり音声は実再生される。GPIO/音声を完全に無効化したい場合は `DRORAS_GPIO=off` を設定する (音声はオーディオデバイス検出で自動判定)。
