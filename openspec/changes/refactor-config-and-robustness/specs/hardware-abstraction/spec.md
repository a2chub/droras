## MODIFIED Requirements

### Requirement: 環境変数 DRORAS_GPIO による実装選択
シグナル実装の選択は、設定 `settings.gpio_mode` (環境変数 `DRORAS_GPIO`: `auto` / `on` / `off` / `mock`、デフォルト `auto`) で制御 SHALL する。GPIO 実装が使用するピン番号は `settings.gpio_pin` (環境変数 `DRORAS_GPIO_PIN`、デフォルト `26`) から取得 SHALL する。`platform.system()` などの OS 種別による分岐を SHALL NOT 使用する。

#### Scenario: auto — GPIO 利用可能環境 (RasPi)
- **WHEN** `DRORAS_GPIO` が未設定または `auto` で、gpiozero のピンファクトリ初期化が成功する
- **THEN** GPIO 実装 (`GpioStartSignal`、ピン番号は `settings.gpio_pin`) が選択される

#### Scenario: ピン番号の設定上書き
- **WHEN** `DRORAS_GPIO_PIN=21` が設定された状態でファクトリが GPIO 実装を生成する
- **THEN** GPIO 21 が使用される

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
