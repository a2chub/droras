#!/bin/bash

source `pwd`/venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=`pwd`"/jdl_lib/jdl-main-b84eea70963d.json"
python main.py
