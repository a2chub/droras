## Context

Phase 1+2 (`refactor-hardware-abstraction`) で HAL 導入・非ブロッキング化・lifespan 移行・テストスイート (31 件) が完了。本 change は Phase 3 として保守性・運用性を仕上げる。

現状の残課題:

- GAS URL が `convert_heatlist.py` にハードコード (README にも「環境変数にしたほうがいいかも」と注記あり)。ポート 8000 は `__main__.py` に、GPIO ピン 26 は `hardware/gpio.py` のデフォルト引数にハードコード
- ヒートリストが空/短いとき: `get_heat_pilots()` が IndexError → `GET /current_pilots` が 500、`set_current_heat()` は index 更新後に例外で中断し「index は変わったがログ・Firestore 未反映」の不整合になる (Phase 1+2 の E2E とテストで観測)
- `event_logger.py` は import しただけで `TimedRotatingFileHandler` を生成。`__init__.py` は import 時に root logger を basicConfig する
- `__main__.py` が起動のたびに GAS へダウンロードに行く (現地のネットワーク不通時に起動が遅延する。lifespan でのローカル CSV 読み込みと二重)
- rye は上流が開発終了 (uv への移行が公式推奨)。Phase 1+2 で macOS に rye が無く lock 再生成ができなかった。開発検証はすでに uv で行っている
- テストは `pytest` 31 件あるが CI なし

## Goals / Non-Goals

**Goals:**

- 大会ごとに変わり得る値 (GAS URL) と環境ごとに変わり得る値 (ポート、GPIO ピン) を環境変数で設定可能にする。未設定なら従来と完全に同一動作
- ヒートリストの状態によらずサーバーが 500 や不整合状態にならない (範囲外アクセスの安全化)
- `import droras` および全サブモジュールの import を副作用ゼロにする (Phase 1+2 の「import 副作用の禁止」をパッケージ全体に拡張)
- 開発機 (macOS) と RasPi の両方で同一ツール (uv) により再現可能な依存管理を行う
- push/PR ごとに macOS / Linux 両環境でテストと lint が自動実行される

**Non-Goals:**

- スタートシーケンスのタイミング定数の設定化 (レース規定値。固定のまま)
- `GET /{heat_index}` ルートの廃止・メソッド変更 (互換維持)
- フロントエンドのビルド・配信方法の変更
- デプロイ自動化 (CD)。CI はテスト・lint まで

## Decisions

### D1. 設定は pydantic-settings の Settings クラスに一元化

`config.py` に `Settings(BaseSettings)` を定義し、環境変数プレフィックス `DRORAS_` で上書き可能にする:

| 設定 | 環境変数 | デフォルト |
|------|----------|-----------|
| `gas_url` | `DRORAS_GAS_URL` | 現行ハードコードの GAS URL |
| `port` | `DRORAS_PORT` | `8000` |
| `gpio_pin` | `DRORAS_GPIO_PIN` | `26` |

- 既存の `DRORAS_GPIO` (auto/on/off/mock) も Settings に取り込む (`gpio_mode`)。読み取りは現行どおりファクトリ呼び出し時に行い、挙動は不変
- パス定数 (`BASE_DIR` / `STATIC_DIR` / `LOG_DIR` / `SOUND_DIR` / `HEAT_LIST_CSV`) は導出値のためモジュール定数のまま維持 (既存テスト・モジュールの `config.HEAT_LIST_CSV` 参照を壊さない)
- インスタンスはモジュールレベルの `settings = Settings()` を一つ公開。テストは `monkeypatch.setenv` + 再生成、または属性 patch で差し替え
- `.env` ファイル読み込みを有効化 (`run.sh` と同階層)。systemd では従来通り `Environment=` でも設定可能

代替案: stdlib のみ (`os.environ.get` + dataclass)。依存は増えないが、型変換・バリデーション・`.env` 対応を自前実装することになる。pydantic は FastAPI 経由で既にインストール済みであり、pydantic-settings の追加コストは小さいため採用。

### D2. 範囲外ヒートアクセスは「安全に無視」で統一

- `get_heat_pilots(heat_id, all_heat_list)`: `heat_id` が `1 <= heat_id < len(all_heat_list)` を満たさない場合は `""` を返す (空リスト時の既存挙動 `""` と一貫)
- `RaceManager.set_current_heat(heat_index)`: 範囲外なら WARNING ログを出し、**状態を一切変更せず** 現在値のまま `{"heat_id": current_heat_index}` を返す。範囲内なら現行どおり (index 更新 → change ログ → Firestore タスク)
- `server.set_current_heat` ハンドラの `current_heat` broadcast は `RaceManager` の戻り値の `heat_id` を emit する (拒否時に誤った値を全クライアントへ配らない)
- ヒートリスト再読み込みで件数が減り `current_heat_index` が範囲外に取り残された場合は、`get_heat_pilots` の安全化により 500 にはならない (index の自動補正はしない — オペレーターが画面で選び直す運用)

代替案: 範囲外は HTTP 4xx / Socket.IO エラー応答にする。フロントエンドのエラーハンドリング改修が必要になり、レース現場では「無視して続行」が最も安全なため見送り。

### D3. event_logger は遅延初期化、logging 設定はエントリーポイントへ

