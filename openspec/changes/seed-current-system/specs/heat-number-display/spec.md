## ADDED Requirements

### Requirement: Socket.IO 経由のヒート番号受信
`/heatno/` 画面は、`useSocket()` hook を通じてサーバーから `current_heat` を SHALL 受信する。

#### Scenario: サーバーからのヒート番号受信
- **WHEN** Socket.IO サーバーが `current_heat` イベントを emit する
- **THEN** `/heatno/` 画面の内部状態 `currentHeat` がその値で更新される
- **AND** 画面は新しい値で再描画される

### Requirement: 有効時の大型ヒート番号表示
`currentHeat > 0` のとき、画面は該当のヒート番号を大型フォントで SHALL 表示する。

#### Scenario: ヒート番号表示
- **WHEN** `currentHeat == 5` の状態になる
- **THEN** 画面上に数字 `5` が表示される
- **AND** テキストは `Impact` フォント、サイズ `text-4xl`、マージン `my-1 mx-2` で描画される

### Requirement: 無効値での非描画
`currentHeat == 0` (初期値または未定義) のとき、画面は何も SHALL NOT 描画する。

#### Scenario: 初期状態
- **WHEN** Socket.IO からまだ有効な `current_heat` を受信していない (`currentHeat == 0`)
- **THEN** コンポーネントは `null` を返し、DOM 要素は描画されない

### Requirement: ライブ配信用の独立ページ
画面は操作 UI を持たず、表示専用のページとして SHALL 提供される。

#### Scenario: 表示専用
- **WHEN** `/heatno/` が配信用に表示される
- **THEN** スタート/ストップ、ヒート選択、リスト管理などの操作要素は一切描画されない
- **AND** `HeatNumber` コンポーネント単独で構成される
