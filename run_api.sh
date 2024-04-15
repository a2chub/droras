export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)"/jdl-main-key.json"
source $(pwd)/venv/bin/activate

cd jdl_lib
python convert_heatlist.py
uvicorn jdl_api:app --reload --host=0.0.0.0
