## Context

JDL の新レギュレーションで 1 ヒート 4 名構成 (通称「4 波」) に対応する必要がある。droras は現在 3 名固定でハードコードされており、backend / frontend 両方で改修が必要。

本 change は [seed-current-system](../seed-current-system/) で確立した baseline への delta として作成される。seed spec の Requirement を MODIFIED で上書きする形で必要最小限の変更を記述する。

### Current state

- `feature/4wave-support` ブランチに seed-current-system がコミット済 (`f084563`)
- seed によって現行 3 名対応の全挙動が capability として spec 化されている
- 本 change がマージ・archive されると `openspec/specs/` に反映される

### Constraints

- **触ってはいけないもの** (ユーザー明示):
  - `device-signals` capability (リレー / GPIO / 音声)
  - `race-control` の開始シーケンス
- **3 名サポートは不要** (ユーザー明示) — 完全切り替え
- **GAS 側の CSV 供給変更は外部責務** — droras は 4 行/heat の CSV を受け取る前提

### Stakeholders

- オペレーター (4 名表示の新 UI を使う)
- ライブ配信担当 (`/telop/` で 4 名を表示する)
- JDL 運営 (4 波レギュレーション運用)
- GAS/Spreadsheet 管理者 (CSV ソース側の整備担当、連携必要)

---

## Goals / Non-Goals

### Goals

1. 1 ヒート 4 名のデータを最小コードで扱えるようにする
2. オペレーター画面とテロップ画面で 4 名を視認性よく表示する
3. チャンネル名と周波数を R2/F1/R4/R5 に統一表示する
4. spec と実装の一貫性を維持する (MODIFIED Requirement による delta 管理)

### Non-Goals

- 3/4 名の両対応 (切り替え機能やデータ中の動的判定)
- device-signals の変更 (リレー / 音声は現行のまま)
- race-control の開始シーケンス変更 (カウントダウン含めて同じ)
- 新しい UI アーキテクチャや TypeScript 型システムの刷新
- GAS/Spreadsheet 側の実装 (外部責務)

---

## Decisions

### Decision 1: `convert_heatlist.py` のデータ行生成は触らない

**選択**: `load_heat_list()` 内の `for ii in range(len(pilots))` ループは `len` で動的に対応しているため、**コードの修正は行わず、CSV 供給が 4 行/heat になれば自動的に 4 パイロット行になる**。

**理由**:
- 既存コードが既に動的対応している (偶然の設計的余裕)
- 最小変更の原則に従う
- 触るのは `heat_name_list = [["E1", "F1", "F4", "HeatNo"]]` の固定ヘッダー定数のみ

**影響**: `heatlist-ingestion` R4 (ヒート行フォーマット) は実装変更なしで spec のみ更新 (MODIFIED)。R5 (固定ヘッダー) は実装・spec 両方を更新。

### Decision 2: 固定ヘッダーは削除せず更新する

**選択**: `[["E1", "F1", "F4", "HeatNo"]]` を `[["R2", "F1", "R4", "R5", "HeatNo"]]` に更新する。削除はしない。

**理由**:
- この行は一見「誰も読まない死データ」だが、実は **1-based index の sentinel** として機能している。`get_heat_pilots(heat_id=1)` は `all_heat_list[1]` を読むので、index 0 に何らかのダミーがないと全ヒートの index がズレる
- 削除すると `range(1, len(by_heat.keys()))` のループロジックと `all_heat_list[heat_id]` のアクセスパターン全体に影響し、変更範囲が広がる
- 更新のみなら 1 行の定数変更で済む

**代替案**: sentinel を `None` や空リストにする → 却下: spec に記録された形式からの逸脱が大きい、JSON シリアライズの互換性懸念もある。

### Decision 3: チャンネル周波数は標準 5.8GHz バンドに従う

**選択**: 以下の標準周波数で固定表示する。

| チャンネル | 周波数 | 帯域 |
|---|---|---|
| R2 | 5695 MHz | Raceband |
| F1 | 5740 MHz | Fatshark/Airwave |
| R4 | 5769 MHz | Raceband |
| R5 | 5806 MHz | Raceband |

**理由**:
- 5.8GHz ISM 帯の標準チャンネルマップに従う
- 既存表示スタイル (`E1 / 5705` 形式) と整合性あり
- チャンネル間隔が 35〜45 MHz で取れており、4 波同時運用時の帯域間干渉リスクが小さい

**代替案**: チャンネル名のみ表示 (周波数なし) → 却下: ビデオピットで周波数を読む運用ニーズがあるため、情報を削らない。

### Decision 4: コンテナ幅を `max-w-screen-md` (768px) → `max-w-screen-lg` (1024px) に拡大

**選択**: `operator-ui` のテーブルコンテナを 1024px 幅に拡大する。

**理由**:
- 現行 5 列 (Heat/Class/P1/P2/P3) → 新 6 列 (Heat/Class/P1/P2/P3/P4) で 1 列増える
- 768px 幅のままだと各パイロット列が窮屈になり、氏名が途切れる可能性
- 1024px はラズパイディスプレイ (一般的に 1280x720 以上) でも収まる

**代替案の比較**:

| 案 | 狙い | 採用しなかった理由 |
|---|---|---|
| コンテナ幅はそのまま、フォント縮小 | 変更最小 | 読みにくくなる、ライブ配信用途で不利 |
| Class 列を縮める | 微妙な幅調整 | Class 文字列長が不定、効果が限定的 |
| Heat 列をアイコン化 | デザイン改善 | 本 change のスコープを超える |
| **max-w-screen-lg に拡大** ✅ | 各パイロット列に余裕 | 採用: 最小介入で視認性を確保 |

