## ADDED Requirements

### Requirement: ハードウェア操作の Protocol 定義
システムは、GPIO シグナルと音声再生を `typing.Protocol` による抽象インターフェースとして定義 SHALL する。`StartSignal` は `on()` / `off()` を、`AudioPlayer` は `play(sound_name)` (再生開始のみ、完了待機は呼び出し側責務) を持つ。

#### Scenario: StartSignal インターフェース
- **WHEN** 任意の `StartSignal` 実装の `on()` / `off()` が呼ばれる
- **THEN** シグナル (リレー/LED) の点灯・消灯に相当する操作が実行される
- **AND** 呼び出し側は具象実装 (GPIO / Null) を区別しない

#### Scenario: AudioPlayer インターフェース
- **WHEN** 任意の `AudioPlayer` 実装の `play(sound_name)` が呼ばれる
- **THEN** `config.SOUND_DIR` 配下の該当音源の再生が開始される (または Null 実装ではログのみ記録される)
- **AND** `play()` は再生完了を待たずに返る

### Requirement: 環境変数 DRORAS_GPIO による実装選択
シグナル実装の選択は、環境変数 `DRORAS_GPIO` (`auto` / `on` / `off` / `mock`、デフォルト `auto`) で制御 SHALL する。`platform.system()` などの OS 種別による分岐を SHALL NOT 使用する。

#### Scenario: auto — GPIO 利用可能環境 (RasPi)
- **WHEN** `DRORAS_GPIO` が未設定または `auto` で、gpiozero のピンファクトリ初期化が成功する
- **THEN** GPIO 実装 (`GpioStartSignal`、GPIO 26) が選択される

#### Scenario: auto — GPIO 不在環境 (macOS / CI)
- **WHEN** `DRORAS_GPIO` が未設定または `auto` で、gpiozero の import またはピンファクトリ初期化が失敗する
- **THEN** Null 実装にフォールバックする
- **AND** フォールバックした旨が WARNING レベルでログに記録される
- **AND** プロセスは起動を継続する

#### Scenario: on — GPIO 強制
- **WHEN** `DRORAS_GPIO=on` で GPIO 初期化が失敗する
- **THEN** 起動時に例外が送出され、フォールバックは行われない (本番での配線・権限異常の黙殺防止)

#### Scenario: off — Null 強制
- **WHEN** `DRORAS_GPIO=off` が設定されている
- **THEN** GPIO 利用可否にかかわらず Null 実装が選択される

#### Scenario: mock — gpiozero MockFactory
- **WHEN** `DRORAS_GPIO=mock` が設定されている
- **THEN** `GPIOZERO_PIN_FACTORY=mock` を適用した上で gpiozero 実装が選択される (gpiozero コード経路の検証用)

### Requirement: 音声実装の独立した能力検出
音声再生の実装選択は、GPIO の有無と独立に `pygame.mixer.init()` の成否で SHALL 決定する。

#### Scenario: オーディオ利用可能環境 (RasPi / macOS)
- **WHEN** `pygame.mixer.init()` が成功する
- **THEN** pygame 実装が選択され、実音声が再生される (macOS 開発環境でも実再生)

#### Scenario: オーディオ不在環境 (ヘッドレス CI 等)
- **WHEN** pygame の import または `pygame.mixer.init()` が失敗する
- **THEN** Null 実装にフォールバックし、WARNING レベルでログに記録される
- **AND** プロセスは起動を継続する

### Requirement: import 副作用の禁止
`droras.hardware` パッケージおよびその全サブモジュールの import は、ハードウェア初期化 (GPIO ピン確保、pygame init) を SHALL NOT 実行する。gpiozero / pygame の import は実装の初期化処理内に遅延 SHALL される。

#### Scenario: GPIO 不在環境での import
- **WHEN** gpiozero / rpi-gpio が動作しない環境で `droras.hardware` (および `hardware.gpio` を含む全サブモジュール) が import される
- **THEN** import は例外なく成功する

#### Scenario: 初期化のタイミング
- **WHEN** ファクトリ関数 (`create_start_signal()` / `create_audio_player()`) が呼ばれる
- **THEN** この時点で初めて GPIO ピン確保 / `pygame.mixer.init()` が実行される

### Requirement: Null 実装の挙動
Null 実装は、対応する操作を実行せず、操作内容を INFO レベルでログに記録 SHALL する。例外を SHALL NOT 送出する。

#### Scenario: Null シグナル操作
- **WHEN** `NullStartSignal` の `on()` / `off()` が呼ばれる
- **THEN** ハードウェア操作は行われず、操作内容 (on/off) がログに記録される

#### Scenario: Null 音声再生
- **WHEN** `NullAudioPlayer` の `play(sound_name)` が呼ばれる
- **THEN** 音声は再生されず、音源名がログに記録され、即座に返る

### Requirement: 手動テスト用エントリーポイント
`python -m droras.hardware` の実行により、サーバーを起動せずスタートシーケンス一式 (シグナル + 音声) を単独実行 SHALL できる。実装選択は通常起動と同じ `DRORAS_GPIO` のルールに従う。

#### Scenario: 単独実行
- **WHEN** `python -m droras.hardware` が実行される
- **THEN** ファクトリでデバイスを生成し、スタートシーケンス (シグナル ON → カウントダウン音 → ランダム遅延 → スタート音 → シグナル OFF) を 1 回実行して終了する
