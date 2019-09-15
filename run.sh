#!/bin/bash

source `pwd`/venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=`pwd`"/jdl_lib/jdl-main-key.json"


wget "https://script.google.com/macros/s/AKfycbwY05MtkIet6Yc_MlQvD9Ng4H_ZTpBcFZvtTj_BPE008Az8H8x2/exec?getrace=now" -O static/pilots.json
python main.py
