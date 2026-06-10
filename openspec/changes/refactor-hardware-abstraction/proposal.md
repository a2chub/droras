## Why

`droras.device` は import 時に `LED(26)` と pygame を初期化するため、GPIO のない macOS 開発環境ではクラッシュする。現在は `platform.system() != "Darwin"` という逆向きの判定で回避しているが、(1) Linux 開発機や CI では依然クラッシュする、(2) macOS では音声を含む全機能がスキップされ開発時テストが不可能、(3) スタートシーケンスが同期 `sleep` でイベントループを 3〜5 秒ブロックしサーバー全体が無応答になる、という安定性・開発体験の問題を抱えている。レース現場で使う機材として、本番 (RasPi) と開発 (macOS) の両環境で同一コードパスが安全に動作する構造に改修する。

## What Changes

- ハードウェア抽象化層 (HAL) を新設: GPIO シグナルと音声再生を Protocol で抽象化し、能力検出 + 環境変数 (`DRORAS_GPIO`) で実装を切り替える。GPIO 不在環境では Null 実装にフォールバックし、音声は GPIO と独立して macOS でも実再生する
- `device.py` を `hardware/` パッケージに再編。import 時のハードウェア初期化 (LED 実体化・pygame init) を撤廃し、ファクトリ経由の遅延初期化に変更
- スタートシーケンスを非ブロッキング化 (`asyncio.to_thread`)。実行中の二重スタートはガードで抑止 (従来は連打防止なし)
- `RaceManager.start()` の未定義変数バグ (`current_pilots` が except 節で未代入参照) を修正
- 裸の `except:` を全廃し、具体的な例外型の捕捉 + 原因ログに置換
- CWD 依存の相対パス (`log/heat_list.csv`, 音源パス) を `config` 経由の絶対パスに統一
- import 時副作用 (`server.py` の `load_heat()`、`RaceManager` 生成) を FastAPI lifespan に移行
- `pyproject.toml` の `rpi-gpio` に環境マーカーを付与し、macOS で `rye sync` が通るようにする
- デッドコード削除 (`isPlayable`/`PLAY_FLG`/`if True:`/コメントアウト済み GPIO 行)

**対象外 (Phase 3 として別 change)**: 設定の pydantic-settings 化、GAS URL の環境変数化、`GET /{heat_index}` 副作用ルートの廃止、CI 整備。

## Capabilities

### New Capabilities

- `hardware-abstraction`: GPIO シグナル / 音声再生の Protocol 定義、実行環境の能力検出と実装選択 (gpiozero 実装・pygame 実装・Null 実装)、`DRORAS_GPIO` による明示制御、遅延初期化のライフサイクル

### Modified Capabilities

- `device-signals`: import 時初期化の撤廃 (→ ファクトリ遅延初期化)、音源パスの config 経由絶対パス化、連打防止なし → 二重スタートガードあり。カウントダウンシーケンスの順序・タイミング (3.0〜5.0 秒ランダム遅延、0.35 秒、音源ファイル) は不変
- `race-control`: Darwin 判定によるスキップを廃止し HAL 注入に置換 (全環境で同一コードパス)、スタートシーケンスの非ブロッキング実行、`start()` の例外処理修正 (未定義変数バグ解消)
- `heatlist-ingestion`: CSV 保存/読み込みパスを CWD 相対から `config.LOG_DIR` 絶対パスに変更、起動時自動読み込みのタイミングを import 直後から lifespan startup に変更 (読み込まれるという外形的挙動は不変)

## Impact

- **コード**: `src/droras/device.py` (削除→ `hardware/` へ再編)、`race_manager.py`、`server.py`、`convert_heatlist.py`、`config.py`、`pyproject.toml`
- **挙動互換性**: Socket.IO イベント・HTTP API・Firestore 同期・イベントログ形式は不変。RasPi 本番でのスタートシーケンスの体感 (音・LED・タイミング) も不変。変わるのは「カウントダウン中もサーバーが応答する」「連打が抑止される」点のみ
- **依存関係**: 追加依存なし。`rpi-gpio` が macOS でインストール対象外になる (RasPi では従来通り)
- **運用**: `run.sh` / systemd unit の変更不要。`DRORAS_GPIO` 未設定時は auto 検出で従来同等に動作
- **他 change との関係**: `add-4wave-support` (実装済み・未 archive) とはファイル重複が `convert_heatlist.py` のヘッダー定数のみで、本 change はヘッダー内容に触れないため競合しない
