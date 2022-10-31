from asyncio.windows_events import INFINITE
from lib2to3.pytree import convert
from operator import mod
from re import A
import uvicorn

from typing import List, Optional, Dict, Union, Tuple
from fastapi import FastAPI, Response, HTTPException, WebSocket, WebSocketDisconnect
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

#converts numbers with units to floats e.g. 100ms to 0.1, 100% to 1
def parseTypedNumber(xs: str) -> Tuple[str, float]:
    if type(xs) != str:
        print("warning, passed non str", xs, " to parseTypedNumber")
        return "", xs

    def find(pred, xs):
        for i in range(len(xs)):
            if pred(xs[i]):
                return i
        return len(xs)

    nonNumberIndex = find(lambda a : not(a.isdigit() or a == "."), xs)
    t = xs[nonNumberIndex:]
    v = (xs[:nonNumberIndex])
    v = 0 if v == "" else float(v)
    return (t, v)

def convertToNumber(xs:str) -> float:
    t, v = parseTypedNumber(xs)

    if t == "ms":
        return v/1000
    if t == "%":
        return v/100
    else:
        return v

# print(convertToNumber("100.1ms")) #-> 0.1001
# print(convertToNumber("100.1%")) #-> 1.1
# print(convertToNumber("100.1")) #-> 100.1


def handleInput(query):
    #query is a (V,E) pair
    nodes = query["nodes"]
    edges = query["edges"]

    recTree = list(map(lambda a : {a["id"] : {**a, "in" : []}}, nodes))
    recTree = dict((key, d[key]) for d in recTree for key in d)

    sustainTime = float(recTree["output0"]["data"]["sustainTime"])

    for e in edges:
        _, source = e["sourceHandle"].split("-")
        tpos, target = e["targetHandle"].split("-")
        source = source
        target = target

        if tpos == "in":
            recTree[target][tpos].append(recTree[source])
        else:
            recTree[target]["data"][tpos] = recTree[source]

    #convert recTree recursively into an AST
    #json should be constant and not changed by this function.
    def recClean(json: Union[dict, str, float, int]) -> dict:
        if type(json) in [str, float, int]:
            return {"num": convertToNumber(json)}

        if type(json) == list:
            return [convertToNumber(v) for v in json]

        dType = json["type"]
        dData = json["data"]
        dChildren = json["in"]

        if dType == "out":
            return recClean(json["in"][0])

        if dType == "effect":
                child = recClean(dChildren[0])
                params = dData["params"]

                return {dData["effectName"] : dict([(k, recClean(params[k])) for k in params.keys()]+[("points", child)])}

        if dType == "mix":
            percent = recClean(dData["percent"]) if type(dData["percent"]) == dict else {"num" : float(dData["percent"]) / 100}
            value0 = recClean(dData["value0"])
            value1 = recClean(dData["value1"])

            #auto parse
            #return dict([k,recClean(v)] for k,v in dData)

            return {"mix" : 
                    {
                        "percent": percent,
                        "value0": value0,
                        "value1": value1
                    }
                }

        if dType == "bezier":
            return {"bezier": dData["points"]}

        if dType == "value":
            return {"num" : float(dData["value"])}

        if dType == "envelope":
            child = recClean(dChildren[0])
            #a,d,r are in ms, s is a percentage
            #convert these to seconds and fraction
            adsr = [float(dData["attack"])/1000, float(dData["decay"])/1000, float(dData["sustain"])/100, float(dData["release"])/1000]
            # adsr = [convertToNumber(v) for _,v in dData]

            return {
                "envelope" : {
                    "points" : child, 
                    "adsr" : {"list" : adsr}
                }
            }

        if dType == "oscillator": 
            return {"wave": dict([k,dData[k]] if k == "shape" else [k, recClean(dData[k])] for k in dData.keys())}

        if dType == "operation":
            return {("+" if dData["opType"] == "sum" else "*") : [recClean(child) for child in dChildren]}

    soundTree = recClean(recTree["output0"])

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
                data = data["adsr"]["list"]
                time = sum([data[0], data[1], data[3]])
                a.append(time)
            elif type(data) == dict:
                a.append(recFindEnv(data))
            else:
                return 0

        return max(a)

    envelopeTime = recFindEnv(soundTree)

    panTree = {"num": float(recTree["output0"]["data"]["pan"])/100} if type(recTree["output0"]["data"]["pan"]) != dict else recClean(recTree["output0"]["data"]["pan"])

    print("pantree\n",panTree)
    print("\nsoundtree\n",soundTree)
    print("")

    #do not add panning if pan percent is set to 0.5
    if not ("num" in panTree and panTree["num"] == 0.5):
        soundTree = {"pan" : { 
            "percent" : panTree, 
            "points" : soundTree
        }}

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
