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
    #query is a (V,E) pair
    nodes = query["nodes"]
    edges = query["edges"]

    nodeKeep = ["id", "type", "data"]
    edgeKeep = ["source", "sourceHandle", "target", "targetHandle"]
    
    def prune(dictlist, keep):
        newList = []
        for d in dictlist:
            newD = {}
            for k in d.keys():
                if k in keep:
                    newD[k] = d[k]

            newList.append(newD)
                
        return newList
                

    # nodes = prune(nodes, nodeKeep)
    # edges = prune(edges, edgeKeep)

    adjList = list(map(lambda a : {a["id"] : {**a, "in" : []}}, nodes))
    adjList = dict((key, d[key]) for d in adjList for key in d)

    for e in edges:
        spos, source = e["sourceHandle"].split("-")
        tpos, target = e["targetHandle"].split("-")
        source = source
        target = target

        if tpos == "in":
            adjList[target][tpos].append(adjList[source])
        else:
            adjList[target]["data"][tpos] = adjList[source]

    #convert the recurisve node format from the frontend into an AST 
    def recClean(json):
        dData = json["data"]
        dType = json["type"]
        dId = json["id"]
        dChildren = json["in"]

        if dType == "out":
            return recClean(json["in"][0])

        if dType == "bezier":
            print(dData)
            return {"bezier": [(0, 0), (dData["x"], dData["y"]), (1, 1)]}

        if dType == "value":
            return {"num" : float(dData["value"])}

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
                    if type(dData[dk]) == str:
                        dData[dk] = {"num" : float(dData[dk])}
                    else:
                        dData[dk] = recClean(dData[dk])

            if "shape" not in dData:
                dData["shape"] = "sin"

            return {"wave" : dData}

        if dType == "operation":
            return {"+" : [recClean(child) for child in dChildren]}

    adjList = recClean(adjList["output0"])

    return adjList


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