- `event_logger.py`: ハンドラ生成を `_get_logger()` (初回呼び出しで `TimedRotatingFileHandler` を構築しキャッシュ) に変更。`log_heat_start/change/error` の API・出力フォーマット・ローテーション・`namer` 規則は不変。`LOG_DIR` 作成もこのタイミングで保証する
- `droras/__init__.py`: `basicConfig` と LOG_DIR 作成を削除し、`setup_logging()` 関数として `config.py` (または専用モジュール) に移設。呼び出し箇所は `__main__.main()` と `server.py` の lifespan startup の 2 箇所 (uvicorn を直接起動された場合もログ設定が効くように。`basicConfig` は二重呼び出しでも no-op なので安全)
- 既存テストの `import droras` 副作用前提 (LOG_DIR 自動作成) が変わるため、テストの追従修正を行う

### D4. __main__ の起動時ダウンロード廃止

`__main__.main()` から `download_heat_list()` を削除。起動時は lifespan がローカル CSV を読む (Phase 1+2 で確立済み)。最新リストが必要なときはオペレーター UI の `download_heat_list` イベント (従来からある導線) を使う。`uvicorn.run` のポートは `settings.port`、`reload=True` は開発専用のため `DRORAS_RELOAD` (デフォルト false) に変更する — 本番 systemd で reload 監視プロセスが動く必要はない。

注意: 現行の本番は reload=True で動いているため、RasPi デプロイ時に挙動差 (ファイル監視プロセスの有無) を確認する。機能面の差はない。

### D5. rye → uv 移行

- `pyproject.toml`: `[tool.rye]` を削除し、dev 依存は `[dependency-groups]` (PEP 735, uv ネイティブ) に移行。`uv lock` で `uv.lock` を生成し、`requirements.lock` / `requirements-dev.lock` は削除
- `run.sh`: `.venv` 直接参照から `uv run python -m droras` ベースに変更 (uv が無い環境を考慮し、`.venv/bin/python` フォールバックは残す)
- README: rye のインストール手順を uv に全面置換
- RasPi 側手順: `curl -LsSf https://astral.sh/uv/install.sh | sh` → `uv sync`。Python 3.12 は uv が自動取得

代替案: rye 継続。上流終了済みで新規インストール手段も先細りのため不採.用。lock 無し運用 (pyproject のみ) は本番機材の再現性を損なうため不採用。

### D6. CI は GitHub Actions、macOS + Linux マトリクス

`.github/workflows/ci.yml`:

- トリガー: push / pull_request
- ジョブ: `uv sync` → `uv run pytest` を `ubuntu-latest` と `macos-latest` で実行 (GPIO 無し環境での auto フォールバックが両 OS で踏まれる)
- lint ジョブ: `uv run ruff check` + `uv run ruff format --check`
- ヘッドレス CI でも全テストが通ることは Phase 1+2 のテスト設計 (SDL dummy、実ハードウェア非依存) で担保済み

### D7. ruff 設定は最小限

`pyproject.toml` に `[tool.ruff]` を追加。line-length は既存コードに合わせ 110 程度、ルールはデフォルト (E/F) + isort (I) から開始し、過剰な厳格化はしない。既存コードの違反は本 change 内で修正する。

## Risks / Trade-offs

- [uv 移行で RasPi デプロイが変わり、現地で手順を間違える] → README の手順を uv 前提に全面書き換えし、`run.sh` にフォールバックを残す。移行後の初回デプロイは大会前の検証期間に実施する
- [reload=True 廃止による本番挙動差] → 機能差はないが、デプロイ時に systemd での起動・自動再起動を実機確認するタスクを設ける。開発時は `DRORAS_RELOAD=1` で従来体験を維持
- [`__init__.py` の logging 副作用削除で、想定外の起動経路 (直接 uvicorn 起動) のログが欠ける] → lifespan でも `setup_logging()` を呼ぶ二段構えにする
- [Settings 導入で既存テストの config 参照 (属性 patch) が壊れる] → パス定数はモジュール定数のまま残す方針で影響を最小化。テストは同 change 内で追従させ、CI で回帰を検知
- [範囲外ガードの「無視して続行」が、オペレーターに変更失敗を気づかせない] → サーバーは正しい現在値を `current_heat` で broadcast し直すため、画面表示は実状態と一致する (画面が変わらないこと自体がフィードバックになる)
- [uv.lock 生成時に依存バージョンが一斉更新される] → `uv lock` の結果を requirements.lock の既存バージョンと突き合わせ、メジャー更新があれば pin して挙動確認する

## Migration Plan

1. Phase 1+2 ブランチ上に積む (同一ブランチ運用)
2. macOS: `uv sync` → `uv run pytest` 全パス → `run.sh` 起動確認 (env 未設定でデフォルト値動作)
3. GitHub Actions が両 OS でグリーンになることを確認
4. RasPi: uv インストール → `uv sync` → systemd unit の起動確認 (`DRORAS_GPIO=on` 推奨設定とあわせて)
5. ロールバックは git revert + 旧 `requirements.lock` 復元で rye 運用に戻せる (rye が RasPi に残っている前提)

## Open Questions

- なし (タイミング定数の設定化は明示的に Non-Goal として確定)
