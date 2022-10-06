from email.headerregistry import ContentTypeHeader
from urllib import response
from pydantic import BaseModel

from typing import Optional, List, Dict

from flask_openapi3 import Info, Tag, ExtraRequestBody
from flask_openapi3 import OpenAPI, Encoding

from flask_cors import CORS, cross_origin

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

class FreqResponse(BaseModel):
    data: Dict[str, str]

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@cross_origin()
@app.post('/points', tags=[PointsTag], extra_body=FreqBody, responses={"200": FreqResponse})
#responses={"200": FreqResponse},
#    extra_responses={"200": {"content": {"text/csv": {"schema": {"type": "string"}}}}},
def createPoints(body: FreqQuery):
    if (body.types == None):
        body.types = ["sin" for _ in range(len(body.freqs))]
    if (body.ampls == None):
        body.ampls = [1 for _ in range(len(body.freqs))]


    res = (pointsToOutput((pointsCalculation.getPoints(body.freqs, body.ampls, body.types, body.samples, debug=True))))

    #return {"code": 0, "message": "ok", "data": res}
    return res

if __name__ == "__main__":
    app.run(debug=True)