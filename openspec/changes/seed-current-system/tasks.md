## 1. Spec ファイル生成

- [x] 1.1 `proposal.md` を作成
- [x] 1.2 `design.md` を作成
- [x] 1.3 `specs/race-control/spec.md` を作成
- [x] 1.4 `specs/heat-navigation/spec.md` を作成
- [x] 1.5 `specs/heatlist-ingestion/spec.md` を作成
- [x] 1.6 `specs/device-signals/spec.md` を作成
- [x] 1.7 `specs/realtime-sync/spec.md` を作成
- [x] 1.8 `specs/firestore-sync/spec.md` を作成
- [x] 1.9 `specs/event-logging/spec.md` を作成
- [x] 1.10 `specs/operator-ui/spec.md` を作成
- [x] 1.11 `specs/pilots-telop/spec.md` を作成
- [x] 1.12 `specs/heat-number-display/spec.md` を作成

## 2. 構造検証

- [ ] 2.1 `openspec validate seed-current-system --strict` でエラーなく通ることを確認
- [ ] 2.2 `openspec show seed-current-system` で proposal 内容を目視確認
- [ ] 2.3 各 spec ファイルの Scenario 見出しが exactly 4 hashtags (`####`) で書かれていることを確認
- [ ] 2.4 各 Requirement が最低 1 つの Scenario を持つことを確認
- [ ] 2.5 SHALL / MUST を用いた normative 表現になっていることを確認

## 3. 実装との突合せ (人手レビュー)

各 capability について、spec の記述と実コードが一致するか確認する。

- [ ] 3.1 `race-control` vs `src/droras/race_manager.py` (`start`, `count_down`)
- [ ] 3.2 `heat-navigation` vs `src/droras/race_manager.py` (`set_current_heat`, `get_current_pilots`) + `src/droras/server.py` (HTTP routes)
- [ ] 3.3 `heatlist-ingestion` vs `src/droras/convert_heatlist.py`
- [ ] 3.4 `device-signals` vs `src/droras/device.py`
- [ ] 3.5 `realtime-sync` vs `src/droras/server.py` (Socket.IO event handlers)
- [ ] 3.6 `firestore-sync` vs `src/droras/race_manager.py` (`connect_to_firestore`, `update_current_heat_on_firestore`)
- [ ] 3.7 `event-logging` vs `src/droras/event_logger.py`
- [ ] 3.8 `operator-ui` vs `front/src/pages/App.tsx` + `front/src/pages/ProgressBar.tsx` + `front/src/lib/socket.ts`
- [ ] 3.9 `pilots-telop` vs `front/src/pages/telop/PilotsTelop.tsx`
- [ ] 3.10 `heat-number-display` vs `front/src/pages/heatno/HeatNumber.tsx` + `front/src/lib/socket.ts`

## 4. Archive 前の最終確認

- [ ] 4.1 PR を作成し、チームレビューを受ける
- [ ] 4.2 レビューで指摘された曖昧さ・誤記を修正
- [ ] 4.3 `openspec validate` が clean な状態でマージ

## 5. Archive と baseline 確立

- [ ] 5.1 マージ後 `openspec archive seed-current-system` を実行
- [ ] 5.2 `openspec/specs/` 配下に 10 capability の spec が生成されたことを確認
- [ ] 5.3 `openspec list --specs` で一覧が意図通りであることを確認
- [ ] 5.4 archive 後のコミットを作成

## 6. Follow-up change の準備 (別 PR で追跡)

seed で記録した食い違いの解消は、本 change の archive 後に別の change として作成する。本 tasks.md では作成までを含めない。

- [ ] 6.1 `README.md` のカウントダウン秒数記述を実装 (3〜5 秒) に合わせる PR を作成
- [ ] 6.2 `device.py` のデッドコード (`isPlayable()`, `PLAY_FLG`) を削除する PR を作成
- [ ] 6.3 `device.py` の古いコメント `# define the 4 GPIO lines we want to use` を実情に合わせて更新する PR を作成
