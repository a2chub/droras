# droras

Drone Race Random Start System

レーススタートのカウントダウンシステム

- ラズパイに リレーHATをつけて、LEDシグナルを点灯させる
- LINEアウトからカウントダウン音を鳴らす
- スタート音は、任意の秒数[default:4~9]後に 発火 < フライング抑制
- Web画面上にヒート毎のPilotを表示（前後ヒート含め3ヒート分）

## インストール

### [rye](https://rye-up.com/guide/installation/) インストール

```sh
curl -sSf https://rye-up.com/get | bash
```

### アプリ本体

```sh
git clone https://github.com/a2chub/droras.git
rye sync
```

### 認証キーの設定

`run.sh` と同じディレクトリに `jdl-main-key.json` として保存。

### サービスとしてインストール

1. `droras.service.example` を `droras.service` としてコピー。
2. `droras.service` を開いて `ExecStart` の `run.sh` のパスを正しいものに変更。
3. `droras.service` を `/etc/systemd/system/` に移動

    ```sh
    sudo mv droras.service /etc/systemd/system/
    ```

4. `droras.service` を起動する

    ```sh
    sudo systemctl start droras.service
    ```

5. `droras.service`  を自動起動するようにする

    ```sh
    sudo systemctl enable droras.service
    ```

## サービスの操作方法

### 状態を確認する

```sh
sudo systemctl status droras.service
```

### 再起動

```sh
sudo systemctl restart droras.service
```

### ログを見る

```sh
sudo journalctl -u droras.service -f -n 100
```
