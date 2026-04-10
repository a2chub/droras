## ADDED Requirements

### Requirement: GAS URL からの CSV ダウンロード
システムは、設定された Google Apps Script URL (`convert_heatlist.url`) から HTTP GET で CSV データを取得 SHALL し、ローカルの `log/heat_list.csv` に保存する。

#### Scenario: ダウンロード成功
- **WHEN** `download_heat_list()` が呼ばれ、レスポンスステータスが 200 である
- **THEN** レスポンス body が `log/heat_list.csv` にバイナリ書き込みされる
- **AND** 成功ログが記録される

#### Scenario: 非 200 ステータス
- **WHEN** レスポンスステータスが 200 以外である
- **THEN** ファイル書き込みは行われない
- **AND** `Failed to download heat list. status code: {code}` のエラーログが記録される

#### Scenario: HTTP リクエスト例外
- **WHEN** `requests.exceptions.RequestException` が発生する
- **THEN** 例外は捕捉され、エラーログが記録される
- **AND** 関数は例外を再送出せず、既存の `load_heat_list()` 結果を返す

### Requirement: HTTP リトライとタイムアウト
ダウンロードはネットワーク瞬断に耐えるため、リトライおよびタイムアウトを SHALL 設定する。

#### Scenario: リトライ戦略
- **WHEN** `download_heat_list()` が HTTP リクエストを行う
- **THEN** `Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])` が適用される
- **AND** タイムアウトは `(connect=10秒, read=30秒)` である

### Requirement: CSV の読み込みとヒート単位へのグループ化
システムは、ローカル CSV (`log/heat_list.csv`) を読み込み、ヒート番号 (列 index 3) をキーとしてヒート単位にグループ化 SHALL する。

#### Scenario: 正常な読み込み
- **WHEN** `load_heat_list()` が呼ばれ、CSV ファイルが存在する
- **THEN** 全行が読み込まれ、列 index 3 の値をキーとする辞書 `by_heat` が構築される
- **AND** ヒート番号 `1` から順に昇順で処理される

#### Scenario: 読み込み失敗
- **WHEN** CSV ファイルが存在しない、または読み込み中に例外が発生する
- **THEN** 例外は捕捉され、エラーログが記録される
- **AND** 関数はヘッダー行のみを含む `[["E1", "F1", "F4", "HeatNo"]]` を返す

### Requirement: ヒート行の正規化フォーマット
各ヒート行は `[pilot1, pilot2, pilot3, heat_number, class_name]` の順で SHALL 構築する。

#### Scenario: ヒート行の構築
- **WHEN** ヒート番号 `i` に対応する行群 `pilots` が存在する
- **THEN** 各 `pilots[ii][1]` (パイロット名) が順に配列に追加される
- **AND** 続けてヒート番号 `i` が追加される
- **AND** 続けて `pilots[0][2]` (class 名) が追加される

### Requirement: 固定ヘッダーの先頭行
返却される配列の先頭行は、固定のラベル行 `["E1", "F1", "F4", "HeatNo"]` で SHALL ある。

#### Scenario: ヘッダー行の存在
- **WHEN** `load_heat_list()` が結果を返す
- **THEN** 結果の index 0 は常に `["E1", "F1", "F4", "HeatNo"]` である
- **AND** この行はクライアント送信時 (realtime-sync) に除外される前提で維持される

### Requirement: カレントヒートからのパイロット文字列取得
システムは `get_heat_pilots(heat_id, all_heat_list)` で指定ヒートの行要素を `","` 区切り文字列として SHALL 返す。

#### Scenario: 正常取得
- **WHEN** `all_heat_list` が空でなく、`heat_id` が範囲内である
- **THEN** `all_heat_list[heat_id]` の各要素を文字列化して `","` で join した結果を返す

#### Scenario: 空リスト
- **WHEN** `all_heat_list` が空 (`len < 1`) である
- **THEN** 空文字列 `""` を返す

### Requirement: 起動時の自動読み込み
サーバー起動時、システムは `RaceManager.load_heat()` を呼び出し、既存の `log/heat_list.csv` を読み込 SHALL む。

#### Scenario: サーバー起動
- **WHEN** `server` モジュールの import 完了直後
- **THEN** `race_manager.load_heat()` が実行される
- **AND** 読み込み失敗時も例外はサーバー起動を阻害しない
