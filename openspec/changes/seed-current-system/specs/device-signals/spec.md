## ADDED Requirements

### Requirement: LED (リレー HAT) の制御
システムは、ラズパイの GPIO 26 に接続された `gpiozero.LED` インスタンスを用いて LED を点灯・消灯 SHALL する。

#### Scenario: LED 点灯
- **WHEN** `led_on()` が呼ばれる
- **THEN** `LED(26).on()` が実行される
- **AND** `INFO: LED on` のログが記録される

#### Scenario: LED 消灯
- **WHEN** `led_off()` が呼ばれる
- **THEN** `LED(26).off()` が実行される
- **AND** `INFO: LED off` のログが記録される

### Requirement: カウントダウン + スタート音シーケンス
`start_sound()` 呼び出し時、システムは以下の順序でシーケンスを SHALL 実行する:

1. LED 点灯 (`led_on()`)
2. カウントダウン音 `sound/pipipi.wav` を `pygame.mixer.Sound` で再生開始
3. `randint(30, 50) / 10.0` 秒 (= **3.0〜5.0 秒**) のランダム遅延
4. スタート音 `sound/po-n.wav` を再生開始 (`start_signal()`)
5. 0.35 秒後に LED 消灯 (`led_off()`)

#### Scenario: スタートシーケンスの実行順序
- **WHEN** `start_sound()` が呼び出される
- **THEN** LED ON → カウントダウン音再生 → ランダム遅延 → スタート音再生 → 0.35 秒待機 → LED OFF の順に処理が進む
- **AND** 各ステップは同期的に (blocking で) 実行される

#### Scenario: ランダム遅延の範囲
- **WHEN** `start_sound()` の遅延計算 `float(randint(30, 50)) / 10.0` が実行される
- **THEN** 遅延値は 3.0 秒以上 5.0 秒以下 (両端含む、0.1 秒刻み) である

### Requirement: 音声リソースパスの解決
音源ファイルは `get_resource_path("sound", <filename>)` により、モジュールの配置位置から相対的に `../../sound/<filename>` として解決 SHALL される。

#### Scenario: リソースパス解決
- **WHEN** `get_resource_path("sound", "pipipi.wav")` が呼ばれる
- **THEN** 戻り値は `<device.py のディレクトリ>/../../sound/pipipi.wav` の絶対パス形式となる

### Requirement: モジュール import 時の初期化
`droras.device` モジュールは import 時点で GPIO LED と pygame を初期化 SHALL する。

#### Scenario: モジュール import
- **WHEN** `droras.device` が import される
- **THEN** `LED(26)` インスタンス (`four`) がモジュールレベルで生成される
- **AND** `pygame.init()` が実行される
- **AND** `pygame.mixer.init()` が実行される

### Requirement: 連打防止機構の不在
現行実装は `start_sound()` 呼び出しの連打防止を SHALL NOT 行わない。

#### Scenario: 連続呼び出し
- **WHEN** `start_sound()` が短時間に連続で呼び出される
- **THEN** 各呼び出しは条件分岐 `if True:` により必ずシーケンスを実行する
- **AND** `isPlayable()` 関数や `PLAY_FLG` 変数による抑制は効かない (現行実装の忠実な記述)

### Requirement: __main__ エントリーポイント
`device.py` をスクリプトとして直接実行した場合、システムは単独で `start_sound()` を SHALL 実行する。

#### Scenario: スクリプト直接実行
- **WHEN** `python -m droras.device` または `python src/droras/device.py` が実行される
- **THEN** `start_sound()` が呼び出される
