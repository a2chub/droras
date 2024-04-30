#!/bin/bash

# Move to the directory where this script is located
cd "$(dirname "$0")"

export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/jdl-main-key.json

$(pwd)/.venv/bin/python -m droras
