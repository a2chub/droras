from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

try:
    from google.cloud import firestore
    db = firestore.Client().from_service_account_json('jdl-main-key_org.json')
    race_ref = db.collection(u'race').document(u'current')
    print("connected firestore complete")
except:
    print(" no firestore")
    db = ""
    pass

@app.get('/api/{heat_index}')
async def set_current(heat_index: int = 1):
    try:
        print("call set_cur_heat_fb")
        set_cur_heat_fb(str(heat_index))
    except:
        print('no send firestore')
    return {"heat_id": heat_index}

def set_cur_heat_fb(heat_id=1):
    print("send firebase")
    race_ref.set({
        u'heat': u'%s' % (heat_id)
    })

app.mount("/", StaticFiles(directory="../static"), name="static")