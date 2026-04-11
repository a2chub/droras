## ADDED Requirements

### Requirement: カレントヒート状態の保持
システムは 1-based のカレントヒート index (`current_heat_index`) を保持 SHALL し、初期値は 1 とする。

#### Scenario: サーバー起動直後
- **WHEN** サーバープロセスが起動直後である
- **THEN** `RaceManager.current_heat_index == 1` である
- **AND** 任意のクライアントが後続の `set_current_heat` を送るまでこの値が維持される

### Requirement: Socket.IO 経由のカレントヒート変更
クライアントは Socket.IO `set_current_heat` イベントに整数 (または整数化可能な値) を渡してカレントヒートを変更 SHALL できる。

#### Scenario: クライアントがヒートを切り替える
- **WHEN** クライアントが `set_current_heat` イベントと整数値 `N` を emit する
- **THEN** `RaceManager.current_heat_index` が `int(N)` に更新される
- **AND** サーバーは全接続クライアントに `current_heat` イベントで `N` を emit する

### Requirement: HTTP パスによるカレントヒート変更
システムは HTTP `GET /{heat_index}` を受けると、カレントヒートを `heat_index` に変更し、その後 `index.html` を返 SHALL す。

#### Scenario: HTTP 経由での直接指定
- **WHEN** クライアントが `GET /5` を要求する
- **THEN** `RaceManager.set_current_heat(5)` が呼び出される
- **AND** レスポンスとして `static/index.html` が返される

### Requirement: カレントパイロットの HTTP 参照
システムは HTTP `GET /current_pilots` にてカレントヒートのパイロット名の配列を JSON で返 SHALL す。

#### Scenario: カレントパイロット取得
- **WHEN** クライアントが `GET /current_pilots` を要求する
- **THEN** レスポンスはカレントヒート行を `","` で分割した文字列配列である
- **AND** `Content-Type: application/json` で返される

### Requirement: ヒート変更のログ記録
システムは、カレントヒートが変更されるたびに event-logging capability 経由で変更を記録 SHALL する。

#### Scenario: set_current_heat 呼び出し時
- **WHEN** `RaceManager.set_current_heat(heat_index)` が呼ばれる
- **THEN** `event_logger.log_heat_change(heat_index, current_pilots)` が呼び出される

### Requirement: ヒート変更の Firestore 反映
システムは、カレントヒート変更時に firestore-sync capability 経由で非同期に外部公開 SHALL する。

#### Scenario: set_current_heat 呼び出し時
- **WHEN** `RaceManager.set_current_heat(heat_index)` が呼ばれる
- **THEN** `asyncio.create_task(self.update_current_heat_on_firestore(str(heat_index)))` が発行される
- **AND** Firestore 更新の成功/失敗はサーバー本体の処理を阻害しない

### Requirement: set_current_heat の戻り値
`RaceManager.set_current_heat(heat_index)` は `{"heat_id": heat_index}` を SHALL 返す。

#### Scenario: 戻り値の形式
- **WHEN** `set_current_heat(3)` が呼ばれる
- **THEN** 戻り値は `{"heat_id": 3}` である
