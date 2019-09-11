#!/usr/bin/env python3

import os
import json
import asyncio
import requests
import platform
import urllib.request

from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS

from google.cloud import firestore

if platform.system() == "Darwin":
  def start_sound():
    print("pi pi pi po-n")
else:
  from jdl_lib.webapp import start_sound

from heat_list import make_heat, get_heat

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
def main(heat_index=1):
    global current_heat_index
    heat_data = make_heat()
    if heat_index > len(heat_data):
        heat_index = 1
    current_heat_index = heat_index
    #send_current_heat()
    #set_cur_heat( heat_index )
    if async_flg:
      loop.run_until_complete( set_cur_heat_fb( heat_index ) )
    return app.send_static_file("index.html")


@app.route('/h/<int:heat_index>')
def api_heat(heat_index=1):
    return jsonify(get_heat(heat_index))


@app.route('/api/start')
def start():
    start_sound()
    return "200"


@app.route('/api/get_cur_heat')
def cur_heat():
    return jsonify({'id': current_heat_index})


@app.route('/api/get_race_data')
def race_data():
    return jsonify(make_heat())


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


def make_return_data(heat_index):
    three_heat_data = [get_heat(int(heat_index) - 1),
                       get_heat(heat_index), get_heat(int(heat_index)+1)]
    heats = []
    ret = {}
    for heat_data in three_heat_data:
        heats.append({
            'E1': heat_data[0]['name'],
            'F1': heat_data[1]['name'],
            'F4': heat_data[2]['name'],
            'heat': heat_data[0]['heat'],
            'class': heat_data[0]['class'],
        })
    ret["heats"] = heats
    ret['prev'] = int(three_heat_data[1][0]['heat']) - 1
    if int(three_heat_data[1][0]['heat']) + 1 > 20:
        next_id = 1
    else:
        next_id = int(three_heat_data[1][0]['heat']) + 1
    ret['next'] = next_id
    return ret


def send_heat_data():
    url = 'http://localhost:3000/api/upload-heat-data'
    headers = {
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(make_heat()).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)

def send_current_heat():
    url = 'http://localhost:3000/api/set-current-heat'
    params = {
      'id': current_heat_index
    }
    req = urllib.request.Request('{}?{}'.format(
        url, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)

async def set_cur_heat_fb(heat_id=1):
  global async_flg
  async_flg = False
  race_ref = db.collection(u'race').document(u'current')
  race_ref.set({
    u'heat': u'%s'%(heat_id)
  })

  async_flg = True


def set_cur_heat(heat_id=1):
  cur_heat = "%s"%(heat_id)
  url = "https://script.google.com/macros/s/AKfycbwY05MtkIet6Yc_MlQvD9Ng4H_ZTpBcFZvtTj_BPE008Az8H8x2/exec"
  query = "?heat="

  try:
    response = requests.get(url + query + cur_heat)
  except:
    pass


if __name__ == '__main__':
  #send_heat_data()

  loop = asyncio.get_event_loop()
  app.run(host="0.0.0.0", port=8080)
