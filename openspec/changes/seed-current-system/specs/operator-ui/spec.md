## ADDED Requirements

### Requirement: ヒートテーブルの 3 行表示
`/` 画面は、前ヒート・現在ヒート・次ヒートの 3 行をテーブル形式で SHALL 表示する。

#### Scenario: 通常表示
- **WHEN** `heatList` が複数ヒートを含み、`currentHeat` が有効値である
- **THEN** 前・現在・次の 3 行が `<table>` に描画される
- **AND** 現在ヒートの行は他の行と視覚的に区別されるハイライトスタイル (緑背景・ボーダー・太字・2xl フォント) で表示される
- **AND** 前後ヒートは通常のボーダー付き行として描画される

### Requirement: ヒート行の wrap-around
前ヒート・次ヒートの index 計算は、先頭や末尾を超える場合 wrap-around SHALL する。

#### Scenario: 最初のヒートで前へ
- **WHEN** `currentHeat == 1` の状態で前ヒートを計算する
- **THEN** 前ヒートは末尾のヒート (`numHeats`) となる

#### Scenario: 最後のヒートで次へ
- **WHEN** `currentHeat == numHeats` の状態で次ヒートを計算する
- **THEN** 次ヒートは先頭のヒート (`1`) となる

### Requirement: テーブルヘッダー
テーブルは以下の固定列ヘッダーを SHALL 持つ: `Heat`, `Class`, `E1 / 5705`, `F1 / 5740`, `F4 / 5800`。

#### Scenario: ヘッダー描画
- **WHEN** `/` 画面が初期描画される
- **THEN** `<thead>` 内の最初の行に上記 5 列のヘッダーが表示される
- **AND** 2 列目以降はパイロットのビデオチャンネル (E1=5705, F1=5740, F4=5800 MHz) に対応する

### Requirement: スタート/ストップボタンとタイマー
画面には 2 分 30 秒 (150 秒) のカウントダウンタイマー付きのスタート/ストップボタンを SHALL 配置する。

#### Scenario: 初期状態 (スタート)
- **WHEN** `timerEnabled == false`
- **THEN** ボタン文字は「スタート」、背景色は緑 (`bg-green-600`) である

#### Scenario: スタート押下
- **WHEN** ユーザーが「スタート」ボタンを押下する
- **THEN** `timerEnabled` が `true` になる
- **AND** Socket.IO `start_heat` イベントが emit される
- **AND** `ProgressBar` がカウントダウンを開始する (`DURATION = 150` 秒)
- **AND** ボタンは「ストップ」表示に切り替わり、背景色は赤 (`bg-red-500`) になる

#### Scenario: ストップ押下
- **WHEN** `timerEnabled == true` の状態でボタンが押される
- **THEN** `timerEnabled` が `false` になる
- **AND** `ProgressBar` がリセットされる
- **AND** `start_heat` は emit されない

### Requirement: 進捗バーの自動完了
`ProgressBar` はタイマーが満了すると自動的に次ヒートへ進 SHALL む。

#### Scenario: タイマー満了
- **WHEN** タイマー開始からの経過秒数が 150 秒を超える
- **THEN** `ProgressBar` は `onComplete` コールバックを呼び出す
- **AND** オペレーター画面は `goNext()` を実行し、次ヒートへ移動する
- **AND** `timerEnabled` は `false` に戻る

#### Scenario: 進捗バー表示内容
- **WHEN** タイマーが進行中である
- **THEN** 左側に経過時間 (`M:SS`)、右側に残り時間 (`M:SS`) を表示する
- **AND** 青い塗り (`bg-blue-500`) が経過割合に応じて左から右に広がる

### Requirement: 前/次ヒートボタン
画面は前ヒート・次ヒートへ明示的に移動できるボタンを SHALL 提供する。

#### Scenario: 前ヒートボタン
- **WHEN** ユーザーが「前のヒート」ボタンを押下する
- **THEN** `timerEnabled` が `false` になる
- **AND** `currentHeat` が wrap-around を考慮した前ヒート番号に更新される
- **AND** Socket.IO `set_current_heat` イベントが emit される

#### Scenario: 次ヒートボタン
- **WHEN** ユーザーが「次のヒート」ボタンを押下する
- **THEN** `timerEnabled` が `false` になる
- **AND** `currentHeat` が wrap-around を考慮した次ヒート番号に更新される
- **AND** Socket.IO `set_current_heat` イベントが emit される

### Requirement: キーボードショートカット
画面はキーボードショートカットで主要操作を SHALL 提供する。

#### Scenario: ショートカット `1`
- **WHEN** ユーザーがキー `1` を押下する
- **THEN** スタート/ストップ トグルが発火する (`handleStart()`)

#### Scenario: ショートカット `2`
- **WHEN** ユーザーがキー `2` を押下する
- **THEN** 前ヒートへ移動する (`goPrev()`)

#### Scenario: ショートカット `3`
- **WHEN** ユーザーがキー `3` を押下する
- **THEN** 次ヒートへ移動する (`goNext()`)

### Requirement: 管理操作と Toast 通知
画面はヒートリストの再読み込み・再ダウンロード・ログアップロードの操作ボタンを SHALL 配置し、結果を toast で通知する。

#### Scenario: ヒートリスト再読み込み
- **WHEN** ユーザーが「ヒートリスト再読み込み」ボタンを押下する
- **THEN** Socket.IO `reload_heat_list` が emit され、ack を待つ
- **AND** 成功時 toast に「ヒートリストの再読み込みに成功しました」が表示される
- **AND** 失敗時 toast に「ヒートリストの再読み込みに失敗しました」が表示される

#### Scenario: ヒートリスト再ダウンロード
- **WHEN** ユーザーが「ヒートリスト再ダウンロード」ボタンを押下する
- **THEN** `downloading` 状態が `true` になりボタンが disabled となる
- **AND** Socket.IO `download_heat_list` が emit され、ack を待つ
- **AND** 完了後 `downloading` が `false` に戻る
- **AND** 成功/失敗に応じて toast 通知が表示される

#### Scenario: ログアップロード
- **WHEN** ユーザーが「ログアップロード」ボタンを押下する
- **THEN** Socket.IO `upload_log` が emit され、ack を待つ
- **AND** 成功/失敗に応じて toast 通知が表示される

### Requirement: URL への pushState
カレントヒートが変更されるたび、画面は URL を `/<heat>` に pushState SHALL する。

#### Scenario: カレントヒート変更
- **WHEN** `currentHeat > 0` になる (初期化または変更)
- **THEN** `window.history.pushState({}, "", "/<currentHeat>")` が実行される

### Requirement: Socket.IO による状態受信
画面は `useSocket()` hook を通じて `currentHeat` と `heatList` を Socket.IO 経由で SHALL 受信する。

#### Scenario: heat_list 受信
- **WHEN** サーバーから `heat_list` イベントを受信する
- **THEN** payload の各行を `{ className: row[4], pilots: row.slice(0, 3) }` にマップして state に反映する

#### Scenario: current_heat 受信
- **WHEN** サーバーから `current_heat` イベントを受信する
- **THEN** state の `currentHeat` がその値で更新される
