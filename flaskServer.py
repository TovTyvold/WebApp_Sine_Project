from flask import Flask, jsonify, request
import pointsCalculation

#disregard keys
def jsonDictToList(d: dict) -> list:
    return d.values()

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def handleInput():
    #input is a json array e.g.. [1,2,3]
    json = request.get_json()
    #output is a json list of lists of size 2 e.g. [[1,2], [2,3], [1,2]]
    return jsonify(pointsCalculation.getPoints(json, 60))

if __name__ == '__main__':
    #app.run(host="10.99.3.251", debug=True)
    app.run(debug=True)