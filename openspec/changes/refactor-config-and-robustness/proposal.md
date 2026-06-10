## Why

Phase 1+2 (`refactor-hardware-abstraction`) でハードウェア抽象化と安定性修復が完了したが、保守性の課題が残っている: (1) GAS URL・ポート・GPIO ピン番号がコードにハードコードされ、大会ごと・環境ごとの変更がコード編集を要する。(2) ヒートリストが空/短い状態で範囲外ヒートを参照すると 500 エラーや状態不整合が起きる (Phase 1+2 の E2E 検証とテスト実装で実地に観測済み)。(3) `event_logger` と `__init__.py` の import 時副作用が残存しテストや再利用を妨げる。(4) 起動時に GAS への自動ダウンロードが走り、ネットワーク不通時の起動が遅い。(5) パッケージ管理の rye が上流で開発終了しており、開発機 (macOS) で lock 再生成が不可能なことが Phase 1+2 で顕在化した。(6) テストは整備されたが CI が無く、回帰検知が手動実行頼みである。

## What Changes

- 設定の一元化: pydantic-settings による `Settings` を導入し、GAS URL / サーバーポート / GPIO ピン番号を環境変数 (`DRORAS_*`) で上書き可能にする (デフォルト値は現行ハードコード値と同一)。スタートシーケンスのタイミング定数 (3.0〜5.0 秒、0.35 秒) はレース規定値のため設定化しない
- ヒート範囲ガード: `get_heat_pilots()` の範囲外 heat_id は空文字列を返す。`set_current_heat()` は範囲外指定を WARNING ログ付きで拒否し、状態を変更しない (現行は index 更新後に IndexError で中断し、ログ・Firestore 未反映の不整合状態になる)。`GET /current_pilots` はヒートリスト空でも 500 を返さない
- `event_logger` のハンドラ生成を import 時から初回利用時 (遅延初期化) に変更。ログ出力フォーマット・ローテーション・ファイル名規則は不変
- `droras/__init__.py` の logging 設定 (basicConfig) をエントリーポイント (`__main__.main()` および lifespan) に移動し、ライブラリとしての import を副作用ゼロにする
- `__main__.py` 起動時の GAS 自動ダウンロードを廃止 (lifespan のローカル CSV 読み込みは維持。ダウンロードは従来通りオペレーター UI の `download_heat_list` イベントから実行)。ポートを Settings から取得
- パッケージ管理を rye から uv に移行: `uv.lock` 生成、`run.sh` / README / `droras.service.example` の手順更新、`requirements*.lock` の扱いを整理 (**運用変更**: RasPi のデプロイ手順が `rye sync` → `uv sync` になる)
- CI 整備: GitHub Actions で push/PR 時に pytest (ubuntu + macos マトリクス) と ruff (lint + format check) を実行
- ruff を dev 依存に追加し、既存コードを lint クリーンにする

**対象外**: フロントエンド (`front/`) の変更、`GET /{heat_index}` ルート自体の廃止 (互換維持。範囲外値の安全化のみ行う)、Firestore 構造の変更、認証まわり。

## Capabilities

### New Capabilities

- `app-configuration`: 環境変数による設定の一元管理 (Settings)、デフォルト値の互換性保証、ログ設定のエントリーポイント初期化
- `developer-tooling`: uv によるパッケージ管理・lock 運用、CI (テスト + lint)、ruff 設定

### Modified Capabilities

- `heatlist-ingestion`: GAS URL を Settings から取得、`get_heat_pilots()` の範囲外安全化、起動時の自動ダウンロード不実施の明文化
- `heat-navigation`: `set_current_heat()` の範囲外ガード (拒否 + WARNING、状態不変)、`GET /current_pilots` の空リスト安全化
- `event-logging`: ハンドラ生成の遅延初期化 (import 副作用の排除)。フォーマット・ローテーション仕様は不変
- `hardware-abstraction`: GPIO ピン番号を Settings から取得 (デフォルト 26)

## Impact

- **コード**: `config.py` (Settings 化)、`convert_heatlist.py`、`race_manager.py`、`server.py`、`event_logger.py`、`__init__.py`、`__main__.py`、`hardware/__init__.py`、`pyproject.toml`、`run.sh`、`.github/workflows/` (新規)、`tests/` (追従)
- **依存関係**: `pydantic-settings` を追加 (pydantic 本体は FastAPI 経由で既存)。dev に `ruff` 追加。rye 関連設定 (`[tool.rye]`) を uv 設定に置換
- **運用**: RasPi デプロイ手順が変わる (uv のインストールと `uv sync`)。環境変数が未設定なら全デフォルト値で従来同一動作のため、設定ファイルなしでも移行可能。`run.sh` は uv 環境を参照するよう更新
- **挙動互換性**: Socket.IO イベント・HTTP API・ログ形式・Firestore 同期は不変。変わるのは (a) 範囲外ヒート指定がエラーでなく安全に無視される、(b) 起動時に GAS ダウンロードが走らない (起動が速く・ネットワーク非依存になる)、の 2 点
- **他 change との関係**: `refactor-hardware-abstraction` (Phase 1+2、実装済み・未 archive) の上に積む。`hardware-abstraction` の delta は同 change の spec を基準とする
