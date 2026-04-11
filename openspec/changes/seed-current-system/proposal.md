## Why

droras (ドローンレース用カウントダウンシステム) の現行仕様はコード本体と README に散在しており、機能追加・リファクタの基準が曖昧。特に `feature/4wave-support` ブランチで予定している 4 波対応を安全に進めるためには、まず **現行 (main 相当) の挙動を忠実に明文化し、変更の差分基準 (baseline) を確立する** 必要がある。

本 proposal は純粋な seed であり、コード変更を一切含まない (doc/spec only)。目的は「今ここにあるものを spec にする」こと、それ以上でも以下でもない。

## What Changes

- 現行コード (Python backend + React frontend) の挙動を忠実に反映した **10 の capability 仕様** を新規追加する
- 以降の変更 (4 波対応など) は OpenSpec の delta (`ADDED` / `MODIFIED` / `REMOVED` Requirements) として管理する
- **Non-breaking**: 既存の挙動・API・UI は一切変更しない

### Capabilities

#### New Capabilities

Backend (7 本):

- `race-control` — レース開始シーケンス (カウントダウン音 → スタート音) の統括
- `heat-navigation` — カレントヒートの参照・遷移・直接指定
- `heatlist-ingestion` — Spreadsheet/GAS からの CSV 取り込みとパース
- `device-signals` — ラズパイ GPIO (LED) と pygame 音声再生
- `realtime-sync` — Socket.IO によるクライアント同期
- `firestore-sync` — カレントヒート番号の Firestore への非同期公開
- `event-logging` — ヒートイベントの CSV ログ (日次ローテ)

Frontend (3 本):

- `operator-ui` — オペレーター操作画面 (`/`)
- `pilots-telop` — ライブ配信用パイロット名テロップ (`/telop/`)
- `heat-number-display` — ライブ配信用ヒート番号表示 (`/heatno/`)

#### Modified Capabilities

なし (seed のため既存 spec は存在しない)。

## Impact

- **Affected code**: なし (doc/spec only)
- **New files**: `openspec/changes/seed-current-system/` 配下のみ
- **Dependencies**: 変更なし
- **APIs**: 変更なし

### 既知の食い違い (Follow-up で追跡可能)

コード読解中に発見された、現行コードと README/内部コメントの食い違い。本 seed では **コード実装を真実とし**、以下は seed archive 後に別途対応する想定:

1. **README のカウントダウン秒数** — README は "default: 4~9" 秒と記載しているが、実装 (`device.py:62`) は `randint(30,50)/10.0` = **3.0〜5.0 秒**。spec はコード基準 (3.0〜5.0 秒) で記述。README 側の修正は別 PR/change で追跡。
2. **デッドコード `isPlayable()` / `PLAY_FLG`** — `device.py` に連打防止機構 (`isPlayable()`, 2 秒クールダウン) が定義されているが、`start_sound()` 内で `if True:` によりバイパスされ、`PLAY_FLG` も一度 False になると元に戻らない経路がない。spec は実態通り「連打防止なし」と記述。コードのクリーンアップは別 change で追跡。
3. **`device.py` 内コメント** — `# define the 4 GPIO lines we want to use` とあるが、実際に定義されているのは GPIO 26 の LED 1 本のみ。spec は実装通り「LED 1 本」と記述。

これらはいずれも spec 変更を伴わないため、通常のコミットまたは doc/refactor 系 change proposal として処理可能。