### Decision 5: `get_current_pilots` の返却形式は維持する

**選択**: `race_manager.get_current_pilots()` の実装は touch しない。返却値は現行通り `",".join(...)` 後の `split(",")` 結果 = 行全体の配列 (6 要素: `[p1, p2, p3, p4, heat_no_str, class_name]`)。

**理由**:
- `PilotsTelop` は index 0〜N の先頭要素しか参照しないため、3→4 名化に伴う追加変更は不要 (N=2→3 に変えるだけ)
- 実装リファクタ (パイロットだけを返す形にする等) は別 change で扱う
- 最小変更の原則

**影響**: `heat-navigation` R4 (`/current_pilots` レスポンス) は MODIFIED Requirement として「要素数 5→6」を記述し、frontend 側 (`pilots-telop`) の index 範囲を合わせる。

### Decision 6: `PilotsTelop` は `<div>` を 3 → 4 に増やす

**選択**: `flex justify-around` レイアウトの中で `<div>` を 4 つに増やす。各 `<div>` は `w-full text-center` のまま。

**理由**:
- `flex justify-around` は子要素数に応じて等分スペーシングするので、4 `<div>` でも自動的にバランスされる
- CSS 追加変更は不要
- ライブ配信用テロップは元々パイロット名のみの単純表示なので拡張が容易

### Decision 7: 新フィールドの TypeScript 型は `string[]` のまま

**選択**: `HeatData.pilots: string[]` の型は変更しない。長さが 3→4 に変わるだけ。

**理由**:
- `string[]` は長さ非制約のため、型変更不要
- tuple 型 (`[string, string, string, string]`) にすることで厳密化することも可能だが、本 change のスコープ外
- 将来の変更柔軟性を残す

---

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| GAS/Spreadsheet 側の CSV 更新が遅れ、4 行/heat のデータが来ない状態でデプロイされる → frontend の `row.slice(0, 4)` が `undefined` を含む可能性 | proposal.md の Prerequisite に明記。デプロイ時の GAS 更新確認を tasks.md に含める |
| 既存の `log/heat_list.csv` (3 人キャッシュ) が残っていると、サーバー起動時の自動読み込みで古いデータが現在値として返される | デプロイ手順として「再ダウンロード実施 or `log/heat_list.csv` 削除後の起動」を運用手順に含める |
| テーブルコンテナ幅変更が既存の CSS 階層や他画面に影響する可能性 | `App.tsx` のルート `div` のみの変更で閉じている (他画面は独立したエントリーポイント) |
| `socket.ts` の index 変更時に className と pilots の対応を間違える | spec の MODIFIED Requirement にコード断片を明記。実装前にレビュー |
| frontend 型が緩い (`string[]`) ため、配列の長さが 4 と想定してアクセスした index が実行時に `undefined` になる | `PilotsTelop` は 3→4 名への拡張時、3 要素未満のガードパターンを維持 (`pilots.length > N ? pilots[N] : ""`) |
| seed spec と本 change の Requirement の食い違いが将来の delta で混乱を生む | `openspec validate` で delta 整合性を確認。MODIFIED Requirement は seed の全文を正確にコピーして編集 |
| 1024px 幅がラズパイ内蔵ディスプレイで横スクロール誘発 | 実機確認を tasks.md に含める。必要ならば patch 版 change でフォントサイズ調整 |

---

## Migration Plan

本 change のコード変更は小さいが、以下の順序でデプロイすることで混乱を避ける:

1. **事前準備**: GAS/Spreadsheet 側が 4 行/heat の CSV を返せるようになっていることを確認 (外部責務)
2. **本 change のマージ**: `feature/4wave-support` ブランチをレビュー → `main` にマージ
3. **サービス停止**: `sudo systemctl stop droras.service`
4. **古いキャッシュの破棄**: `rm log/heat_list.csv` (念のため)
5. **サービス再起動**: `sudo systemctl restart droras.service`
6. **動作確認**: Operator UI でヒートリストの再ダウンロードを実施し、4 名表示が正しいことを目視確認
7. **テロップ動作確認**: `/telop/` 画面を OBS で読み込み、4 名が並ぶことを確認
8. **Firestore 確認**: カレントヒート変更が `race/current.heat` に反映されることを確認

### Rollback strategy

問題が発生した場合:

1. `git revert` で本 change のマージコミットを戻す
2. `log/heat_list.csv` も 3 名版に戻す必要がある (古いバックアップが必要)
3. GAS 側も 3 行/heat に戻す必要がある (外部責務) — **ロールバックは容易ではない** ため、デプロイ前の確認を入念に行う

### Archive

本 change が安定運用されたことを確認後:

```bash
openspec archive add-4wave-support
```

これにより `openspec/specs/` の該当 capability が MODIFIED Requirement の新内容で上書きされる。

---

## Open Questions

1. **ラズパイ実機での 1024px 幅の見え方**: 実機に接続されているディスプレイ解像度が不明。デプロイ時に横スクロールが出る場合は幅調整が必要
2. **`PilotsTelop` の文字サイズ**: 4 名に増えると 1 名あたりの幅が狭くなる (`text-xl` のまま十分か)。実機で確認
3. **ヒートリスト CSV の 4 名未満エッジケース**: 一部のヒートで 3 名または 2 名しかいない場合 (練習ヒート等)、`slice(0, 4)` で配列が短くなる。表示は空セル扱いで OK か、警告表示が必要か
4. **`get_current_pilots` のリファクタ**: Decision 5 で保留にしたが、将来的に `{pilots: [...], heat_no: N, class_name: ...}` のような辞書型レスポンスに移行する価値はある。別 change で扱うべき
