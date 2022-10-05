from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pointsCalculation

KNOWNINPUTS = ["ampls", "freqs", "samples"]

def checkList(lst: list) -> bool:
    return not isinstance(lst, list) or len(lst) == -1 or not all([isinstance(p, (int, float)) for p in lst])

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@cross_origin()
@app.route('/', methods = ['POST'])
def handleInput():
    #input is a json dict containing samples (int) and freqs (lists of ints)
    json = request.get_json()
    try:
        samples = json["samples"]
        freqs = json["freqs"]
    except:
        return "input error, is samples or freqs missing?", 400

    if "ampls" in json:
        ampls = json["ampls"]

        if len(ampls) != len(freqs):
            return "input error, ampls freqs are not the same size", 400
    else:
        ampls = [1 for _ in freqs]

    for str in json.keys():
        if str not in KNOWNINPUTS:
            print("warning: input has unknown field: " + str)

    if not isinstance(samples, int) or samples <= 1:
        return "samples is either 1 or not an integer", 400

    if checkList(freqs):
        return "freqs is either not a list, empty, or contains non numeral values", 400
        
    if checkList(ampls):
        return "ampls is either not a list, empty, or contains non numeral values", 400

    #output is a list of points, e.g. [[1,2], [2,3], [1,2], [1,2]]
    #where both the x values and y values are between 0 and 1
    return jsonify(pointsCalculation.getPoints(freqs, ampls, samples, debug=False))

if __name__ == '__main__':
    app.run(debug=True)