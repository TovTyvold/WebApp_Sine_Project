from asyncio.windows_events import INFINITE
from operator import mod
from re import A
import uvicorn

from typing import List, Optional, Dict, Union
from fastapi import FastAPI, Response, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pointsCalculation
import soundGen
import ADSR_mod
import copy

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def handleInput(query):
    #convert the recurisve node format from the frontend into an AST 
    def recClean(json):
        dData = json["data"]
        dType = json["type"]
        dId = json["id"]
        dChildren = json["children"]

        if dType == "output":
            return recClean(json["children"][0])

        if dType == "envelope":
            child = recClean(dChildren[0])
            adsr = [float(f) for f in dData.values()]

            return {
                "envelope" : {
                    "points" : child, 
                    "adsr" : {"list" : adsr}
                }
            }

        if dType == "oscillator": #currently a leaf
            for dk in dData.keys():
                if dk in ["frequency", "amplitude"]:
                    dData[dk] = {"num" : float(dData[dk])}

            if "shape" not in dData:
                dData["shape"] = "sin"

            return {"wave" : dData}

        if dType == "operation":
            return {"+" : [recClean(child) for child in dChildren]}

    query = recClean(query)

    #find how long the signal should be
    #based on the longest envelope
    def findDur(query):
        if type(query) is not dict:
            return 0

        if type(query) is list:
            return max([findDur(q) for q in query])

        v = [0]
        for k in query.keys():
            if k == "envelope":
                v.append(sum(query[k]["adsr"]["list"]))
            else:
                v.append(findDur(query[k]))

        return max(v)

    dur = findDur(query)

    #if there are no envelopes default to 1 second
    return query


CHUNKSIZE = 1024
SAMPLES = 44100
@app.websocket("/sound")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while (True):
        #recieve wave information
        query = await websocket.receive_json()
        seconds = float(query["Seconds"])
        query = handleInput(query["NodeTree"])

        print(query)
        print(seconds)

        soundData = pointsCalculation.newparse(query, SAMPLES, seconds)

        #send chunkSize chunks of the sounddata until all is sent
        cb = soundGen.samplesToCB(soundData)
        data = cb.readChunk(CHUNKSIZE)
        while data:
            await websocket.send_bytes(data)
            data = cb.readChunk(CHUNKSIZE)


if __name__ == "__main__":
    config = uvicorn.Config("apiServer:app", port=5000,
                            log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()

