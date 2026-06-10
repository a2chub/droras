## Context

droras はドローンレースのスタート制御システムで、RasPi 上で systemd サービスとして稼働する。GPIO 26 のリレー HAT で LED シグナルを制御し、pygame で カウントダウン音 / スタート音を再生する。開発は macOS 上で行われる。

現行の `device.py` はモジュール import 時に `LED(26)` の実体化と `pygame.init()` を行い、`race_manager.count_down()` 内の `platform.system() != "Darwin"` 判定で import 自体を回避している。このため:

- macOS では音声を含む全スタートシーケンスがテスト不能
- Linux 開発機 / CI では起動時クラッシュ
- `start_sound()` の `sleep(3〜5 秒)` が Socket.IO の同期ハンドラ経由で呼ばれ、AsyncServer のイベントループを停止させる
- `pyproject.toml` の `rpi-gpio` が無条件依存のため macOS で `rye sync` が失敗する

他に、裸 `except:` 4 箇所、`RaceManager.start()` の except 節での未定義変数参照、CWD 依存の相対パス、import 時副作用 (logging 設定・`load_heat()`・`RaceManager` 生成) がある。

## Goals / Non-Goals

**Goals:**

- RasPi / macOS / Linux のどの環境でも同一コードパスで安全に起動・動作する (環境差は HAL の実装選択のみに閉じる)
- macOS でスタートシーケンス (音声再生含む) を実際に動かして開発・確認できる
- カウントダウン中もサーバーが応答し続ける (イベントループ非ブロッキング)
- 本番 RasPi での外形的挙動 (音・LED・タイミング・API・ログ形式) を一切変えない
- 例外処理を明示化し、障害時に原因がログから追える状態にする

**Non-Goals:**

- 設定の pydantic-settings 化、GAS URL の環境変数化 (Phase 3)
- `GET /{heat_index}` 副作用ルートの仕様変更 (互換のため現状維持)
- フロントエンド (`front/`) の変更
- テストフレームワーク / CI の整備 (Phase 3。ただし本 change の構造はテスト可能性を前提に設計する)

## Decisions

### D1. HAL は Protocol + ファクトリ関数で構成する

`src/droras/hardware/` パッケージを新設:

```
src/droras/hardware/
  __init__.py   # create_start_signal(), create_audio_player() ファクトリ + 公開API
  base.py       # StartSignal / AudioPlayer の Protocol 定義
  gpio.py       # GpioStartSignal (gpiozero。import はモジュール関数/メソッド内で遅延)
  audio.py      # PygameAudioPlayer (pygame。遅延 init)
  null.py       # NullStartSignal / NullAudioPlayer (ログ出力のみ)
  __main__.py   # 手動テスト用エントリ (python -m droras.hardware でシーケンス単独実行)
```

- `base.py` は `typing.Protocol` で `StartSignal` (`on()` / `off()`) と `AudioPlayer` (`play(sound_name)` — 再生開始のみ、待機は呼び出し側) を定義。ABC 継承ではなく Protocol にするのは、実装側に基底クラス依存を持ち込まず Null 実装やテストダブルを自由に書けるようにするため。
- gpiozero / pygame の import は各実装モジュールの初期化メソッド内に置き、`hardware` パッケージの import 自体はどの環境でも副作用なしで成功する。

代替案: gpiozero の `MockFactory` (`GPIOZERO_PIN_FACTORY=mock`) のみで吸収する案。gpiozero のコード経路をそのまま通せる利点はあるが、(1) macOS に gpiozero のインストールは必要なまま、(2) pygame 側の抽象化は別途必要、(3) 暗黙の環境変数依存になる — ため、自前 Protocol を主構造とし、MockFactory は `DRORAS_GPIO=mock` の一実装として利用可能にするに留める。

### D2. 実装選択は「能力検出 + 環境変数オーバーライド」

`create_start_signal()` は環境変数 `DRORAS_GPIO` で制御する:

| 値 | 挙動 |
|----|------|
| `auto` (デフォルト/未設定) | gpiozero の import とピンファクトリ初期化を試行し、失敗したら WARNING ログを出して Null 実装にフォールバック |
| `on` | GPIO 実装を強制。初期化失敗は起動時エラー (本番 RasPi で配線・権限異常を黙殺しないため) |
| `off` | Null 実装を強制 |
| `mock` | `GPIOZERO_PIN_FACTORY=mock` を設定して gpiozero 実装を使用 (gpiozero コード経路の検証用) |

音声は GPIO と独立に検出する: `pygame.mixer.init()` を試行し、失敗 (オーディオデバイスなし、ヘッドレス CI 等) なら Null にフォールバック。macOS では実音声が鳴る。

`platform.system()` による分岐は全廃する。「OS が何か」ではなく「その機能が使えるか」が判定基準。

本番 RasPi の systemd unit では将来的に `Environment=DRORAS_GPIO=on` を推奨する (フォールバックによる無音動作を防ぐ) が、未設定 `auto` でも従来同等に動作するため運用変更は必須としない。

### D3. デバイスは RaceManager にコンストラクタ注入する

`RaceManager(start_signal, audio_player)` とし、生成は `server.py` の lifespan で行う。`count_down()` 内の遅延 import + platform 分岐は削除。シーケンスロジック (LED ON → pipipi 再生 → ランダム遅延 → po-n 再生 → 0.35 秒 → LED OFF) は `hardware/` 側ではなく `RaceManager` (または専用の `StartSequence` 関数) に置き、HAL は「単機能の操作」のみ提供する。タイミング定数 (`randint(30, 50) / 10.0`、`0.35`) は現行値を維持する。

### D4. 非ブロッキング化は asyncio.to_thread + 実行中フラグ

