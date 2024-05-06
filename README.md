# droras

Drone Race Random Start System

レーススタートのカウントダウンシステム

- ラズパイにリレーHATをつけて、LEDシグナルを点灯させる
- LINEアウトからカウントダウン音を鳴らす
- スタート音は、任意の秒数 (default: 4~9) 後に 発火 < フライング抑制
- Web画面上にヒート毎のPilotを表示（前後ヒート含め3ヒート分）
- サーバー側は Python, FastAPI
- Web側は Vite, React
- サーバーと Web は Scoket.IO で同期
- 現在のヒート番号のみ Firestore に保存して <https://info.japandroneleague.com/> と同期

## インストール

### [rye](https://rye-up.com/guide/installation/) インストール

Python 仮想環境とモジュール管理に rye つかってます。

```sh
curl -sSf https://rye-up.com/get | bash
```

### アプリ本体

```sh
git clone https://github.com/a2chub/droras.git
git checkout refactor-all
rye sync
```

`rye sync` だけで仮想環境構築と関連モジュールダウンロード全部できる、らくちん。

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

### iptables の設定

やらなくてもいいけどやるとポート番号指定しなくてよくなる。( <http://jdl-pi.local/> とか)  
droras はポート 8000 で動いてるので 80 を 8000 に流してやる。

```sh
sudo apt-get install iptables
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8000
sudo iptables-save
sudo apt-get install iptables-persistent
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

## ヒートリスト

- CSV を Spreadsheet から直接読み込んでる
- URL は [`convert_heatlist.py` に直接かかれてる](https://github.com/a2chub/droras/blob/39ab1b86eeaf05063e2b4c81768cf1b120e4faaa/src/droras/convert_heatlist.py#L11)（ほんとは環境変数にしたほうがいいかも？

## 開発

### サーバー側

`run.sh` で起動すれば uvicorn が reload=True になってるのでファイル変更すれば自働反映

### Web側

- `front` ディレクトリ内で開発（ラズパイだとちょっと重いかも…
- pnpm でパッケージ管理してるので必要に応じて[インストール](https://pnpm.io/installation)
- `pnpm i` で依存関係を install
- `pnpm dev` で dev server が ポート 5173 で起動 <http://localhost:5173/>
- `pnpm build` で `/static/` にサーバー配信用ファイルたちが生成される
