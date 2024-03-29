#!/usr/bin/env python3

import json
import requests
import asyncio
import platform
import re

from flask import Flask, jsonify
from flask_cors import CORS


if platform.system() == "Darwin":
    def start_sound():
        print("pi pi pi po-n")
else:
    from jdl_lib.webapp import start_sound


async_flg = True

with open('static/pilots.csv') as f:
    heat_list = {}
    for index, line in enumerate(f.readlines()):
        id, name, klass, heat = line.strip().split(',')
        # print(index, id, name, klass, heat)
        if not re.match(r'J\d{5}', id):
            continue
        if heat not in heat_list:
            heat_list[heat] = []
        heat_list[heat].append({id: id, name: name, klass: klass})
    # print(heat_list)
total_heat_count = len(heat_list)
# print(total_heat_count)

app = Flask(__name__, static_url_path='')
CORS(app)
app.debug = False

try:
    from google.cloud import firestore
    db = firestore.Client()
except:
    print(" no firestore")
    db = ""
    pass


@app.route('/')
def root():
    return app.send_static_file("index.html")


@app.route('/<int:heat_index>')
def set_current_heat(heat_index=1):
    return app.send_static_file("index.html")


@app.route('/telop/')
def telop():
    return app.send_static_file("index.html")


@app.route('/api/start')
def start():
    start_sound()
    return "200"


@app.route('/api/<int:heat_index>')
def set_current(heat_index=1):
    heat_index = (heat_index - 1) % total_heat_count + 1
    print("set cur heat number")
    if async_flg:
        try:
            loop.run_until_complete(set_cur_heat_fb(heat_index))
        except:
            print('no send firestore')
    return jsonify({'id': heat_index})


async def set_cur_heat_fb(heat_id=1):
    global async_flg
    print("send firebase")
    async_flg = False
    race_ref = db.collection(u'race').document(u'current')
    race_ref.set({
        u'heat': u'%s' % (heat_id)
    })
    async_flg = True


@app.route('/api/jsonpudate')
def download_heat():
    res = requests.get(
        "https://script.google.com/macros/s/AKfycbwY05MtkIet6Yc_MlQvD9Ng4H_ZTpBcFZvtTj_BPE008Az8H8x2/exec?getrace=now").json()
    text = json.dumps(res, ensure_ascii=False)
    with open("static/pilots.json", "w") as file:
        file.write(str(text.encode("utf-8")))
    return "save done"


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.run(host="0.0.0.0", port=8080)