- `start_heat` ハンドラを async 化し、シーケンス本体 (同期 `sleep` を含む) を `asyncio.to_thread()` で実行する。シーケンス内部は同期コードのまま変えない (pygame の再生と `sleep` の組み合わせは同期実装が最も単純で、タイミング特性も現行と同一になる)。
- 二重スタートガード: `RaceManager` に実行中フラグ (`asyncio.Lock` の non-blocking 取得、または bool + 例外安全な try/finally) を持たせ、シーケンス実行中の `start()` は WARNING ログを出して無視する。レース現場でのオペレーター連打・誤操作はこれまで「たまたま」問題化していなかっただけで、同時 2 シーケンスは音の重複と LED 状態不整合を起こすため抑止する。

代替案: シーケンス自体を async 化 (`asyncio.sleep`)。コードは一見綺麗になるが、pygame 呼び出しはどのみち同期であり、スレッド実行のほうが「現行コードとの差分が最小 = タイミング挙動の回帰リスクが最小」のため見送り。

### D5. import 時副作用は lifespan に集約する

- `server.py` モジュールレベルの `race_manager = RaceManager()` と `race_manager.load_heat()` を FastAPI の lifespan (startup) に移す。Firestore 接続 (`RaceManager.__init__` 内) もこれに伴い起動時に実行される (タイミングが import 時→ startup 時に変わるだけで挙動は不変)。
- Socket.IO ハンドラからの参照はモジュール変数 `race_manager: RaceManager | None` を lifespan で代入する形にする (ハンドラ登録構造は現行を維持し、変更を最小化)。
- `__init__.py` の logging 設定と `event_logger.py` のハンドラ生成は現状維持とする (副作用ではあるがクラッシュ要因ではなく、変更すると systemd 運用時のログ挙動に回帰リスクがあるため Phase 3 送り)。

### D6. パスは config.py 起点の絶対パスに統一

- `convert_heatlist.py` の `"log/heat_list.csv"` → `config.HEAT_LIST_CSV` (= `os.path.join(LOG_DIR, "heat_list.csv")`) を新設して参照。
- 音源パス: `config.SOUND_DIR` (= `BASE_DIR/sound`) を新設し、`device.py` の `get_resource_path()` (相対 `../../` 解決) を置き換える。
- `run.sh` が CWD を固定しているため現行でも事故は起きていないが、`python -m droras` の直接実行や将来のテスト実行で壊れる構造を排除する。

### D7. 例外処理の明示化

| 箇所 | 現行 | 変更後 |
|------|------|--------|
| `RaceManager.connect_to_firestore` | 裸 except | `Exception` 捕捉 + `exc_info` 付きログ (グレースフル継続は維持) |
| `RaceManager.load_heat` | 裸 except | 同上 |
| `RaceManager.start` | 裸 except + 未定義変数参照 | `current_pilots = ""` を事前初期化し、`Exception` 捕捉。`log_heat_error` → `log_heat_start` の二重記録は「エラー時もヒート開始記録は残す」意図として維持 |
| `server.upload_log` | 裸 except | `OSError` / `subprocess.SubprocessError` 捕捉 + `exc_info` 付きログ |

裸 `except:` は `KeyboardInterrupt` / `SystemExit` を握りつぶすため全廃。捕捉後の外形的挙動 (戻り値・継続) は現行スペックを維持する。

### D8. pyproject.toml の依存マーカー

```toml
"rpi-gpio>=0.7.1; sys_platform == 'linux'",
```

`gpiozero` は pure Python で全環境にインストール可能なため無条件のまま。`rpi-gpio` のみ Linux 限定にする (RasPi OS は linux)。lock ファイル (`requirements.lock`) は rye で再生成する。

## Risks / Trade-offs

- [本番 RasPi でのタイミング回帰] → シーケンスロジックの数値・順序を一切変えず、同期コードをスレッドに載せるだけの構成にする。実装後に RasPi 実機での音・LED 確認をタスク化する
- [`auto` 検出のフォールバックにより、本番で GPIO 初期化失敗が「無音で Null 動作」になる] → フォールバック時は WARNING を必ずログする。本番は `DRORAS_GPIO=on` の明示設定を README / service example に追記して推奨
- [lifespan 移行による起動順序の変化 (Firestore 接続・heat 読み込みが ASGI startup まで遅延)] → uvicorn 起動フローでは実用上の差なし。起動失敗時も従来同様グレースフルに継続することを spec で固定
- [二重スタートガードという新挙動の追加] → 「実行中のみ無視 + WARNING ログ」という最小限の介入に留める。連打可能だった現行挙動に依存した運用は存在しない (運用ヒアリング済みの前提。spec の REMOVED で明示)
- [pygame.mixer の遅延 init による初回再生のレイテンシ] → lifespan 起動時にファクトリで初期化を済ませるため、`start()` 時点では初期化済み。初回ヒートでの遅延は発生しない
- [rye lock 再生成が他依存のバージョンを動かす可能性] → lock 差分をレビューし、`rpi-gpio` のマーカー以外の意図しない更新があれば固定する

## Migration Plan

1. 本 change を `feature/4wave-support` ブランチ上に積む (4wave はコード実装済みのため競合最小)
2. macOS で `rye sync` → `run.sh` 起動 → `DRORAS_GPIO=off|auto` で全 Socket.IO イベント動作確認 (音声は実再生)
3. RasPi 実機で `DRORAS_GPIO` 未設定 (auto) のままデプロイし、LED・音・タイミングを従来と比較確認
4. 問題があれば revert のみで戻せる (DB スキーマ・外部契約・フロントエンドに変更がないため)

## Open Questions

- なし (本番 systemd unit への `DRORAS_GPIO=on` 追記は推奨に留め、本 change では example ファイルとREADME の更新のみ行う)
