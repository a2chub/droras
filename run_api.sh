
export GOOGLE_APPLICATION_CREDENTIALS=`pwd`"/jdl_lib/jdl-main-key.json"
source `pwd`/venv/bin/activate
cd jdl_lib
uvicorn jdl_api:app --reload --host=0.0.0.0
