from pydantic import BaseModel

from typing import Optional, List

from flask_openapi3 import Info, Tag, ExtraRequestBody
from flask_openapi3 import OpenAPI

from flask import request

import pointsCalculation

info = Info(title="Sine API", version="1.0.0")
app = OpenAPI(__name__, info=info)

PointsTag = Tag(name="points", description="List of points")

FreqBody = ExtraRequestBody(
    description="Data containing the sinsoidal information",
    required=True,
)

class FreqQuery(BaseModel):
    samples: int
    freqs: List[int]
    types: Optional[List[str]]
    ampls: Optional[List[int]]

def pointsToOutput(l : list) -> str:
    output = "["
    for p in l:
        output += "{x:" + str(p[0]) + ", " + "y: " + str(p[1]) + "}, "
    output += "]"

    return output


@app.post('/points', tags=[PointsTag], extra_body=FreqBody)
def createPoints(body: FreqQuery):
    print(body.samples)
    print(pointsToOutput((pointsCalculation.getPoints(body.freqs, body.ampls, body.types, body.samples, debug=True))))

    #return (pointsCalculation.getPoints(body.freqs, body.ampls, body.types, body.samples, debug=True))
    return {"code": 0, "message": "ok"}

if __name__ == "__main__":
    app.run(debug=True)