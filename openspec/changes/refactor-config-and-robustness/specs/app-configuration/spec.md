## ADDED Requirements

### Requirement: Settings による設定の一元管理
システムは、pydantic-settings ベースの `Settings` クラスで実行時設定を一元管理 SHALL し、環境変数プレフィックス `DRORAS_` で上書き可能 SHALL とする。管理対象は以下とする:

| 設定 | 環境変数 | デフォルト |
|------|----------|-----------|
| GAS URL (`gas_url`) | `DRORAS_GAS_URL` | 現行ハードコードの GAS URL |
| サーバーポート (`port`) | `DRORAS_PORT` | `8000` |
| GPIO ピン番号 (`gpio_pin`) | `DRORAS_GPIO_PIN` | `26` |
| GPIO モード (`gpio_mode`) | `DRORAS_GPIO` | `auto` |

#### Scenario: 環境変数による上書き
- **WHEN** `DRORAS_PORT=9000` が設定された状態でサーバーが起動する
- **THEN** サーバーはポート 9000 で listen する

#### Scenario: GAS URL の上書き
- **WHEN** `DRORAS_GAS_URL` に別のスプレッドシート出力 URL が設定されている
- **THEN** `download_heat_list()` はその URL から CSV を取得する

### Requirement: デフォルト値の後方互換性
すべての設定項目は、環境変数が未設定の場合に Phase 1+2 時点のハードコード値と同一のデフォルト値で動作 SHALL する。設定なしでのデプロイで挙動が変わることを SHALL NOT 許容する。

#### Scenario: 環境変数なしでの起動
- **WHEN** `DRORAS_*` 環境変数を一切設定せずにサーバーを起動する
- **THEN** ポート 8000、GPIO 26、従来の GAS URL、GPIO auto 検出で動作する

### Requirement: .env ファイルの読み込み
`Settings` は、プロジェクトルート (`run.sh` と同階層) の `.env` ファイルから設定を読み込み SHALL できる。環境変数が `.env` より優先 SHALL される。

#### Scenario: .env による設定
- **WHEN** プロジェクトルートに `DRORAS_PORT=9000` を含む `.env` が存在する
- **THEN** サーバーはポート 9000 で起動する

#### Scenario: 環境変数の優先
- **WHEN** `.env` に `DRORAS_PORT=9000`、環境変数に `DRORAS_PORT=9100` が設定されている
- **THEN** ポート 9100 が使用される

### Requirement: パス定数の維持
ディレクトリ・ファイルパス (`BASE_DIR` / `STATIC_DIR` / `LOG_DIR` / `SOUND_DIR` / `HEAT_LIST_CSV`) は、リポジトリ配置からの導出値としてモジュール定数のまま SHALL 維持する (環境変数化しない)。

#### Scenario: パス定数の参照
- **WHEN** 各モジュールが `config.HEAT_LIST_CSV` 等を参照する
- **THEN** Phase 1+2 と同一のモジュール定数として解決される

### Requirement: アプリケーションログ設定のエントリーポイント初期化
アプリケーションログの設定 (basicConfig 相当: ファイル + 標準出力、フォーマット) は、`droras` パッケージの import 時では SHALL NOT なく、エントリーポイント (`__main__.main()` および ASGI lifespan startup) で `setup_logging()` 関数により SHALL 初期化する。出力フォーマット・出力先 (`log/app.log` + stream) は現行と同一 SHALL とする。

#### Scenario: ライブラリとしての import
- **WHEN** テストコード等が `import droras` を実行する
- **THEN** root logger の設定変更やファイルハンドラ生成は発生しない

#### Scenario: python -m droras での起動
- **WHEN** `python -m droras` でサーバーを起動する
- **THEN** `setup_logging()` が実行され、従来同一のフォーマットで `log/app.log` と標準出力にログが記録される

#### Scenario: uvicorn 直接起動
- **WHEN** `uvicorn droras.server:app` で直接起動される
- **THEN** lifespan startup の `setup_logging()` によりログ設定が有効になる (二重呼び出しは無害)
