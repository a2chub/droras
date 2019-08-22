#!/usr/bin/env python3

from heat_list import make_heat, get_heat
from flask import Flask, render_template
from flask import send_from_directory
import json
import os

from jdl_lib.webapp import start_sound

import redis
REDIS_HOST = "localhost"

app = Flask(__name__)
app.debug = True


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<h_id>')
def main(h_id=1):
  global conn
  heat_data = make_heat()
  if int(h_id) > len(heat_data):
    h_id = 1
  conn.set("cur_heat", h_id)
  return render_template('index.html', data= make_return_data(h_id) )

@app.route('/h/<h_id>')
def api_heat(h_id=1):
  return json.dumps( get_heat( h_id ), indent=2, ensure_ascii=False)

@app.route('/api/start')
def start():
  start_sound()
  return "200"

@app.route('/api/get_cur_heat')
def cur_heat():
  h_id = conn.get("cur_heat")
  return str( h_id.decode('utf-8') )

@app.route('/')
def view():
  global conn
  h_id = conn.get("cur_heat")
  return render_template('view.html', data= make_return_data(h_id) )

def make_return_data(h_id):
  three_heat_data = [get_heat( int(h_id) -1 ), get_heat( h_id ), get_heat( int(h_id)+1 )]
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
  ret['prev'] = int( three_heat_data[1][0]['heat']) -1
  if int(three_heat_data[1][0]['heat']) + 1 > 20:
    next_id = 1
  else:
    next_id = int(three_heat_data[1][0]['heat']) + 1
  ret['next'] =  next_id
  return ret


def redis_setup():
  global REDIS_HOST
  conn = redis.StrictRedis(host=REDIS_HOST,  port=6379)
  return conn

if __name__ == '__main__':
  conn = redis_setup()
  app.run(host="0.0.0.0", port=8080)
