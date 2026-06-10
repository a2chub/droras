## MODIFIED Requirements

### Requirement: ヒートイベントログファイル
システムは、ヒートイベントを `config.LOG_DIR/heat_start.csv` に追記 SHALL する。`TimedRotatingFileHandler` の生成は `event_logger` モジュールの import 時では SHALL NOT なく、最初のログ記録呼び出し時に遅延初期化 SHALL する。初期化時に `config.LOG_DIR` の存在を SHALL 保証する (なければ作成)。

#### Scenario: import 時の副作用なし
- **WHEN** `droras.event_logger` モジュールが import される
- **THEN** ファイルハンドラの生成・ログディレクトリの作成は発生しない

#### Scenario: 初回ログ記録時の初期化
- **WHEN** `log_heat_start` / `log_heat_change` / `log_heat_error` のいずれかが初めて呼ばれる
- **THEN** `TimedRotatingFileHandler` が `config.LOG_DIR/heat_start.csv` に対して作成される (以降の呼び出しでは再生成されない)
- **AND** `config.LOG_DIR` が存在しなければ作成される
- **AND** ログレベルは `INFO` 以上を記録する

#### Scenario: 出力の互換性
- **WHEN** 遅延初期化後にヒートイベントが記録される
- **THEN** ログ行フォーマット・ローテーション設定 (`MIDNIGHT` / `backupCount=100`)・ファイル名規則 (`heat_start_YYYY-MM-DD.csv`)・logger 名 (`heatStartLog`) は従来と同一である
