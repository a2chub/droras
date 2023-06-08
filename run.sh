#!/bin/bash

source `pwd`/venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=`pwd`"/jdl_lib/jdl-main-key.json"

python main.py
