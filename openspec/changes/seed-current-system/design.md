## Context

droras は日本ドローンリーグ (JDL) 向けのレーススタート用カウントダウンシステムで、ラズパイ単体で完結するハードウェア+Web統合アプリケーションである。現行構成:

- **Server**: Python 3 + FastAPI + python-socketio (ASGIモード) + uvicorn
- **Frontend**: React + Vite (multi-entry) + TypeScript + TailwindCSS + shadcn/ui
- **Hardware**: Raspberry Pi + リレー HAT (GPIO 26) + アナログ音声出力
- **External**: Google Sheets (via GAS エンドポイント) + Google Cloud Firestore
- **Deployment**: systemd unit (`droras.service`) + iptables port redirect

本 change は **seed proposal** であり、コード変更を一切含まない。目的は「今ここにあるものを OpenSpec の spec として忠実に明文化する」ことのみ。以降のすべての変更 (4 波対応・機能追加・バグ修正) は、ここで確立した baseline に対する delta (ADDED/MODIFIED/REMOVED Requirements) として管理される。

### Current state

- `openspec/specs/` は空 (capability ベースラインなし)
- `openspec/changes/archive/` も空 (過去の change 履歴なし)
- `feature/4wave-support` ブランチは現時点で `main` と同一コミット (4 波実装は未着手)
- README にはシステム概要と運用手順が記載されているが、コードとの食い違いあり (後述)

### Constraints

- **変更なし**: 本 seed はコードを一切変更しない
- **忠実性**: 仕様は README でも意図でもなく **実装そのもの** を真実とする
- **網羅性**: 漏れのない仕様書を目指す (粒度 3、詳細レベル)

### Stakeholders

- オペレーター (レース中に `/` を操作)
- ライブ配信オペレーター (`/telop/` `/heatno/` を OBS 等に表示)
- JDL 本部 (Firestore 経由の現在ヒート情報を外部サイトで消費)
- 開発者 (seed を基準に今後の変更を行う)

---

## Goals / Non-Goals

### Goals

1. 現行コード (Python backend + React frontend) の挙動を 1 対 1 で spec として記述する
2. 10 の capability に責務分割し、それぞれ Requirement + Scenario (WHEN/THEN) で表現する
3. 以降の変更が delta ベースで管理できる baseline を確立する
4. コードと README の食い違いを記録し、follow-up 対象として明示する

### Non-Goals

- **コード修正**: README と実装の食い違いを本 change で解消しない (別 change で追跡)
- **リファクタ**: デッドコード (`isPlayable()`, `PLAY_FLG`) の削除は本 change で行わない
- **新機能**: 4 波対応・新機能は別 change で追加する
- **テストコード**: 本 change は spec only、自動テストコードは追加しない
- **ドキュメント更新**: README の修正は follow-up 対象

---

## Decisions

### Decision 1: Seed を change proposal 経由で作成する (Q1 選択 A)

**選択**: Seed を `openspec/changes/seed-current-system/` に一時的に配置し、`openspec archive` で `openspec/specs/` に反映する。

**理由**:
- OpenSpec の正統ワークフローに乗せることで、以降の change proposal との整合性が取れる
- レビュー履歴が change archive に残る (誰がどう baseline を seed したか追跡可能)
- `archive` コマンドによる自動反映で `specs/` の物理的な編集ミスを回避できる

**代替案**: `openspec/specs/` に直接書き込む。却下理由は、OpenSpec のワークフローから外れ、後の delta 管理との整合性が崩れるため。

### Decision 2: コード実装を真実とする (Q2 選択 C)

**選択**: spec はコードの現行挙動を忠実に記述する。README や内部コメントとの食い違いは spec 側を修正せず、コード側またはドキュメント側の修正を別 change で追跡する。

**具体的な食い違い**:

| 項目 | README / コメント | コード実装 | spec の真実 |
|---|---|---|---|
| カウントダウン遅延 | "default: 4~9" 秒 (README) | `randint(30,50)/10.0` = 3.0〜5.0 秒 | **3.0〜5.0 秒** |
| 連打防止 | `isPlayable()` 関数 (2 秒クールダウン) 定義あり | `if True:` でバイパス、`PLAY_FLG` も戻らない | **連打防止なし** |
| GPIO 本数 | `# define the 4 GPIO lines we want to use` | 実際は `LED(26)` 1 本のみ | **LED 1 本** |

**理由**:
- ユーザー確認により「現場では 3〜5 秒で合っている」ことが判明
- README は古い記述であり、実運用のソース・オブ・トゥルースはコード

**代替案**: README を真実として spec を書く。却下理由は、spec と実動作が乖離し、外部からの挙動検証が不可能になるため。

### Decision 3: Capability を 10 本に細分化 (Q3 選択 A + Q4 選択 B)

**選択**: Backend 7 本 + Frontend 3 本 = 計 10 本。

