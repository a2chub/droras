#!/usr/bin/env python3

import os
from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS

from jdl_lib.webapp import start_sound
from heat_list import make_heat, get_heat

current_heat = 0

app = Flask(__name__, static_url_path='')
CORS(app)
app.debug = True


@app.route('/')
def root():
    return app.send_static_file("index.html")


@app.route('/<int:h_id>')
def main(h_id=1):
    global current_heat
    heat_data = make_heat()
    if h_id > len(heat_data):
        h_id = 1
    current_heat = h_id
    return render_template('index.html', data=make_return_data(h_id))


@app.route('/h/<int:h_id>')
def api_heat(h_id=1):
    return jsonify(get_heat(h_id))


@app.route('/api/start')
def start():
    start_sound()
    return "200"


@app.route('/api/get_cur_heat')
def cur_heat():
    return jsonify({'id': current_heat})


@app.route('/api/get_race_data')
def race_data():
    return jsonify(make_heat())


def make_return_data(h_id):
    three_heat_data = [get_heat(int(h_id) - 1),
                       get_heat(h_id), get_heat(int(h_id)+1)]
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
