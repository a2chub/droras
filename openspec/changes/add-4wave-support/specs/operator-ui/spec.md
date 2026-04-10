## MODIFIED Requirements

### Requirement: ヒートテーブルの 3 行表示
`/` 画面は、前ヒート・現在ヒート・次ヒートの 3 行をテーブル形式で SHALL 表示する。各行は 4 パイロット分の列を持つ。

#### Scenario: 通常表示
- **WHEN** `heatList` が複数ヒートを含み、`currentHeat` が有効値である
- **THEN** 前・現在・次の 3 行が `<table>` に描画される
- **AND** 各行は 6 列 (Heat 番号 + Class 名 + 4 パイロット) で構成される
- **AND** 現在ヒートの行は他の行と視覚的に区別されるハイライトスタイル (緑背景・ボーダー・太字・2xl フォント) で表示される
- **AND** 前後ヒートは通常のボーダー付き行として描画される
- **AND** `TableRow` コンポーネントは `pilots[0]` から `pilots[3]` までの 4 セルを描画する

### Requirement: テーブルヘッダー
テーブルは以下の固定列ヘッダーを SHALL 持つ: `Heat`, `Class`, `R2 / 5695`, `F1 / 5740`, `R4 / 5769`, `R5 / 5806`。

#### Scenario: ヘッダー描画
- **WHEN** `/` 画面が初期描画される
- **THEN** `<thead>` 内の最初の行に上記 6 列のヘッダーが表示される
- **AND** 2 列目 (Class) 以降はパイロットのビデオチャンネル (R2=5695, F1=5740, R4=5769, R5=5806 MHz) に対応する
- **AND** チャンネル順は R2 → F1 → R4 → R5 で固定される (周波数昇順に一致)

### Requirement: Socket.IO による状態受信
画面は `useSocket()` hook を通じて `currentHeat` と `heatList` を Socket.IO 経由で SHALL 受信する。

#### Scenario: heat_list 受信
- **WHEN** サーバーから `heat_list` イベントを受信する
- **THEN** payload の各行を `{ className: row[5], pilots: row.slice(0, 4) }` にマップして state に反映する
- **AND** `className` は行の index 5 (6 要素配列の最終要素) から取得される
- **AND** `pilots` は行の先頭 4 要素 (index 0〜3) から取得される

#### Scenario: current_heat 受信
- **WHEN** サーバーから `current_heat` イベントを受信する
- **THEN** state の `currentHeat` がその値で更新される

## ADDED Requirements

### Requirement: テーブルコンテナ幅
`/` 画面のメインコンテナは、6 列レイアウトの視認性を確保するため、最大幅を `max-w-screen-lg` (1024px) で SHALL 表示する。

#### Scenario: コンテナ幅
- **WHEN** `/` 画面が描画される
- **THEN** ルート `<div>` のクラスに `max-w-screen-lg` が含まれる
- **AND** 旧 `max-w-screen-md` (768px) 指定は使われない
- **AND** `mx-auto` により中央揃えが維持される

#### Scenario: 狭幅ディスプレイでの挙動
- **WHEN** ビューポート幅が 1024px 未満である
- **THEN** Tailwind のレスポンシブ挙動により、コンテナはビューポート幅に収まる (`max-w-*` は最大値のみを制約するため)
- **AND** 横スクロールは発生しない (コンテナ内テーブルが親幅を超える場合は例外)
