## ADDED Requirements

### Requirement: Socket.IO サーバーの提供
システムは、ASGI アプリケーションとして Socket.IO サーバーを SHALL 提供する。

#### Scenario: Socket.IO サーバーの初期化
- **WHEN** サーバープロセスが起動する
- **THEN** `socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")` が初期化される
- **AND** `socketio.ASGIApp` が `static_files={"/": config.STATIC_DIR}` とともに生成される
- **AND** `app.mount("/", sio_app)` により FastAPI 配下にマウントされる

### Requirement: 接続時の初期状態送信
システムは、クライアントが接続した際、その caller にのみ現在のヒートリストとカレントヒート index を SHALL 送信する。

#### Scenario: 新規クライアント接続
- **WHEN** クライアントが Socket.IO に接続する
- **THEN** サーバーは `heat_list` イベントを `room=sid` で emit する
- **AND** 送信内容は `race_manager.all_heat_list[1:]` (ヘッダー行を除外したリスト) である
- **AND** 続けて `current_heat` イベントを `room=sid` で `race_manager.current_heat_index` とともに emit する
- **AND** `Connected: {sid}` のログが記録される

### Requirement: 切断ログ
クライアント切断時、システムは切断イベントをログに SHALL 記録する。

#### Scenario: クライアント切断
- **WHEN** クライアントの Socket.IO 接続が切断される
- **THEN** `Disconnect: {sid}` のログが記録される

### Requirement: ヒート変更のブロードキャスト
`set_current_heat` イベント処理後、システムは全クライアントに更新後のカレントヒートを SHALL 通知する。

#### Scenario: ヒート変更時の通知
- **WHEN** クライアントが `set_current_heat` イベントに整数 `N` を送信する
- **THEN** サーバーは `race_manager.set_current_heat(int(N))` を呼び出す
- **AND** 続けて `current_heat` イベントを `N` とともに全クライアントへ broadcast する (room 指定なし)

### Requirement: ヒートリストのリロード
クライアントは `reload_heat_list` イベントで、既存の `log/heat_list.csv` からヒートリストを再読み込みさせる SHALL ことができる。

#### Scenario: ヒートリスト再読み込み
- **WHEN** クライアントが `reload_heat_list` イベントを送信する
- **THEN** `race_manager.load_heat()` が呼ばれる
- **AND** 成功時 `heat_list` イベントが全クライアントに broadcast される (payload は `all_heat_list[1:]`)
- **AND** `Heat list reloaded` ログが記録される
- **AND** ack callback 経由で `True` が返される

### Requirement: ヒートリストの再ダウンロード
クライアントは `download_heat_list` イベントで、GAS URL から CSV を再取得させる SHALL ことができる。

#### Scenario: ヒートリスト再ダウンロード
- **WHEN** クライアントが `download_heat_list` イベントを送信する
- **THEN** `convert_heatlist.download_heat_list()` が呼ばれる
- **AND** 成功時 `heat_list` イベントが全クライアントに broadcast される (payload は `race_manager.all_heat_list[1:]`)
- **AND** ダウンロード開始・完了のログが記録される
- **AND** ack callback 経由で `True` が返される

### Requirement: ログのアップロード
クライアントは `upload_log` イベントで、サーバー上の `0_log_upload.sh` スクリプトを実行させる SHALL ことができる。

#### Scenario: アップロード成功
- **WHEN** クライアントが `upload_log` イベントを送信する
- **THEN** サーバーは `BASE_DIR/0_log_upload.sh` を `subprocess.call(..., shell=True)` で実行する
- **AND** ack callback 経由で `True` が返される

#### Scenario: アップロード失敗
- **WHEN** `subprocess.call` が例外を投げる
- **THEN** 例外は捕捉され、エラーログが記録される
- **AND** ack callback 経由で `False` が返される

### Requirement: CORS とトランスポート
サーバーは CORS を全許容し、Socket.IO のトランスポートとして WebSocket を SHALL 受け入れる。

#### Scenario: CORS 設定
- **WHEN** FastAPI アプリが初期化される
- **THEN** `CORSMiddleware` が `allow_origins=["*"]`, `allow_credentials=True`, `allow_methods=["*"]`, `allow_headers=["*"]` で追加される
- **AND** Socket.IO は `cors_allowed_origins="*"` で初期化される

### Requirement: 送信されるヒートリストの形式
クライアントに送信される `heat_list` の各行は、ヘッダー行を除いた二次元配列である SHALL 。

#### Scenario: heat_list payload 形式
- **WHEN** `heat_list` イベントが emit される
- **THEN** payload は `race_manager.all_heat_list[1:]` (固定ヘッダー `["E1", "F1", "F4", "HeatNo"]` を除外したリスト) である
- **AND** 各行は `[pilot1, pilot2, pilot3, heat_number, class_name]` 形式である
