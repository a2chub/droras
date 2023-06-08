from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from webapp import start_sound
from start_log import logger

app = FastAPI()
CURRENT_HEAT_INDEX = 1

try:
    from google.cloud import firestore
    db = firestore.Client()
    race_ref = db.collection(u'race').document(u'current')
    print("connected firestore complete")
except:
    print(" no firestore")
    db = ""
    pass

# リレーの制御とスター音を鳴らす
@app.get('/api/start')
async def start():
    global CURRENT_HEAT_INDEX
    logger.info(f"{CURRENT_HEAT_INDEX}\tstart_heat")
    await count_down()
    return {"status":200}

async def count_down():
    start_sound()

@app.get('/api/{heat_index}')
async def set_current(heat_index: int = 1):
    global CURRENT_HEAT_INDEX
    CURRENT_HEAT_INDEX = heat_index
    logger.info(f"{CURRENT_HEAT_INDEX}\tchange_heat")
    try:
        print("call set_cur_heat_fb")
        await set_cur_heat_fb(str(heat_index))
    except:
        print('no send firestore')
    return {"heat_id": heat_index}

async def set_cur_heat_fb(heat_id=1):
    print("send firebase")
    race_ref.set({
        u'heat': u'%s' % (heat_id)
    })


app.mount("/", StaticFiles(directory="../static"), name="static")

