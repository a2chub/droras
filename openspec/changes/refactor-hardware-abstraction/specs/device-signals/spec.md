## MODIFIED Requirements

### Requirement: LED (リレー HAT) の制御
システムは、`StartSignal` 抽象 (hardware-abstraction) を通じて LED シグナルを点灯・消灯 SHALL する。GPIO 環境における実装は gpiozero を用い、ピン番号は従来通り GPIO 26 SHALL とする。

#### Scenario: LED 点灯
- **WHEN** スタートシーケンスがシグナル ON を要求する
- **THEN** 選択された `StartSignal` 実装の `on()` が実行される (GPIO 環境では GPIO 26 が ON)
- **AND** 点灯操作がログに記録される

#### Scenario: LED 消灯
- **WHEN** スタートシーケンスがシグナル OFF を要求する
- **THEN** 選択された `StartSignal` 実装の `off()` が実行される (GPIO 環境では GPIO 26 が OFF)
- **AND** 消灯操作がログに記録される

### Requirement: カウントダウン + スタート音シーケンス
スタートシーケンスは、注入された `StartSignal` / `AudioPlayer` を用いて以下の順序で SHALL 実行する。順序・タイミング・音源ファイルは従来実装と同一 SHALL とする:

1. シグナル ON
2. カウントダウン音 `pipipi.wav` の再生開始
3. `randint(30, 50) / 10.0` 秒 (= **3.0〜5.0 秒**) のランダム遅延
4. スタート音 `po-n.wav` の再生開始
5. 0.35 秒待機
6. シグナル OFF

#### Scenario: スタートシーケンスの実行順序
- **WHEN** スタートシーケンスが実行される
- **THEN** シグナル ON → カウントダウン音再生 → ランダム遅延 → スタート音再生 → 0.35 秒待機 → シグナル OFF の順に処理が進む
- **AND** シーケンス内部は同期的に実行される (サーバーから呼ぶ際の非ブロッキング化は race-control の責務)

#### Scenario: ランダム遅延の範囲
- **WHEN** 遅延計算 `float(randint(30, 50)) / 10.0` が実行される
- **THEN** 遅延値は 3.0 秒以上 5.0 秒以下 (両端含む、0.1 秒刻み) である

#### Scenario: GPIO 不在環境でのシーケンス
- **WHEN** Null シグナル実装が選択された環境 (macOS 等) でシーケンスが実行される
- **THEN** 音声再生とタイミングは GPIO 環境と同一に動作し、シグナル操作はログ記録のみとなる

### Requirement: 音声リソースパスの解決
音源ファイルは `config.SOUND_DIR` (= `BASE_DIR/sound`) 配下の絶対パスとして解決 SHALL される。カレントディレクトリおよびモジュール位置からの相対パス解決を SHALL NOT 使用する。

#### Scenario: リソースパス解決
- **WHEN** `AudioPlayer` が音源名 `pipipi.wav` の再生を要求される
- **THEN** `<BASE_DIR>/sound/pipipi.wav` の絶対パスで音源が読み込まれる
- **AND** プロセスの CWD に依存しない

### Requirement: __main__ エントリーポイント
ハードウェアシーケンスの単独手動テストは `python -m droras.hardware` で SHALL 実行できる (旧 `python -m droras.device` を置換)。

#### Scenario: スクリプト直接実行
- **WHEN** `python -m droras.hardware` が実行される
- **THEN** スタートシーケンスが 1 回実行される

## REMOVED Requirements

### Requirement: モジュール import 時の初期化
**Reason**: import 時の `LED(26)` 実体化と `pygame.init()` が GPIO 不在環境でのクラッシュ原因であり、hardware-abstraction の「import 副作用の禁止」要件に置換される。
**Migration**: ハードウェア初期化はファクトリ関数 (`create_start_signal()` / `create_audio_player()`) 呼び出し時 (サーバー lifespan startup) に実行される。

### Requirement: 連打防止機構の不在
**Reason**: 実行中の二重スタートは音の重複と LED 状態不整合を起こすため、race-control に二重スタートガードを追加する。「抑止しない」ことを保証する本要件は廃止。
**Migration**: race-control の「二重スタートガード」要件を参照。シーケンス非実行中の挙動 (即時開始) は変わらない。
