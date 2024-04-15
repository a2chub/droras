import csv
import logging

import requests

logger = logging.getLogger(__name__)

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQSIb1_Hys9ai97Mlf9LnxHaSFdWciZ2IC9kCTMbEQAHe7lvuM-7D-_8iKOtwibWMFL1ff1bP-keLJm/pub?gid=554938252&single=true&output=csv"


def get_heat_list(url=url):
    logger.info(f"Starting get heat list from url: {url}")

    response = requests.get(url)

    if response.status_code == 200:
        with open("log/heat_list.csv", "wb") as file:
            file.write(response.content)
        logger.info("Sucessfully downloaded heat list")
    else:
        logger.error(f"Failed to download heat list. status code: {response.status_code}")

    text = response.content.decode("utf-8")
    reader = csv.reader(text.splitlines(), delimiter=",")
    return list(reader)


def load_heat_list():
    by_heat = {}

    with open("log/heat_list.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            # heat number をキーとして、辞書にラウンドデータを追加
            by_heat.setdefault(row[3], []).append(row)

    heat_name_list = [["E1", "F1", "F4", "HeatNo"]]

    for i in range(1, len(by_heat.keys())):
        heat_names = []
        pilots = by_heat[str(i)]

        for ii in range(len(pilots)):
            pilot_name = pilots[ii][1]
            heat_names.append(pilot_name)
        heat_names.append(i)
        heat_name_list.append(heat_names)

    return heat_name_list


def get_heat_pilots(heat_id=1, all_heat_list=[]):
    if len(all_heat_list) < 1:
        return ""
    ret = ",".join([str(x) for x in all_heat_list[heat_id]])
    return ret


if __name__ == "__main__":
    import pprint

    get_heat_list(url)

    heat_list = load_heat_list()
    pprint.pprint(heat_list, indent=4)

"""
  test_heat = 8
  pilots_name = get_heat_pilots(test_heat, h_list)
  print(pilots_name)
"""
