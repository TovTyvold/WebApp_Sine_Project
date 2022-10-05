from flask import Flask, jsonify, request
import pointsCalculation

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def handleInput():
    #input is a json dict containing samples (int) and freqs (lists of ints)
    json = request.get_json()
    try:
        samples = json["samples"]
        freqs = json["freqs"]
    except:
        return "input error, is samples or freqs missing?", 400

    if len(json) > 2:
        print("warning: input has unknown fields")
        print(json.keys())

    if not isinstance(samples, int) or samples <= 1:
        return "samples is either 1 or not an integer", 400

    if not isinstance(freqs, list) or len(freqs) == 0 or not all([isinstance(p, (int, float)) for p in freqs]):
        return "freqs is either not a list, empty, or contains non numeral values", 400

    #output is a list of points, e.g. [[1,2], [2,3], [1,2], [1,2]]
    #where both the x values and y values are between 0 and 1
    return jsonify(pointsCalculation.getPoints(freqs, samples, debug=True))

if __name__ == '__main__':
    app.run(debug=True)