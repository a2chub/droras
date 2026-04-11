## Why

JDL (Japan Drone League) の運営要件として、1 ヒートあたり **4 名** のパイロットがレースする「4 波」形式に対応する必要がある。現行システムは 1 ヒート = 3 名前提でハードコードされており、フロントエンド表示・CSV パース・Socket.IO payload・HTTP API レスポンスの各層で 3 名の仮定を解く必要がある。

本 change は seed-current-system で確立した baseline に対する **delta** として、4 名対応に必要な spec 変更のみを記述する。3 名対応は維持しない (完全切り替え)。

## What Changes

- **パイロット表示数** を 3 → 4 に変更
- **ビデオチャンネル** を `E1 / 5705`, `F1 / 5740`, `F4 / 5800` から `R2 / 5695`, `F1 / 5740`, `R4 / 5769`, `R5 / 5806` に変更
- **ヒート行フォーマット** (`all_heat_list` の各行) を `[p1, p2, p3, heat_no, class_name]` (5 要素) から `[p1, p2, p3, p4, heat_no, class_name]` (6 要素) に拡張
- **`socket.ts`** のハードコード index (`className: row[4]`, `pilots: row.slice(0, 3)`) を新フォーマットに合わせて更新
- **`operator-ui`** のテーブルコンテナ幅を `max-w-screen-md` (768px) → `max-w-screen-lg` (1024px) に拡大し、6 列化による窮屈さを緩和
- **固定ヘッダー sentinel** を `["E1", "F1", "F4", "HeatNo"]` → `["R2", "F1", "R4", "R5", "HeatNo"]` に更新 (1-based index の保証のため削除ではなく更新)

**BREAKING**: 3 名構成のヒートデータは読み込み対象外となる。既存の `log/heat_list.csv` は、展開後に 4 名版で再ダウンロードする必要がある。

### Out of Scope (本 change で触らない)

- 🚫 **`device-signals`** — リレー / GPIO / 音声制御は一切変更しない (ユーザー明示)
- 🚫 **`race-control`** — レース開始シーケンス自体は 3/4 名で変わらない
- 🚫 **`firestore-sync`** — ヒート番号同期は変わらない
- 🚫 **`event-logging`** — ログフォーマット自体は変わらない (パイロット CSV の中身が 1 要素長くなるのみ)
- 🚫 **`heat-number-display`** — ヒート番号表示は無関係

### Capabilities

#### New Capabilities
なし。本 change は既存 capability の MODIFIED のみ。

#### Modified Capabilities

- `heatlist-ingestion` — 行フォーマット拡張 (5→6 要素)、固定ヘッダー更新
- `heat-navigation` — `/current_pilots` レスポンスの要素数が 5→6
- `realtime-sync` — `heat_list` payload の各行が 5→6 要素 (プロトコル不変)
- `operator-ui` — 4 パイロット列化、新チャンネル名、コンテナ幅拡大、socket.ts の index/slice 更新
- `pilots-telop` — 最大 3 名 → 最大 4 名表示

## Impact

- **Affected code**:
  - `src/droras/convert_heatlist.py` — `load_heat_list()` の固定ヘッダー定数更新 (データ行生成ロジックは `len(pilots)` で動的なので変更不要)
  - `front/src/lib/socket.ts` — `className: row[5]`, `pilots: row.slice(0, 4)` に変更、`HeatData.pilots` 型は同じ `string[]`
  - `front/src/pages/App.tsx` — `TableRow` コンポーネントに 4 パイロット目のセルを追加、テーブルヘッダーを更新、コンテナ幅を `max-w-screen-lg` に変更
  - `front/src/pages/telop/PilotsTelop.tsx` — 表示 `<div>` を 4 つに拡張、`pilots[3]` のバインディング追加
- **Affected spec files**: 5 capability (heatlist-ingestion / heat-navigation / realtime-sync / operator-ui / pilots-telop)
- **Dependencies**: 変更なし
- **APIs**: HTTP / Socket.IO のイベント名・エンドポイント名は不変。ペイロードの要素数のみ変化
- **External prerequisite**: GAS/Spreadsheet が各ヒートにつき 4 行 (= 4 パイロット分) の CSV を返すよう整備されていること。これは droras リポジトリ外の責務
- **Operational prerequisite**: デプロイ後に `log/heat_list.csv` の再ダウンロードが必要 (3 名時代のキャッシュを破棄)
