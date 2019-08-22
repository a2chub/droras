# droras
Drone Race Random Start System

レーススタートのカウントダウンシステム
- ラズパイに リレーHATをつけて、LEDシグナルを点灯させる
- LINEアウトからカウントダウン音を鳴らす
- スタート音は、任意の秒数[default:4~9]後に 発火 < フライング抑制
- Web画面上にヒート毎のPilotを表示（前後ヒート含め3ヒート分）


## インストール

```
git clone このリポジトリ
cd リポジトリ
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requests.txt
python main.py
```

## ヒートデータの作り方

`heat_list.py` 内に 1行 1選手で記述する
4カラムで、スペース2つがデリミタとなる（ GoogleSpreadSheetからのコピペ対策

サンプル
`管理ID  氏名  クラス  HeatNo`

## API 仕様

### 現在フライト中のヒートID取得
URL: `/api/get_cur_heat`
Response: int文字列

### 開催中の全レースデータ取得
URL: `/api/get_race_data`
Response: ヒート毎のArrayが詰まった、LISTのJSON
Sample：　```
[
  [
    {
      "JDL_ID": "J17026",
      "name": "山崎 鉄兵",
      "heat": "1",
      "class": "Open"
    },
    {
      "JDL_ID": "J19253",
      "name": "楠本 竜也",
      "heat": "1",
      "class": "Open"
    },
    {
      "JDL_ID": "J17032",
      "name": "小池 卓三",
      "heat": "1",
      "class": "Open"
    }
  ],
  [
    {
      "JDL_ID": "J19252",
      "name": "西脇 慎一",
      "heat": "2",
      "class": "Open"
    },
    {
      "JDL_ID": "J19250",
      "name": "清水 友理香",
      "heat": "2",
      "class": "Open"
    },
    {
      "JDL_ID": "J19249",
      "name": "重光 真吾",
      "heat": "2",
      "class": "Open"
    }
  ],
  ．．．．．．
  ]
]
```
