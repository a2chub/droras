## MODIFIED Requirements

### Requirement: Socket.IO 経由のカレントヒート変更
クライアントは Socket.IO `set_current_heat` イベントに整数 (または整数化可能な値) を渡してカレントヒートを変更 SHALL できる。指定値がヒートリストの有効範囲 (`1 <= N < len(all_heat_list)`) 外の場合、システムは状態を SHALL NOT 変更せず、WARNING ログを記録 SHALL する。

#### Scenario: クライアントがヒートを切り替える
- **WHEN** クライアントが `set_current_heat` イベントと有効範囲内の整数値 `N` を emit する
- **THEN** `RaceManager.current_heat_index` が `int(N)` に更新される
- **AND** サーバーは全接続クライアントに `current_heat` イベントで `N` を emit する

#### Scenario: 範囲外のヒート指定
- **WHEN** クライアントが範囲外の値 (例: ヒートリストが空、または件数を超える index) を emit する
- **THEN** `current_heat_index` は変更されない
- **AND** WARNING ログが記録される
- **AND** ヒート変更のイベントログ・Firestore 更新は発行されない
- **AND** サーバーは変更前の現在値を `current_heat` イベントで emit する (クライアント表示を実状態に同期)

### Requirement: set_current_heat の戻り値
`RaceManager.set_current_heat(heat_index)` は、変更が受理された場合は `{"heat_id": heat_index}` を、範囲外で拒否された場合は変更されなかった現在値 `{"heat_id": current_heat_index}` を SHALL 返す。

#### Scenario: 受理時の戻り値
- **WHEN** 有効範囲内で `set_current_heat(3)` が呼ばれる
- **THEN** 戻り値は `{"heat_id": 3}` である

#### Scenario: 拒否時の戻り値
- **WHEN** 現在値が 2 の状態で範囲外の `set_current_heat(99)` が呼ばれる
- **THEN** 戻り値は `{"heat_id": 2}` である

### Requirement: カレントパイロットの HTTP 参照
システムは HTTP `GET /current_pilots` にてカレントヒートのパイロット名の配列を JSON で返 SHALL す。ヒートリストが空、またはカレントヒートが範囲外の場合でも 500 エラーを SHALL NOT 返す。

#### Scenario: カレントパイロット取得
- **WHEN** クライアントが `GET /current_pilots` を要求する
- **THEN** レスポンスはカレントヒート行を `","` で分割した文字列配列である
- **AND** `Content-Type: application/json` で返される

#### Scenario: ヒートリスト未読み込み時
- **WHEN** ヒートリストが空 (またはヘッダーのみ) の状態で `GET /current_pilots` を要求する
- **THEN** HTTP 200 で空相当の配列 (`get_heat_pilots` の `""` を split した結果) が返される
- **AND** 500 エラーにはならない

### Requirement: HTTP パスによるカレントヒート変更
システムは HTTP `GET /{heat_index}` を受けると、カレントヒートを `heat_index` に変更し、その後 `index.html` を返 SHALL す。範囲外の `heat_index` は `set_current_heat` の範囲ガードにより無視され、`index.html` の返却は SHALL 継続する。

#### Scenario: HTTP 経由での直接指定
- **WHEN** クライアントが `GET /5` を要求する (5 は有効範囲内)
- **THEN** `RaceManager.set_current_heat(5)` が呼び出される
- **AND** レスポンスとして `static/index.html` が返される

#### Scenario: 範囲外パスの指定
- **WHEN** クライアントが範囲外の `GET /999` を要求する
- **THEN** カレントヒートは変更されず WARNING ログが記録される
- **AND** レスポンスとして `static/index.html` が返される (エラー画面にしない)
