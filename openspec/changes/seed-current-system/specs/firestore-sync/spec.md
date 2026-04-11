## ADDED Requirements

### Requirement: Firestore クライアントの確立
サーバー起動時、システムは Google Cloud Firestore に接続し、`race/current` ドキュメントへの参照を SHALL 保持する。

#### Scenario: 接続成功
- **WHEN** `RaceManager.__init__` が呼ばれる
- **THEN** `google.cloud.firestore.AsyncClient()` が生成される
- **AND** `db.collection("race").document("current")` が `self.race_ref` に保持される
- **AND** `Successfully connected to Firestore` ログが記録される

#### Scenario: 接続失敗時のグレースフル継続
- **WHEN** `AsyncClient()` の生成または collection/document 取得中に例外が発生する
- **THEN** 例外は捕捉され、`self.race_ref` は `None` となる
- **AND** `Failed to connect to Firestore` エラーログが記録される
- **AND** サーバー本体の起動は継続する

### Requirement: 認証キーの読み込み
Firestore 接続は、`run.sh` と同じディレクトリに配置された `jdl-main-key.json` を資格情報として SHALL 利用する。

#### Scenario: 認証キーの参照
- **WHEN** サーバーが起動する
- **THEN** `GOOGLE_APPLICATION_CREDENTIALS` 相当の環境変数または `jdl-main-key.json` が `AsyncClient` に参照される
- **AND** 認証情報の解決は外部 (systemd unit もしくは実行環境) の責務である

### Requirement: カレントヒートの非同期更新
カレントヒートの変更時、システムは `race/current` ドキュメントの `heat` フィールドを非同期で SHALL 更新する。

#### Scenario: 更新トリガー
- **WHEN** `RaceManager.set_current_heat(heat_index)` が呼ばれる
- **THEN** `asyncio.create_task(self.update_current_heat_on_firestore(str(heat_index)))` が発行される
- **AND** メインのハンドラ処理は Firestore 更新完了を待たずに継続する

#### Scenario: Firestore 書き込み成功
- **WHEN** `await self.race_ref.set({"heat": heat_id})` が成功する
- **THEN** `Heat {heat_id} successfully updated on Firestore` ログが記録される

#### Scenario: Firestore 書き込み失敗
- **WHEN** `await self.race_ref.set(...)` が例外を投げる
- **THEN** 例外は捕捉され、`Failed to update heat {heat_id} on Firestore: {e}` エラーログが記録される
- **AND** 例外はサーバー本体に伝播しない

### Requirement: heat フィールドの文字列化
Firestore に書き込まれる `heat` フィールドは整数ではなく文字列 SHALL とする。

#### Scenario: データ型
- **WHEN** `update_current_heat_on_firestore(heat_id)` が `race_ref.set` を呼ぶ
- **THEN** 第一引数は `{"heat": heat_id}` であり、`heat_id` は `str(heat_index)` による文字列である

### Requirement: 外部連携先との整合性
Firestore の `race/current.heat` は外部サイト (`https://info.japandroneleague.com/`) と同期する契約を SHALL 維持する。

#### Scenario: 外部同期契約
- **WHEN** カレントヒートが変更される
- **THEN** `race/current.heat` は変更後の値で更新される
- **AND** 当該外部サイトは同ドキュメントを購読してヒート番号を表示する (外部契約)
