from json import JSONEncoder
from multiprocessing import allow_connection_pickling
from typing import List, Union, Optional
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
 
import pointsCalculation

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

class FreqQuery(BaseModel):
    samples: int
    freqs: List[int]
    ampls: Optional[List[int]]
    types: Optional[List[str]]

@app.post("/")
async def readPoints(query: FreqQuery):
    query.ampls = [1 for _ in range(len(query.freqs))] if (query.ampls == None) else query.ampls
    query.types = ["sin" for _ in range(len(query.freqs))] if (query.types == None) else query.types

    l = pointsCalculation.getPoints(query.freqs, query.ampls, query.types, query.samples)

    d = []
    for p in l:
        x = p[0]
        y = p[1]

        d.append({"x": x, "y": y})
    return d

if __name__ == "__main__":
    config = uvicorn.Config("fast:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()