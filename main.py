#!/usr/bin/env python3

from heat_list import make_heat
import os
import json
import asyncio
import platform

from flask import Flask, jsonify
from flask_cors import CORS

from google.cloud import firestore

if platform.system() == "Darwin":
    def start_sound():
        print("pi pi pi po-n")
else:
    from jdl_lib.webapp import start_sound


current_heat_index = 0
async_flg = True


app = Flask(__name__, static_url_path='')
CORS(app)
app.debug = True

try:
    db = firestore.Client()
except:
    print(" no firestore")
    pass


@app.route('/')
def root():
    return app.send_static_file("index.html")


@app.route('/<int:heat_index>')
def set_current_heat(heat_index=1):
    return app.send_static_file("index.html")


@app.route('/api/start')
def start():
    start_sound()
    return "200"


@app.route('/api/<int:heat_index>')
def set_current(heat_index=1):
    global current_heat_index
    heat_data = make_heat()
    if heat_index > len(heat_data):
        heat_index = 1
    current_heat_index = heat_index
    if async_flg:
        loop.run_until_complete(set_cur_heat_fb(heat_index))
    return jsonify({'id': current_heat_index})


async def set_cur_heat_fb(heat_id=1):
    global async_flg
    async_flg = False
    race_ref = db.collection(u'race').document(u'current')
    race_ref.set({
        u'heat': u'%s' % (heat_id)
    })
    async_flg = True


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.run(host="0.0.0.0", port=8080)
