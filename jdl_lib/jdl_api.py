from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from webapp import start_sound
app = FastAPI()

try:
    from google.cloud import firestore
    db = firestore.Client()
    race_ref = db.collection(u'race').document(u'current')
    print("connected firestore complete")
except:
    print(" no firestore")
    db = ""
    pass

@app.get('/api/start')
async def start():
    await count_down()
    return {"status":200}


async def count_down():
  start_sound()

@app.get('/api/{heat_index}')
async def set_current(heat_index: int = 1):
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
