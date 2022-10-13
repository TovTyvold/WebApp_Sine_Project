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


#define response model for post
class PointsAnswer(BaseModel):
    points: List[Dict[str, float]]


#define input model for waves
class FreqQuery(BaseModel):
    funcs: List[Dict[str, Union[float, str, List[float]]]]
    seconds: Optional[float] = 1.0
    samples: Optional[int] = 400

    class Config:
        schema_extra = {
            "example": {
                "funcs": [{"shape": "sin", "frequency": 2, "amplitude": 1, "adsr": [1, 1, 1, 1]}],
                "seconds": 1.0,
                "samples": 400
            }
        }


#query contains information about signal length, desired samples, and functions with envelopes
#convert this to AST data to be parsed in pointsCalculation
def BuildAST(query: Dict, samples: int, seconds: float, debug=False, doEnvelope=True):
    l = []
    if doEnvelope:
        for func in query["funcs"]:
            l.append({"envelope": {
                "points": {
                    "wave": {
                        "shape": func["shape"],
                        "frequency": func["frequency"],
                        "amplitude": func["amplitude"]
                    },
                },
                "numbers": {
                    "list": [{"num": v} for v in ([1, 3, 1, 1] if "adsl" not in func or func["adsl"] == None else func["adsl"])]
                }
            }})
    else:
        for func in query["funcs"]:
            l.append({"wave": {
                "shape": func["shape"], "frequency": func["frequency"], "amplitude": func["amplitude"]
            }})

    d = {"+": l}

    if debug:
        print(d)

    return pointsCalculation.parse(d, samples, seconds)

#samples and seconds are optional, fill the data points if they are missing
def handleMissing(query: Dict):
    query["samples"] = 44100 if "samples" not in query else query["samples"]
    query["seconds"] = 1 if "seconds" not in query else query["seconds"]

    return query


@app.post("/points", response_model=PointsAnswer)
async def getPoints(query: FreqQuery):
    query = handleMissing(query)
    ypoints = BuildAST(
        query.dict(),  query["samples"], query["seconds"], debug=True, doEnvelope=False)
    xpoints = pointsCalculation.genSamples(query["samples"], query["seconds"])

    return {"points": [{"x": x, "y": y} for (x, y) in zip(xpoints, ypoints)]}

chunkSize = 1024
@app.websocket("/sound")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    #recieve wave information
    query = await websocket.receive_json()
    query = handleMissing(query)

    #generate points to be displayed,
    #dividing the frequencies by freqWindow
    freqWindow = 200
    modQuery = copy.deepcopy(query)
    for f in modQuery["funcs"]:
        f["frequency"] /= freqWindow

    xpoints = pointsCalculation.genSamples(400, 1)
    ypoints = BuildAST(modQuery, 400, 1.0, debug=False, doEnvelope=False)

    displayData = {"points": [{"x": x, "y": y}
                              for (x, y) in list(zip(xpoints, ypoints))]}
    await websocket.send_json(displayData)

    #get soundData
    soundData = BuildAST(
        query, query["samples"], query["seconds"], debug=True)
    cb = soundGen.samplesToCB(soundData)

    #send chunkSize chunks of the sounddata until all is sent
    data = cb.readChunk(chunkSize)
    while data:
        await websocket.send_bytes(data)
        data = cb.readChunk(chunkSize)

    await websocket.close()

if __name__ == "__main__":
    config = uvicorn.Config("apiServer:app", port=5000,
                           
                            log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()

