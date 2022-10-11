import uvicorn

from typing import List, Optional, Dict, Union
from fastapi import FastAPI, Response, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
 
import pointsCalculation
import soundGen

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class PointsAnswer(BaseModel):
    points: List[Dict[str, float]]

    class Config:
        schema_extra = {
            "example": {
                "points": [
                    {
                        "x": 0.0,
                        "y": -0.18779169356732647
                    },
                    {
                        "x": 0.1111111111111111,
                        "y": 1.0
                    },
                    {
                        "x": 0.2222222222222222,
                        "y": 0.4030499856394059
                    },
                    {
                        "x": 0.3333333333333333,
                        "y": 0.8757591174341461
                    },
                    {
                        "x": 0.4444444444444444,
                        "y": 0.5923973782324737
                    },
                    {
                        "x": 0.5555555555555556,
                        "y": -0.5923973782324736
                    },
                    {
                        "x": 0.6666666666666666,
                        "y": -0.8757591174341461
                    },
                    {
                        "x": 0.7777777777777778,
                        "y": -0.4030499856394064
                    },
                    {
                        "x": 0.8888888888888888,
                        "y": -1.0000000000000004
                    },
                    {
                        "x": 1.0,
                        "y": 0.18779169356732614
                    }
                ]
            }
        }

class FreqQuery(BaseModel):
    funcs: List[Dict[ str, Union[float, int, str] ]]
    seconds: Optional[float] = 1.0
    samples: Optional[int] = 400

    class Config:
        schema_extra = {
            "example": { 
                "funcs" : [{"shape": "sin", "frequency": 2, "amplitude": 1}], 
                "seconds": 1.0,
                "samples": 400
            }
        }

@app.post("/points", response_model=PointsAnswer)
async def getPoints(query: FreqQuery):
    funcs = [pointsCalculation.parseJSON(func) for func in query.funcs]
    l = pointsCalculation.getPoints(funcs, query.samples, debug=True, seconds=query.seconds)

    #convert l to a dictionary
    d = []
    for p in l:
        x = p[0]
        y = p[1]

        d.append({"x": x, "y": y})

    return {"points": d}

chunkSize = 1024
samplesCount = 44100
@app.websocket("/sound")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    await websocket.send_text(str(samplesCount))

    cb = soundGen.samplesToCB([y for (_,y) in pointsCalculation.getPoints([ pointsCalculation.parseJSON({"shape" : "sin", "frequency" : 440, "amplitude" : 1}) ], 44100, debug=False)])
    data = cb.readChunk(chunkSize)
    while data:
        await websocket.send_bytes(data)
        data = cb.readChunk(chunkSize)

    await websocket.send_text("SIGNAL STREAM END")

    await websocket.close()

if __name__ == "__main__":
    config = uvicorn.Config("apiServer:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()