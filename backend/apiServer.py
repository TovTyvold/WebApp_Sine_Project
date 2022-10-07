import uvicorn

from typing import List, Optional, Dict
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
 
import pointsCalculation

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
    samples: Optional[int]
    freqs: List[int]
    ampls: Optional[List[int]]
    types: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "samples": 10,
                "freqs": [1,3,5],
                "ampls": [5,3,1],
                "types": ["sin", "triangle", "saw"],
            }
        }

@app.post("/points", response_model=PointsAnswer)
async def getPoints(query: FreqQuery):
    query.samples = max(query.freqs)*400 if query.samples == None else query.samples

    query.ampls = [1 for _ in range(len(query.freqs))] if (query.ampls == None) else query.ampls
    query.types = ["sin" for _ in range(len(query.freqs))] if (query.types == None) else query.types

    types = [pointsCalculation.parse(s) for s in query.types]
    if None in types:
        raise HTTPException(status_code=412, detail="Type not recognized")

    if len(query.ampls) != len(query.freqs):
        raise HTTPException(status_code=400, detail="Length not matching")
            
    if len(query.types) != len(query.freqs):
        raise HTTPException(status_code=400, detail="Length not matching")

    #l is a list of pairs of points
    l = pointsCalculation.getPoints(query.freqs, query.ampls, types, query.samples, debug=True)

    #convert l to a dictionary
    d = []
    for p in l:
        x = p[0]
        y = p[1]

        d.append({"x": x, "y": y})

    return {"points": d}

if __name__ == "__main__":
    config = uvicorn.Config("apiServer:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()