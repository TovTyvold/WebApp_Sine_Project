import uvicorn

from typing import List, Optional, Dict, Union, Tuple
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import pointsCalculation
import soundGen

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


#convert recTree recursively into an AST
#json should be constant and not changed by this function.
def recClean(json: Union[dict, str, float, int]) -> dict:
    if type(json) in [str, float, int]:
        return {"num": float(json)}

    if type(json) == list:
        return [{"num": float(v)} for v in json]

    if "percent" in json:
        return {"num": float(json["percent"]) / 100}

    if "ms" in json:
        return {"num": float(json["ms"]) / 1000}

    dType = json["type"]
    dData = json["data"]
    dChildren = json["in"]

    if dType == "out":
        return recClean(json["in"][0])

    if dType == "effect":
        return {dData["effectName"] : dict([(k, recClean(dData["params"][k])) for k in dData["params"].keys()]+[("points", recClean(dChildren[0]))])}

    if dType == "noise":
        return {"color" : dData["color"]}

    if dType == "mix":
        return {dType : dict([(k, recClean(dData[k])) for k in dData.keys()])}

    if dType == "bezier":
        return {"bezier": dData["points"]}

    if dType == "value":
        return recClean(dData["value"])

    if dType == "envelope":
        return {"envelope": dict([(k, recClean(dData[k])) for k in dData.keys()]+[("points", recClean(dChildren[0]))])}

    if dType == "oscillator": 
        return {"wave": dict([k,dData[k]] if k == "shape" else [k, recClean(dData[k])] for k in dData.keys())}

    if dType == "operation":
        return {("+" if dData["opType"] == "sum" else "*") : [recClean(child) for child in dChildren]}

#go through the tree and find the largest topmost envelope time
def recFindEnv(tree : dict):
    if (type(tree) != dict):
        return 0

    a = []
    for key in tree.keys():
        data = tree[key]

        if (type(data) == list):
            a.append(max([recFindEnv(child) for child in data]))
        elif key == "envelope":
            #we do not recurse here
            #therefore only the topmost envelope time is used
            times = [data[k]["num"] if k in ["attack", "decay", "release"] else 0 for k in data]
            time = sum(times)
            a.append(time)
        elif type(data) == dict:
            a.append(recFindEnv(data))
        else:
            return 0

    #could be multiple envelopes in the signal (e.g. added togheter), 
    # we want the longest one
    return max(a)

def handleInput(query):
    #query is a (V,E) pair
    nodes = query["nodes"]
    edges = query["edges"]

    recTree = list(map(lambda a : {a["id"] : {**a, "in" : []}}, nodes))
    recTree = dict((key, d[key]) for d in recTree for key in d)

    for e in edges:
        _, source = e["sourceHandle"].split("-")
        tpos, target = e["targetHandle"].split("-")
        source = source
        target = target

        if tpos == "in":
            recTree[target][tpos].append(recTree[source])
        else:
            recTree[target]["data"][tpos] = recTree[source]

    soundTree = recClean(recTree["output0"])
    panTree = recClean(recTree["output0"]["data"]["pan"])
    print("\nsoundtree\n",soundTree)
    print("\npantree\n",panTree)

    #do not add panning if pan percent is set to 0.5
    if not ("num" in panTree and panTree["num"] == 0.5):
        soundTree = {"pan" : { 
            "percent" : panTree, 
            "points" : soundTree
        }}


    sustainTime = recTree["output0"]["data"]["sustainTime"]["sec"]
    envelopeTime = recFindEnv(soundTree)
    return soundTree, sustainTime, envelopeTime


CHUNKSIZE = 1024
SAMPLES = 44100
@app.websocket("/sound")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while (True):
            #recieve wave information
            query = await websocket.receive_json()
            query, sustainTime, envelopeTime = handleInput(query)

            print("\nprocessesing: \n", query)
            print("\ntotalTime: ", envelopeTime+sustainTime, ", consisting of:", "\n\tsustainTime:", sustainTime, "\n\tenvelopeTime:", envelopeTime, "\n")

            soundData, channels = pointsCalculation.newparse(query, SAMPLES, sustainTime, envelopeTime)

            print("done processesing")

            sampleCount = len(soundData) if type(soundData) is not tuple else len(soundData[0])
            await websocket.send_json({"SampleCount": sampleCount, "Channels": channels})

            # soundGen.play(soundData, channels)

            #send chunkSize chunks of the sounddata until all is sent
            cb = soundGen.samplesToCB(soundData)
            data = cb.readChunk(CHUNKSIZE)
            while data:
                await websocket.send_bytes(data)
                data = cb.readChunk(CHUNKSIZE)
    except WebSocketDisconnect:
        print("disconnected")


if __name__ == "__main__":
    config = uvicorn.Config("apiServer:app", port=5000,
                            log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
