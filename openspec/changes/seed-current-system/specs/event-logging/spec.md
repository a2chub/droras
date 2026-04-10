## ADDED Requirements

### Requirement: ヒートイベントログファイル
システムは、ヒートイベントを `log/heat_start.csv` に追記 SHALL する。

#### Scenario: ログファイル配置
- **WHEN** `event_logger` モジュールが import される
- **THEN** `TimedRotatingFileHandler` が `config.LOG_DIR/heat_start.csv` に対して作成される
- **AND** ログレベルは `INFO` 以上を記録する

### Requirement: 深夜ローテーションと保持数
システムは、毎日深夜 (`MIDNIGHT`) にログファイルをローテーション SHALL し、最大 100 個のバックアップを保持する。

#### Scenario: ローテーション設定
- **WHEN** `TimedRotatingFileHandler` が初期化される
- **THEN** `when="MIDNIGHT"`, `interval=1`, `backupCount=100` で設定される

### Requirement: ローテーション後のファイル名規則
ローテーション後のバックアップファイルは `heat_start_YYYY-MM-DD.csv` 形式で SHALL 命名する。

#### Scenario: ローテーションファイル名の変換
- **WHEN** ローテーションが発生し、デフォルト名が `heat_start.csv.2026-04-10` のような形式である
- **THEN** `namer` により正規表現 `\.([^.]+)\.(\d{4})-(\d{2})-(\d{2})$` → `_\2-\3-\4.\1` の置換が適用される
- **AND** 最終ファイル名は `heat_start_2026-04-10.csv` となる

### Requirement: ログ行フォーマット
各ログ行は `YYYY/MM/DD,HH:MM:SS,<heat_index>,<event_type>,<pilots_csv>` の形式で SHALL 記録する。

#### Scenario: フォーマット構成
- **WHEN** ログが書き込まれる
- **THEN** タイムスタンプは `%Y/%m/%d,%H:%M:%S` 形式で先頭に出力される
- **AND** `%(message)s` 部分に `<heat_index>,<event_type>,<pilots_csv>` が続く
- **AND** カラム区切りはすべてカンマ (`,`) である

### Requirement: イベントタイプ
システムは、以下 3 種類のイベントタイプを SHALL 記録する:

- `start_heat` — レース開始時
- `change_heat` — カレントヒート変更時
- `firebase_send_error` — パイロット情報取得失敗時

#### Scenario: start_heat の記録
- **WHEN** `log_heat_start(heat_index, pilots)` が呼ばれる
- **THEN** `<heat_index>,start_heat,<pilots>` が `INFO` レベルで記録される

#### Scenario: change_heat の記録
- **WHEN** `log_heat_change(heat_index, pilots)` が呼ばれる
- **THEN** `<heat_index>,change_heat,<pilots>` が `INFO` レベルで記録される

#### Scenario: firebase_send_error の記録
- **WHEN** `log_heat_error(heat_index, pilots)` が呼ばれる
- **THEN** `<heat_index>,firebase_send_error,<pilots>` が `ERROR` レベルで記録される
- **AND** 現行実装では `race_manager.start()` 内でパイロット情報取得失敗時にのみ呼ばれる (Firestore エラーとは無関係な命名である点を明記)

### Requirement: ロガーの独立性
ヒートイベントログは、独立した named logger `"heatStartLog"` を SHALL 使用する。

#### Scenario: ロガー名
- **WHEN** `event_logger` がロガーを取得する
- **THEN** `logging.getLogger("heatStartLog")` が使われる
- **AND** 他の application ロガーのハンドラとは独立して `log/heat_start.csv` へのみ出力する
