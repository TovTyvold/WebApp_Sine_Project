from asyncio.windows_events import INFINITE
from operator import mod
from re import A
import uvicorn

from typing import List, Optional, Dict, Union
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

def handleInput(query):
    #query is a (V,E) pair
    nodes = query["nodes"]
    edges = query["edges"]

    recTree = list(map(lambda a : {a["id"] : {**a, "in" : []}}, nodes))
    recTree = dict((key, d[key]) for d in recTree for key in d)

    sustainTime = recTree["output0"]["data"]["sustainTime"]

    for e in edges:
        _, source = e["sourceHandle"].split("-")
        tpos, target = e["targetHandle"].split("-")
        source = source
        target = target

        if tpos == "in":
            recTree[target][tpos].append(recTree[source])
        else:
            recTree[target]["data"][tpos] = recTree[source]

    #convert the recurisve node format from the frontend into an AST 
    #json should be constant and not changed by this function.
    def recClean(json:dict) -> dict:
        dType = json["type"]
        dData = json["data"]
        dChildren = json["in"]

        if dType == "out":
            return recClean(json["in"][0])

        if dType == "effect":
                child = recClean(dChildren[0])

                if dData["effectName"] == "reverb":
                    duration = float(dData["params"]["duration"])
                    wetdry = float(dData["params"]["mixPercent"])

                    return {
                        "reverb" : {
                            "points" : child,
                            "duration": {"num":  duration},
                            "wetdry": {"num": wetdry},
                        }
                    }

                if dData["effectName"] in ["lpf", "hpf"]:
                    cutoff = float(dData["params"]["cutoff"])

                    return {
                        dData["effectName"] : {
                            "points" : child,
                            "cutoff" : {"num": cutoff},
                        }
                    }

                if dData["effectName"] in ["lfo-sin", "lfo-saw"]:
                    rate = float(dData["params"]["rate"])

                    return {
                        dData["effectName"] : {
                            "points" : child,
                            "rate" : {"num": rate},
                        }
                    }

                if dData["effectName"] == "dirac":
                    precision = float(dData["params"]["precision"])
                    rate = float(dData["params"]["rate"])

                    return {
                        "dirac" : {
                            "points" : child,
                            "rate" : {"num": rate},
                            "precision" : {"num": precision},
                        }
                    }

                if dData["effectName"] == "dirac":
                    level = float(dData["params"]["level"])

                    return {
                        "dirac" : {
                            "points" : child,
                            "level" : {"num": level},
                        }
                    }

        if dType == "mix":
            percent = recClean(dData["percent"]) if type(dData["percent"]) == dict else {"num" : float(dData["percent"]) / 100}
            value0 = recClean(dData["value0"]) if type(dData["value0"]) == dict else {"num" : float(dData["value0"])}
            value1 = recClean(dData["value1"]) if type(dData["value1"]) == dict else {"num" : float(dData["value1"])}

            return {"mix" : 
                {
                    "percent": percent,
                    "value0": value0,
                    "value1": value1
                }
            }

        if dType == "pan":
            percent = recClean(dData["percent"]) if type(dData["percent"]) == dict else {"num" : float(dData["percent"]) / 100}
            points = recClean(dData["points"]) 

            return {"pan" : 
                {
                    "percent": percent,
                    "points": points
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
            # adsr = [float(f) for f in dData.values()]

            return {
                "envelope" : {
                    "points" : child, 
                    "adsr" : {"list" : adsr}
                }
            }

        if dType == "oscillator": 
            data = {}
            for dk in dData.keys():
                if dk in ["frequency", "amplitude"]:
                    if type(dData[dk]) == dict:
                        data[dk] = recClean(dData[dk]) 
                        # dData[dk] = recClean(dData[dk]) 
                    else:
                        data[dk] = {"num" : float(dData[dk])}

            if "shape" not in dData:
                data["shape"] = "sin"
            else:
                data["shape"] = dData["shape"]


            return {"wave" : data}

        if dType == "operation":
            return {("+" if dData["opType"] == "sum" else "*") : [recClean(child) for child in dChildren]}

    recTree = recClean(recTree["output0"])

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

    #find topmost envelope and output its combined length in ms
    envelopeTime = 0 #largest envelope in ms
    for node in nodes:
        if node["type"] == "envelope":
            data = node["data"]
            time = sum(map(lambda a : float(a), [data["attack"] , data["decay"] , data["release"]]))
            if (time > envelopeTime):
                envelopeTime = time

    return recTree, sustainTime, envelopeTime


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

            print("processesing: \n", query)
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