**Backend (7)**:
- `race-control` — レース開始統括
- `heat-navigation` — ヒート状態と遷移
- `heatlist-ingestion` — Spreadsheet/CSV 取込み
- `device-signals` — GPIO + 音声
- `realtime-sync` — Socket.IO
- `firestore-sync` — Firestore 反映
- `event-logging` — CSV ログ

**Frontend (3)**:
- `operator-ui` (`/`)
- `pilots-telop` (`/telop/`)
- `heat-number-display` (`/heatno/`)

**理由**:
- 詳細レベル (粒度 3) では、責務を細かく切った方が個別の Requirement を見渡しやすい
- Frontend はエントリー (HTML) 単位で画面が独立している (Vite multi-entry) ため、画面ごとに capability を分ける方が自然
- 4 波対応のような横断的変更は、複数 capability への delta として表現しやすい

**代替案**:
- 粒度を粗く 5 本に統合する → 却下: 詳細仕様を書く際に Requirement が雑多になる
- Frontend を 1 本にまとめる → 却下: 各画面の責務が明確に異なる (操作 / 表示専用 × 2) ため分割の意義がある

### Decision 4: design.md / tasks.md も生成 (Q6 選択 C)

**選択**: `proposal.md` / `specs/` に加えて `design.md` (本ファイル) と `tasks.md` も作成する。

**理由**:
- ユーザーが「漏れのない仕様書」を希望しており、seed の背景・決定事項・follow-up を残しておく価値が高い
- 将来 seed を参照したとき、なぜ 10 分割になったか・なぜコード基準で書いたかを追跡可能にする
- `tasks.md` は seed の archive 前チェックリストとして利用する

**代替案**: `proposal.md` + `specs/` のみ。却下理由は、seed の意思決定履歴が失われ、同様の seed を将来行う際の参考にならないため。

---

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| spec がコードの **バグ** まで忠実に記述してしまい、修正時に spec も書き換える必要がある (例: `race_manager.start()` 内で `except: log_heat_error(...)` 後に `log_heat_start(...)` を続けて呼ぶ実装) | seed の目的が "現状のフリーズ" であることを proposal で明示。修正時は delta として MODIFIED Requirement を出す前提を合意 |
| 粒度が細かすぎて Requirement 数が多く、レビュー負荷が高い | capability 単位でレビュー可能に分割済。全 spec を一度に見る必要はない |
| コードを読んで書き起こす過程で人間ミスが入り、実装との齟齬が残る | 本 change を archive する前に `openspec validate` を実行し、必要であれば各 spec を実コードと突き合わせる確認タスクを `tasks.md` に入れる |
| 後の 4 波対応 change が大きくなり、多数の capability に delta を入れる必要が出る | seed で capability が細かく分かれているため、影響範囲を局所化しやすい (細分化の利点) |
| README / デッドコードの食い違いを放置することで、新規参加者が混乱する | proposal の "Impact" セクションに follow-up 対象として明示。archive 後に別 change で対応 |
| 認証キー (`jdl-main-key.json`) の取り扱いは spec には書けるが運用面は外部責務になる | `firestore-sync` spec 内で "外部責務" と明示。運用ドキュメントは README 側で扱う |

---

## Migration Plan

本 change はコード変更を伴わないため、従来的な意味での "マイグレーション" は不要。ただし seed を `openspec/specs/` に反映するための archive 手順は以下:

1. 全 spec ファイル生成後、`openspec validate seed-current-system --strict` で整形・構造チェック
2. レビュー (PR 経由) でヒューマンチェック
3. `openspec archive seed-current-system` で `openspec/specs/<capability>/spec.md` に自動反映
4. 以降の change は `openspec/specs/` を baseline として delta を出す

**ロールバック戦略**: seed の archive 後に問題が発覚した場合は、`openspec/specs/` を `git revert` または手動で削除し、改訂した seed change を再度作成・archive する。

---

## Open Questions

1. **`log_heat_error` の命名**: `event_logger.log_heat_error` のログラベルは `firebase_send_error` だが、実際は `get_heat_pilots` 失敗時に呼ばれる (Firestore とは無関係)。spec には事実として両方記述したが、将来的に命名を修正する価値がある。
2. **`/current_pilots` のレスポンス形式**: 現在は CSV 文字列を `","` 分割した配列を返すが、ヒート番号・クラス名なども含まれるため、消費側 (`pilots-telop`) は index 0〜2 しか見ていない。将来的に辞書型レスポンスへの移行を検討する余地あり。
3. **Socket.IO の acknowledgement 引数**: `reload_heat_list` `download_heat_list` `upload_log` は ack 用に `data` 引数を受け取るが、内容は使われていない。spec には "受け取るが使用しない" と明示すべきか?
   - 本 seed では「受け取る」点のみ記載し、詳細は未記述。
4. **4 波対応時の影響範囲**: 想定では `heatlist-ingestion` (CSV カラム追加) / `operator-ui` (列追加) / `realtime-sync` (payload 構造変更) / `pilots-telop` (表示数変更) あたりに delta が入る。これは seed archive 後の 4 波 change proposal で確定させる。
