
export GOOGLE_APPLICATION_CREDENTIALS=`pwd`"/jdl_lib/jdl-main-key_org.json"
cd jdl_lib
uvicorn jdl_api:app --reload --host=0.0.0.0
