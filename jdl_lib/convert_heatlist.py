
import requests
import csv
from start_log import logger

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQSIb1_Hys9ai97Mlf9LnxHaSFdWciZ2IC9kCTMbEQAHe7lvuM-7D-_8iKOtwibWMFL1ff1bP-keLJm/pub?gid=554938252&single=true&output=csv"

def get_heat_list(url=url):
  # 指定されたURLからデータをリクエストする
  r = requests.get(url)

  # ステータスコードが200 (成功) の場合
  if r.status_code == 200:
    # ファイルにデータを書き込む
    with open("log/heat_list.csv", "wb") as file:
      file.write(r.content)
    # ダウンロード完了のメッセージを表示
    print("ファイルのダウンロードが完了しました。")
    logger.info(f"download heat list")
  else:
    # ダウンロード失敗のメッセージを表示
    print("ファイルのダウンロードに失敗しました。")
    logger.info(f"download fail heat list")

  # 取得したデータをutf-8形式でデコード
  decoded_content = r.content.decode('utf-8')
  # デコードしたデータをCSVリーダーで処理
  cr = csv.reader(decoded_content.splitlines(), delimiter=',')
  # CSVデータをリストに変換して返す
  heat_list_csv = list(cr)
  return heat_list_csv


def load_heat_list():
  # 熱ごとのデータを格納する辞書
  by_heat = {}

  # CSVファイルを開く
  with open("log/heat_list.csv") as f:
    # CSVリーダーで読み込む
    reader = csv.reader(f)
    # ファイル内の各行をイテレート
    for row in reader:
      # 熱番号をキーとして、辞書にラウンドデータを追加
      by_heat.setdefault(row[3], []).append(row)

  # ヒート名のリストを初期化
  heat_name_list = [["E1", "F1", "F4", "HeatNo"]]

  # 各熱ごとに処理
  for i in range(1, len(by_heat.keys())):
    heat_names = []  # ヒート名を保持するためのリスト
    pilots = by_heat[str(i)]  # 各熱のパイロットデータ

    # パイロットデータをイテレート
    for ii in range(len(pilots)):
      pilot_name = pilots[ii][1]  # パイロット名を取得
      heat_names.append(pilot_name)  # ヒート名リストに追加
    heat_names.append(i)  # 現在のヒート番号を追加
    heat_name_list.append(heat_names)  # ヒート名リストに保存

  return heat_name_list  # ヒート名リストを返す


def get_heat_pilots(heat_id=1, all_heat_list=[]):
  if len(all_heat_list) < 1:
    return ""
  ret = ",".join([str(x) for x in all_heat_list[heat_id]])
  return ret

if __name__ == "__main__":
  import pprint
  get_heat_list(url)
  
  h_list = load_heat_list()
  pprint.pprint(h_list, indent=4)

"""
  test_heat = 8
  pilots_name = get_heat_pilots(test_heat, h_list)
  print(pilots_name)
"""  
