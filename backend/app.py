from fastapi import FastAPI, Request
import backend.utils as utils
from pathlib import Path
import os.path

app = FastAPI()


@app.post("/predict")
async def predict(request:Request):
    res = await request.json()
    ticket = res['ticket']
    flag = os.path.isfile(f'./backend/models/rnn_{ticket}.pth')
    if flag:
        model  = utils.Predict(ticket)
        return model.predict()
    else:
        return {'status':'ERROR! Ticket is not exist.'}