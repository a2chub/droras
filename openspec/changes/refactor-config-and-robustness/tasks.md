## 1. Settings 導入 (app-configuration)

- [ ] 1.1 `pydantic-settings` を本体依存に追加
- [ ] 1.2 `config.py` に `Settings(BaseSettings)` を実装: `gas_url` / `port` / `gpio_pin` / `gpio_mode`、env prefix `DRORAS_`、`.env` 読み込み対応 (注意: `gpio_mode` の環境変数名は既存互換のため `DRORAS_GPIO` — prefix 規則と異なるので alias 指定)。モジュールレベルで `settings = Settings()` を公開。パス定数 (`BASE_DIR` 等) は現状のモジュール定数のまま維持
- [ ] 1.3 `convert_heatlist.py` のハードコード URL を `settings.gas_url` 参照に変更 (デフォルト値として現行 URL を Settings 側へ移設。旧スプシ直接出力 URL のコメントも Settings 側に移す)
- [ ] 1.4 `hardware/__init__.py` / `hardware/gpio.py` のモード判定とピン番号を `settings.gpio_mode` / `settings.gpio_pin` 参照に変更 (挙動・フォールバック規則は不変)
- [ ] 1.5 `__main__.py` のポートを `settings.port` に変更

## 2. ヒート範囲ガード (heatlist-ingestion / heat-navigation)

- [ ] 2.1 `get_heat_pilots()`: `1 <= heat_id < len(all_heat_list)` の範囲外で `""` を返すガードを追加
- [ ] 2.2 `RaceManager.set_current_heat()`: 範囲外指定を WARNING ログ + 状態変更なしで拒否し、戻り値は常に実際の現在値 `{"heat_id": ...}` とする。受理時の処理 (change ログ → Firestore タスク) は不変
- [ ] 2.3 `server.set_current_heat` ハンドラ: `RaceManager` の戻り値の `heat_id` を `current_heat` として emit する (拒否時は変更前の値が配られる)
- [ ] 2.4 `GET /{heat_index}`: 範囲外でも 500 にせず `index.html` を返すことを確認 (2.2 のガードで自然に満たされるはず)

## 3. import 副作用の排除 (app-configuration / event-logging)

- [ ] 3.1 `event_logger.py`: ハンドラ生成を初回ログ呼び出し時の遅延初期化に変更 (`_get_logger()` でキャッシュ)。`LOG_DIR` 不在時は作成。フォーマット・ローテーション・`namer`・logger 名は不変
- [ ] 3.2 `setup_logging()` 関数を実装 (出力先・フォーマットは現行 `__init__.py` の basicConfig と同一。`LOG_DIR` 作成もここで保証)
- [ ] 3.3 `droras/__init__.py` から basicConfig と `os.makedirs` を削除 (import 副作用ゼロ化)
- [ ] 3.4 `__main__.main()` と `server.py` lifespan startup の両方から `setup_logging()` を呼ぶ
- [ ] 3.5 `python -c "import droras, droras.server, droras.event_logger"` で root logger 変更・ファイル生成・ディレクトリ作成が発生しないことを確認

## 4. __main__ の整理 (heatlist-ingestion)

- [ ] 4.1 `__main__.main()` から起動時 `download_heat_list()` を削除
- [ ] 4.2 `uvicorn.run` の `reload=True` を `DRORAS_RELOAD` (デフォルト false) 制御に変更し、README の開発手順に `DRORAS_RELOAD=1` を記載

## 5. uv 移行 (developer-tooling)

- [ ] 5.1 `pyproject.toml`: `[tool.rye]` を削除し、dev 依存 (pytest / httpx / ruff) を `[dependency-groups]` に移行
- [ ] 5.2 `uv lock` で `uv.lock` を生成し、旧 `requirements.lock` との主要依存バージョン差分をレビュー (メジャー更新があれば pin して動作確認)
- [ ] 5.3 `requirements.lock` / `requirements-dev.lock` を削除
- [ ] 5.4 `run.sh` を uv ベース (`uv run python -m droras`) に変更し、uv 不在時の `.venv/bin/python` フォールバックを実装
- [ ] 5.5 README のインストール手順を rye から uv に全面書き換え (RasPi での uv インストール手順含む)

## 6. CI / lint (developer-tooling)

- [ ] 6.1 `pyproject.toml` に `[tool.ruff]` 設定を追加 (line-length 110、ルールはデフォルト + isort)
- [ ] 6.2 `uv run ruff check --fix` + `uv run ruff format` で src/ と tests/ をクリーン化し、自動修正で挙動が変わらないことをテストで確認
- [ ] 6.3 `.github/workflows/ci.yml` を作成: push/PR トリガー、`ubuntu-latest` + `macos-latest` マトリクスで `uv sync` → `uv run pytest`、別ジョブで `ruff check` + `ruff format --check`
- [ ] 6.4 GitHub 上で両 OS の CI がグリーンになることを確認

## 7. テスト追従・追加

- [ ] 7.1 既存テストの追従: Settings 導入・`__init__.py` 副作用削除 (LOG_DIR 自動作成前提の箇所) による影響を修正
- [ ] 7.2 追加テスト — Settings: デフォルト値の互換性、環境変数上書き (`DRORAS_PORT` / `DRORAS_GAS_URL` / `DRORAS_GPIO_PIN`)、`.env` より環境変数優先
- [ ] 7.3 追加テスト — 範囲ガード: `get_heat_pilots` 範囲外 → `""`、`set_current_heat` 範囲外 → 状態不変 + WARNING + 現在値返却 + Firestore/イベントログ未発行、`/current_pilots` ヒートリスト空 → 200
- [ ] 7.4 追加テスト — event_logger: import 副作用なし、初回呼び出しでのハンドラ生成、出力フォーマット互換 (tmp_path の LOG_DIR に patch して実書き込み検証)
- [ ] 7.5 全テストが macOS ローカルで 2 回連続パスすることを確認

## 8. ドキュメント

- [ ] 8.1 README に環境変数一覧 (`DRORAS_GAS_URL` / `DRORAS_PORT` / `DRORAS_GPIO` / `DRORAS_GPIO_PIN` / `DRORAS_RELOAD`) と `.env` の説明を追記
- [ ] 8.2 `droras.service.example` に `Environment=` での設定例 (または `EnvironmentFile=` + `.env`) を追記

## 9. 検証

- [ ] 9.1 macOS: 環境変数なしで `run.sh` 起動 → ポート 8000・従来 GAS URL・GPIO auto フォールバックで従来同一動作
- [ ] 9.2 macOS: `DRORAS_PORT=9000` 等で上書き起動を確認。ネットワーク遮断状態でも起動が即時完了することを確認
- [ ] 9.3 ヒートリスト未配置で起動 → `/current_pilots` が 200、範囲外 `set_current_heat` が無視され画面が実状態と同期することを確認
- [ ] 9.4 `openspec validate refactor-config-and-robustness --strict` がエラーなく通ることを確認
- [ ] 9.5 RasPi 実機: uv インストール → `uv sync` → systemd unit 起動・自動再起動・LED/音の従来動作を確認 (実機作業、デプロイ時に実施)
