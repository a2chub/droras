## ADDED Requirements

### Requirement: パイロット情報のポーリング取得
`/telop/` 画面は、HTTP `GET /current_pilots` を 2 秒間隔で SHALL ポーリングする。

#### Scenario: 初回取得
- **WHEN** `/telop/` がマウントされる
- **THEN** 直ちに `fetch('/current_pilots')` が 1 度実行される

#### Scenario: 継続ポーリング
- **WHEN** 画面がマウントされた後
- **THEN** `setInterval(fetchPilots, 2000)` により 2 秒ごとに `fetch('/current_pilots')` が呼ばれる
- **AND** 画面アンマウント時に interval がクリアされる

### Requirement: 取得失敗のハンドリング
fetch 失敗時、システムは例外をコンソールにログ出力 SHALL し、直前の表示状態を維持する。

#### Scenario: fetch 例外
- **WHEN** `fetch('/current_pilots')` が例外を投げる
- **THEN** `Failed to fetch pilots:` をプレフィックスとするエラーが `console.error` で出力される
- **AND** `pilots` state は変更されない (直前の値を維持)

### Requirement: 最大 3 パイロットの横並び表示
画面は取得したパイロット名配列から、最大 3 名を横並びで SHALL 表示する。

#### Scenario: 3 名以上の場合
- **WHEN** `pilots` 配列の長さが 3 以上である
- **THEN** index 0, 1, 2 の要素がそれぞれ 3 つの `<div>` に表示される

#### Scenario: 3 名未満の場合
- **WHEN** `pilots` 配列の長さが 3 未満である
- **THEN** 不足分の位置には空文字列が表示される
- **AND** 各 `<div>` のレイアウト (幅・中央揃え) は維持される

### Requirement: 表示スタイル
パイロット名表示は、ライブ配信用に大きく読みやすい SHALL 書式とする。

#### Scenario: スタイル適用
- **WHEN** パイロット行が描画される
- **THEN** コンテナは `flex justify-around w-full my-2 text-xl font-bold` クラスを持つ
- **AND** 各 `<div>` は `w-full text-center` で中央揃えされる

### Requirement: 接続先の自動切替
画面は、開発モードでは `http://localhost:8000` 、本番モードでは同一オリジンへ SHALL リクエストを送る。

#### Scenario: 開発モード
- **WHEN** `import.meta.env.DEV` が true である
- **THEN** fetch URL は `http://localhost:8000/current_pilots` である

#### Scenario: 本番モード
- **WHEN** `import.meta.env.DEV` が false である
- **THEN** fetch URL は `/current_pilots` (相対パス) である
