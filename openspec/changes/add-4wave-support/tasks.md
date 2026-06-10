## 1. 事前準備 / 外部連携

- [ ] 1.1 GAS/Spreadsheet 側が各ヒートにつき 4 行の CSV を返すことを確認 (外部責務)
- [ ] 1.2 テスト用の 4 名ヒート CSV サンプルを取得し、手動で `log/heat_list.csv` に配置して動作確認できる状態を作る

## 2. Backend 変更

- [x] 2.1 `src/droras/convert_heatlist.py` の `load_heat_list()` 内の固定ヘッダー定数を `[["E1", "F1", "F4", "HeatNo"]]` → `[["R2", "F1", "R4", "R5", "HeatNo"]]` に変更
- [x] 2.2 `load_heat_list()` の例外処理内の同じ固定ヘッダーも合わせて変更 (コード再確認の結果、例外処理内に別の定数は存在せず §2.1 の 1 箇所変更で両ケース網羅)
- [x] 2.3 `convert_heatlist.py` 単独実行で 4 行 CSV が正しく 6 要素行として読み込まれることを確認 — 4パイロット×4ヒートの test CSV で `load_heat_list()` ロジックを検証、各ヒート行が 6 要素 `[p1..p4, heat_no, class_name]` になることを確認済

## 3. Frontend 変更 — 共通層

- [x] 3.1 `front/src/lib/socket.ts` の `onHeatList` 内のマップ処理を以下に変更:
  - `className: row[4]` → `className: row[5]`
  - `pilots: row.slice(0, 3)` → `pilots: row.slice(0, 4)`
- [x] 3.2 `HeatData` 型は `string[]` のまま変更なし (長さが 4 に変わるだけ)

## 4. Frontend 変更 — オペレーター画面 (`operator-ui`)

- [x] 4.1 `front/src/pages/App.tsx` の `TableRow` コンポーネントに 4 番目のパイロットセル (`pilots[3]`) を追加
- [x] 4.2 `<thead>` 内のヘッダー行を以下に変更:
  - `Heat`, `Class`, `R2 / 5695`, `F1 / 5740`, `R4 / 5769`, `R5 / 5806`
- [x] 4.3 ルート `<div>` のクラスを `container max-w-screen-md pt-4 mx-auto text-lg` → `container max-w-screen-lg pt-4 mx-auto text-lg` に変更
- [x] 4.4 開発環境 (`pnpm dev`) で 4 パイロット表示を目視確認 — 実機サーバー起動 + curl / Socket.IO クライアントで検証。`/current_pilots` が 6 要素配列 `[Pilot_A1..A4, "1", "Sport"]` を返すこと、`heat_list` イベントが 3 ヒート × 6 要素/行で broadcast されることを確認済 (ブラウザでの目視確認は実機デプロイ時に §8.4 で実施)
- [ ] 4.5 キーボードショートカット (1/2/3)・スタート/ストップ・前後ヒートが従来通り動作することを確認

## 5. Frontend 変更 — テロップ画面 (`pilots-telop`)

- [x] 5.1 `front/src/pages/telop/PilotsTelop.tsx` の JSX に 4 番目の `<div>` を追加:
  - `{pilots.length > 3 ? pilots[3] : ""}`
- [x] 5.2 既存の 3 つの `<div>` はそのまま維持 (条件式 `> 0`, `> 1`, `> 2` は変更不要)
- [ ] 5.3 `flex justify-around` が 4 要素で正しく等分配置されることを目視確認
- [ ] 5.4 OBS 等への読み込み確認 (実運用画面で余白・折り返しチェック)

## 6. Spec 変更の構造検証

- [x] 6.1 `openspec validate add-4wave-support --strict` でエラーなく通ることを確認
- [x] 6.2 `openspec show add-4wave-support --type change` で delta が意図通り表示されることを確認 (9 deltas: 5 capability)
- [x] 6.3 MODIFIED Requirement の全文が seed の該当 Requirement を基に修正されていることを確認

## 7. 実装と spec の突合せ

- [x] 7.1 `heatlist-ingestion` の MODIFIED Requirement が `convert_heatlist.py` の実装と一致していることを確認
- [x] 7.2 `heat-navigation` の MODIFIED Requirement が `/current_pilots` の実装と一致していることを確認 (race_manager は変更不要、heatlist 側変更で自動対応)
- [x] 7.3 `realtime-sync` の MODIFIED Requirement が Socket.IO `heat_list` emit 実装と一致していることを確認 (server.py は変更不要)
- [x] 7.4 `operator-ui` の MODIFIED / ADDED Requirement が `App.tsx` `socket.ts` の実装と一致していることを確認
- [x] 7.5 `pilots-telop` の MODIFIED Requirement が `PilotsTelop.tsx` の実装と一致していることを確認

## 8. 実機確認 (ラズパイ)

- [ ] 8.1 ラズパイ本体にデプロイして起動確認
- [ ] 8.2 サービス再起動 (`sudo systemctl restart droras.service`)
- [ ] 8.3 オペレーター画面でヒートリスト再ダウンロード実施
- [ ] 8.4 4 パイロット表示が実機ディスプレイで視認可能であることを確認
- [ ] 8.5 1024px 幅が実機ディスプレイで横スクロールを生まないことを確認 (生む場合は patch 対応)
- [ ] 8.6 リレー・音声は **変更していない** ため、カウントダウン動作が seed 時点と同一であることを確認

## 9. Archive

- [ ] 9.1 PR を作成・レビューを受ける
- [ ] 9.2 `main` にマージ後、本 change が安定動作することを確認
- [ ] 9.3 `openspec archive add-4wave-support` を実行
- [ ] 9.4 `openspec/specs/` の該当 capability が MODIFIED 内容で上書きされていることを確認
- [ ] 9.5 archive 後のコミットを作成

## 10. 運用・ドキュメント

- [x] 10.1 README のチャンネル表記を更新 (3 チャンネル → 4 チャンネル) — 確認の結果 README にチャンネル表記は存在せず (line 10 の「3ヒート分」は前/現/次の 3 ヒート表示の意味で、パイロット数ではない)。更新不要
- [x] 10.2 運用手順書の再ダウンロード手順を更新 — 運用手順書はリポジトリ内に存在せず、口頭伝承で運用されていることを確認。更新対象ファイルなし
- [ ] 10.3 既知の未解決事項 (`design.md` Open Questions) を Issue 化するか判断
