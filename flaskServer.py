from flask import Flask, jsonify, request
import pointsCalculation

#disregard keys
def jsonDictToList(d: dict) -> list:
    return d.values()

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def handleInput():
    #input is a json dict containing samples (int) and freqs (lists of ints)
    json = request.get_json()
    try:
        samples = json["samples"]
        freqs = json["freqs"]
    except:
        return "input error", 400

    if samples <= 1 or not isinstance(samples, int):
        return "samples is not valid", 400

    if not isinstance(freqs, list) or len(freqs) == 0 or not all([isinstance(p, (int, float)) for p in freqs]):
        return "freqs is not valid", 400

    #output is a json list (samples long) of lists of size 2 e.g. [[1,2], [2,3], [1,2], [1,2]]
    return jsonify(pointsCalculation.getPoints(freqs, samples))

if __name__ == '__main__':
    #app.run(host="10.99.3.251", debug=True)
    app.run(debug=True)