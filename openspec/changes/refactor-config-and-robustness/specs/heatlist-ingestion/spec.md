## MODIFIED Requirements

### Requirement: GAS URL からの CSV ダウンロード
システムは、`settings.gas_url` (環境変数 `DRORAS_GAS_URL` で上書き可能、デフォルトは従来の Google Apps Script URL) から HTTP GET で CSV データを取得 SHALL し、`config.HEAT_LIST_CSV` (= `config.LOG_DIR` 配下の `heat_list.csv` 絶対パス) に保存する。

#### Scenario: ダウンロード成功
- **WHEN** `download_heat_list()` が呼ばれ、レスポンスステータスが 200 である
- **THEN** レスポンス body が `config.HEAT_LIST_CSV` にバイナリ書き込みされる
- **AND** 成功ログが記録される
- **AND** 保存先はプロセスの CWD に依存しない

#### Scenario: URL の設定上書き
- **WHEN** `DRORAS_GAS_URL` が設定された状態で `download_heat_list()` が呼ばれる
- **THEN** 設定された URL に対して HTTP GET が行われる

#### Scenario: 非 200 ステータス
- **WHEN** レスポンスステータスが 200 以外である
- **THEN** ファイル書き込みは行われない
- **AND** `Failed to download heat list. status code: {code}` のエラーログが記録される

#### Scenario: HTTP リクエスト例外
- **WHEN** `requests.exceptions.RequestException` が発生する
- **THEN** 例外は捕捉され、エラーログが記録される
- **AND** 関数は例外を再送出せず、既存の `load_heat_list()` 結果を返す

### Requirement: カレントヒートからのパイロット文字列取得
システムは `get_heat_pilots(heat_id, all_heat_list)` で指定ヒートの行要素を `","` 区切り文字列として SHALL 返す。`heat_id` が有効範囲 (`1 <= heat_id < len(all_heat_list)`) 外の場合は、例外を送出せず空文字列 `""` を SHALL 返す。

#### Scenario: 正常取得
- **WHEN** `all_heat_list` が空でなく、`heat_id` が範囲内である
- **THEN** `all_heat_list[heat_id]` の各要素を文字列化して `","` で join した結果を返す

#### Scenario: 空リスト
- **WHEN** `all_heat_list` が空 (`len < 1`) である
- **THEN** 空文字列 `""` を返す

#### Scenario: 範囲外の heat_id
- **WHEN** `all_heat_list` がヘッダー行のみ (またはヒート数より大きい `heat_id` / `heat_id < 1`) である
- **THEN** IndexError を送出せず空文字列 `""` を返す

## ADDED Requirements

### Requirement: 起動時のネットワークアクセス不実施
サーバー起動処理 (`__main__.main()` および lifespan startup) は、GAS への CSV ダウンロードを SHALL NOT 実行する。起動時はローカルの `config.HEAT_LIST_CSV` の読み込みのみを行い、ダウンロードはオペレーター操作 (Socket.IO `download_heat_list` イベント) によってのみ SHALL 実行される。

#### Scenario: ネットワーク不通環境での起動
- **WHEN** インターネット接続のない現地環境でサーバーを起動する
- **THEN** 起動はネットワークタイムアウトを待たず完了する
- **AND** 既存のローカル CSV があればヒートリストが読み込まれる

#### Scenario: 最新リストの取得
- **WHEN** オペレーターが UI から `download_heat_list` イベントを発火する
- **THEN** GAS からのダウンロードと再読み込みが実行される (従来挙動)
