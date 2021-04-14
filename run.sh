#!/bin/bash

source `pwd`/venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=`pwd`"/jdl_lib/jdl-main-key.json"

#2020 csv
#wget "https://docs.google.com/spreadsheets/d/e/2PACX-1vT70EjI5FcC7nNBO7DuwQeYlzADbWYWSxpO97PVHHYCUEpdsNwGGArXAh9EBpQl_3vXLyygdJZMY10K/pub?gid=554938252&single=true&output=csv" -O static/pilots.csv

wget "https://docs.google.com/spreadsheets/d/e/2PACX-1vQSIb1_Hys9ai97Mlf9LnxHaSFdWciZ2IC9kCTMbEQAHe7lvuM-7D-_8iKOtwibWMFL1ff1bP-keLJm/pub?gid=554938252&single=true&output=csv" -O  static/pilots.csv

python main.py
