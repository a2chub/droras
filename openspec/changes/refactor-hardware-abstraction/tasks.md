## 1. config / 依存関係の基盤整備

- [x] 1.1 `src/droras/config.py` に `SOUND_DIR` (= `BASE_DIR/sound`) と `HEAT_LIST_CSV` (= `LOG_DIR/heat_list.csv`) を追加
- [x] 1.2 `pyproject.toml` の `rpi-gpio` 依存に `; sys_platform == 'linux'` マーカーを付与
- [ ] 1.3 `rye sync` (macOS) が成功することを確認し、lock ファイルの差分が `rpi-gpio` マーカー以外に意図しない変更を含まないことをレビュー

## 2. hardware パッケージの新設 (HAL)

- [x] 2.1 `src/droras/hardware/base.py`: `StartSignal` (`on()` / `off()`) と `AudioPlayer` (`play(sound_name)`) の Protocol を定義
- [x] 2.2 `src/droras/hardware/null.py`: `NullStartSignal` / `NullAudioPlayer` (操作内容を INFO ログのみ、例外なし)
- [x] 2.3 `src/droras/hardware/gpio.py`: `GpioStartSignal` (GPIO 26)。gpiozero の import はクラス初期化内で遅延
- [x] 2.4 `src/droras/hardware/audio.py`: `PygameAudioPlayer`。pygame の import / `mixer.init()` は初期化内で遅延。音源は `config.SOUND_DIR` 配下の絶対パスで解決
- [x] 2.5 `src/droras/hardware/__init__.py`: `create_start_signal()` (DRORAS_GPIO=auto/on/off/mock の選択ロジック、auto 失敗時 WARNING + Null フォールバック、on 失敗時は例外送出) と `create_audio_player()` (mixer init 試行 → 失敗時 WARNING + Null) を実装
- [x] 2.6 `src/droras/hardware/__main__.py`: ファクトリでデバイス生成しスタートシーケンスを 1 回実行する手動テストエントリ
- [x] 2.7 GPIO 不在環境で `python -c "import droras.hardware, droras.hardware.gpio, droras.hardware.audio, droras.hardware.null"` が副作用なく成功することを確認

## 3. スタートシーケンスの移設

- [x] 3.1 スタートシーケンス関数 (シグナル ON → pipipi 再生 → `randint(30,50)/10.0` 秒遅延 → po-n 再生 → 0.35 秒 → シグナル OFF) を `StartSignal` / `AudioPlayer` を引数に取る同期関数として実装 (タイミング値・順序は現行 `device.py` と同一)
- [x] 3.2 `src/droras/device.py` を削除し、デッドコード (`isPlayable` / `PLAY_FLG` / `if True:` / コメントアウト GPIO 行 / `get_resource_path`) を持ち込まないことを確認
- [ ] 3.3 macOS で `python -m droras.hardware` を実行し、音声が実再生され、シグナルが Null ログになることを確認 (PygameAudioPlayer の初期化・play() 実行は SDL dummy ドライバで検証済み。スピーカーからの実音再生のみ未確認 — 開発者の耳で1回流すだけで完了)

## 4. RaceManager の改修

- [x] 4.1 `RaceManager.__init__` を `(start_signal, audio_player)` のコンストラクタ注入に変更し、`count_down()` の platform 分岐 + 遅延 import を削除
- [x] 4.2 `start()` を非ブロッキング化: シーケンス本体を `asyncio.to_thread()` で実行し、実行中フラグによる二重スタートガード (実行中は WARNING ログ + 無視、完了/エラー時は try/finally で必ず解放) を実装
- [x] 4.3 `start()` の `current_pilots` 未定義変数バグを修正 (事前に空文字列で初期化)。エラー時は `log_heat_error` → `log_heat_start` の順で記録 (現行挙動維持)
- [x] 4.4 `connect_to_firestore()` / `load_heat()` の裸 `except:` を `Exception` 捕捉 + `exc_info` 付きログに置換 (グレースフル継続は維持)

## 5. server / convert_heatlist の改修

- [x] 5.1 `server.py`: モジュールレベルの `race_manager = RaceManager()` と `race_manager.load_heat()` を FastAPI lifespan (startup) に移行。lifespan 内でファクトリからデバイス生成 → `RaceManager` 生成 → `load_heat()` の順に実行
- [x] 5.2 `start_heat` ハンドラを async 化し、非ブロッキングの `race_manager.start()` を呼び出す形に変更
- [x] 5.3 `upload_log` の裸 `except:` を `OSError` / `subprocess.SubprocessError` 捕捉 + `exc_info` 付きログに置換 (False 返却は維持)
- [x] 5.4 `convert_heatlist.py` の `"log/heat_list.csv"` (2 箇所) を `config.HEAT_LIST_CSV` に置換
- [x] 5.5 重複定義されている route 関数名 `index` (`GET /` と `GET /{heat_index}`) の後者をリネーム (ルーティング挙動は不変)

## 6. ドキュメント / 運用ファイル

- [x] 6.1 `droras.service.example` に `Environment=DRORAS_GPIO=on` (推奨設定) をコメント付きで追記
- [x] 6.2 README に `DRORAS_GPIO` の説明 (auto/on/off/mock) と macOS 開発手順 (rye sync が通ること、音声実再生) を追記

## 7. 検証

- [x] 7.1 macOS: `run.sh` でサーバー起動 → import 時副作用なし・lifespan で heat 読み込み・Firestore 接続失敗時もグレースフル継続を確認
- [x] 7.2 macOS: Socket.IO 経由で `start_heat` を発火し、(a) 音声が再生される、(b) シーケンス中も他イベント (`set_current_heat` 等) が応答する、(c) 連打時に WARNING ログで無視される、を確認
- [x] 7.3 macOS: `reload_heat_list` / `download_heat_list` / `current_pilots` が CWD によらず動作することを確認 (リポジトリ外 CWD から起動して検証。`download_heat_list` の GAS 実呼び出しのみ未実施 — 保存先は同一の `config.HEAT_LIST_CSV` 定数のためパス面のリスクなし)
- [x] 7.4 `openspec validate refactor-hardware-abstraction --strict` がエラーなく通ることを確認
- [ ] 7.5 RasPi 実機: `DRORAS_GPIO` 未設定 (auto) でデプロイし、LED・音・タイミングが従来と同等であることを確認 (実機作業、デプロイ時に実施)

## 8. テストスイート (Phase 3 前倒し)

- [x] 8.1 pytest 基盤導入: `[tool.rye] dev-dependencies` に pytest/httpx 追加、`[tool.pytest.ini_options]` 設定 (pytest-asyncio 不使用、async は `asyncio.run` で実行。lock は未再生成 — .venv へは uv で直接インストール)
- [x] 8.2 `tests/` 作成 (31 テスト、全パス・0.5 秒): ファクトリ選択 (off/mock/auto フォールバック/on 例外伝播/不正値)、import 副作用なし、シーケンス順序とタイミング (sleep/randint モック)、RaceManager (二重スタートガード/例外時のガード解放/エラー経路のログ順序/Firestore 文字列書き込み)、heatlist (実運用フォーマット = ヘッダー行付き CSV での全件読み込み/ファイル不在/CWD 非依存)、サーバー lifespan 統合 (TestClient)
- [x] 8.3 データ形式の前提を documenting test として固定: GAS 出力 CSV のヘッダー行が `range(1, len(by_heat))` の成立条件であり、ヘッダー無し CSV では最終ヒートが落ちる (GAS 側の出力形式変更を検知するための番犬テスト)
