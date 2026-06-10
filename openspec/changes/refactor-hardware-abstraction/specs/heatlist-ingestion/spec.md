## MODIFIED Requirements

### Requirement: GAS URL からの CSV ダウンロード
システムは、設定された Google Apps Script URL (`convert_heatlist.url`) から HTTP GET で CSV データを取得 SHALL し、`config.HEAT_LIST_CSV` (= `config.LOG_DIR` 配下の `heat_list.csv` 絶対パス) に保存する。

#### Scenario: ダウンロード成功
- **WHEN** `download_heat_list()` が呼ばれ、レスポンスステータスが 200 である
- **THEN** レスポンス body が `config.HEAT_LIST_CSV` にバイナリ書き込みされる
- **AND** 成功ログが記録される
- **AND** 保存先はプロセスの CWD に依存しない

#### Scenario: 非 200 ステータス
- **WHEN** レスポンスステータスが 200 以外である
- **THEN** ファイル書き込みは行われない
- **AND** `Failed to download heat list. status code: {code}` のエラーログが記録される

#### Scenario: HTTP リクエスト例外
- **WHEN** `requests.exceptions.RequestException` が発生する
- **THEN** 例外は捕捉され、エラーログが記録される
- **AND** 関数は例外を再送出せず、既存の `load_heat_list()` 結果を返す

### Requirement: CSV の読み込みとヒート単位へのグループ化
システムは、ローカル CSV (`config.HEAT_LIST_CSV`) を読み込み、ヒート番号 (列 index 3) をキーとしてヒート単位にグループ化 SHALL する。

#### Scenario: 正常な読み込み
- **WHEN** `load_heat_list()` が呼ばれ、CSV ファイルが存在する
- **THEN** 全行が読み込まれ、列 index 3 の値をキーとする辞書 `by_heat` が構築される
- **AND** ヒート番号 `1` から順に昇順で処理される
- **AND** 読み込み元はプロセスの CWD に依存しない

#### Scenario: 読み込み失敗
- **WHEN** CSV ファイルが存在しない、または読み込み中に例外が発生する
- **THEN** 例外は捕捉され、エラーログが記録される
- **AND** 関数はヘッダー行のみを含む配列を返す (ヘッダー内容は add-4wave-support の定義に従う)

### Requirement: 起動時の自動読み込み
サーバー起動時、システムは ASGI lifespan startup において `RaceManager.load_heat()` を呼び出し、既存のヒートリスト CSV を読み込 SHALL む。モジュール import 時の読み込みを SHALL NOT 行う。

#### Scenario: サーバー起動
- **WHEN** ASGI アプリケーションの lifespan startup が実行される
- **THEN** `race_manager.load_heat()` が実行される
- **AND** 読み込み失敗時も例外はサーバー起動を阻害しない

#### Scenario: モジュール import
- **WHEN** `droras.server` モジュールが import される (lifespan 未実行)
- **THEN** ヒートリストの読み込み・Firestore 接続などの副作用は発生しない
