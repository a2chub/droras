## ADDED Requirements

### Requirement: uv による依存管理
プロジェクトの Python 仮想環境・依存解決・lock は uv で管理 SHALL する。lock ファイルは `uv.lock` とし、rye 由来の `requirements.lock` / `requirements-dev.lock` および `[tool.rye]` 設定は SHALL 削除する。dev 依存 (pytest / httpx / ruff) は `[dependency-groups]` で SHALL 管理する。

#### Scenario: 開発環境の構築
- **WHEN** macOS または Linux で `uv sync` を実行する
- **THEN** Python 3.12 系の仮想環境が構築され、本体 + dev 依存がインストールされる
- **AND** macOS では `rpi-gpio` はインストール対象外となる (環境マーカー)

#### Scenario: lock の再現性
- **WHEN** `uv.lock` が存在する状態で `uv sync` を実行する
- **THEN** lock に固定されたバージョンが環境差なくインストールされる

### Requirement: run.sh の uv 対応
`run.sh` は uv 管理の環境でサーバーを起動 SHALL する。uv が利用できない環境では既存の `.venv/bin/python` 直接参照にフォールバック SHALL する。

#### Scenario: uv のある環境での起動
- **WHEN** `run.sh` を実行する
- **THEN** uv 管理の環境で `python -m droras` が起動する
- **AND** `GOOGLE_APPLICATION_CREDENTIALS` の設定など既存の前処理は維持される

### Requirement: CI によるテスト実行
システムは GitHub Actions により、push および pull request のたびに `ubuntu-latest` と `macos-latest` の両方で全テストスイートを実行 SHALL する。

#### Scenario: push 時のテスト実行
- **WHEN** ブランチに push される
- **THEN** 両 OS で `uv sync` → pytest が実行され、全テストがパスすればジョブが成功する

#### Scenario: GPIO 不在環境での実行
- **WHEN** CI 環境 (GPIO・オーディオデバイスなし) でテストが実行される
- **THEN** ハードウェア依存のテストは Null フォールバック / モックにより実機なしで完走する

### Requirement: CI による lint チェック
CI は ruff による lint (`ruff check`) とフォーマット検査 (`ruff format --check`) を実行 SHALL し、違反があればジョブを失敗 SHALL させる。

#### Scenario: lint 違反の検出
- **WHEN** lint 違反を含むコードが push される
- **THEN** CI の lint ジョブが失敗する

### Requirement: ruff 設定
ruff の設定は `pyproject.toml` に記述 SHALL し、リポジトリ内の既存 Python コード (src/ および tests/) は lint・フォーマット検査をクリーン SHALL に保つ。

#### Scenario: ローカルでの lint 実行
- **WHEN** `uv run ruff check src tests` を実行する
- **THEN** 違反 0 件で終了する
