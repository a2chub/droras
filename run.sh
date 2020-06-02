#!/bin/bash

source `pwd`/venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=`pwd`"/jdl_lib/jdl-main-key.json"


wget "https://docs.google.com/spreadsheets/d/e/2PACX-1vT70EjI5FcC7nNBO7DuwQeYlzADbWYWSxpO97PVHHYCUEpdsNwGGArXAh9EBpQl_3vXLyygdJZMY10K/pub?gid=554938252&single=true&output=csv" -O static/pilots.csv
python main.py
