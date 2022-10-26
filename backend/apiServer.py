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
                


    print(nodes)
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
        print(json)
        dData = json["data"]
        dType = json["type"]
        dId = json["id"]
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
                    "v1": value0,
                    "v2": value1
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

        if dType == "oscillator": #currently a leaf
            for dk in dData.keys():
                if dk in ["frequency", "amplitude"]:
                    if type(dData[dk]) == dict:
                        dData[dk] = recClean(dData[dk])
                    else:
                        dData[dk] = {"num" : float(dData[dk])}

            if "shape" not in dData:
                dData["shape"] = "sin"

            return {"wave" : dData}

        if dType == "operation":
            return {("+" if dData["opType"] == "sum" else "*") : [recClean(child) for child in dChildren]}

    adjList = recClean(adjList["output0"])


    # #{'envelope': {'points': {'wave': {'frequency': {'num': 200.0}, 'amplitude': {'num': 1.0}, 'shape': 'sin'}}, 'adsr': {'list': [1.0, 0.02, 1.0, 1.0]}}}
    # def recFindEnc(tree:dict):
    #     for key in tree.keys():
    #         if key == "envelope":
    #             time = sum(map(lambda a: float(a), [
    #                        data["attack"], data["decay"], data["release"]]))
    #             # tree[key]["adsr"]
    #             return time
    #     return tree


    #find topmost envelope and output its combined length in ms
    totalTime = 0 #largest envelope in ms
    for node in nodes:
        if node["type"] == "envelope":
            data = node["data"]
            time = sum(map(lambda a : float(a), [data["attack"] , data["decay"] , data["release"]]))
            if (time > totalTime):
                totalTime = time

    return adjList, totalTime


CHUNKSIZE = 1024
SAMPLES = 44100
@app.websocket("/sound")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while (True):
        #recieve wave information
        query = await websocket.receive_json()
        print(query)
        sustainTime = float(query["SustainTime"])
        query, envelopeTime = handleInput(query["NodeTree"])

        envelopeTime /= 1000
        print(query)
        print("totalTime: ", envelopeTime+sustainTime, "sustainTime:", sustainTime, "envelopeTime:", envelopeTime)

        soundData = pointsCalculation.newparse(query, SAMPLES, sustainTime, envelopeTime)

        await websocket.send_json(len(soundData))

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
