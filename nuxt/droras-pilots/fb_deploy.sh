#!/bin/bash

cp -rf ../../static/ public
wget "https://script.google.com/macros/s/AKfycbwY05MtkIet6Yc_MlQvD9Ng4H_ZTpBcFZvtTj_BPE008Az8H8x2/exec?getrace=now" -O public/pilots.json

cp public/pilots.json ../../static/pilots.json
firebase deploy
