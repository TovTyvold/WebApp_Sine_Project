from typing import Dict, List, Union, Optional
import math
import functools

sines = {"+": [
    {"sin": {"ampl" : 2, "freq": 1}},
    {"sin": {"ampl" : 5, "freq": 3}},
]}

operators = ["-", "+", "x"]
terminals = ['0','1','2','3','4','5','6','7','8','9']
def parseStr(w : str) -> str:
    output = ""
    currOP = ""
    v1 = ""
    v2 = ""
    reading = True
    for i in range(len(w)):
        if w[i] in terminals:
            if reading:
                v1 += w[i]
            else:
                v2 += w[i]

        if w[i] in operators:
            if currOP is "":
                output += "{" + currOP + "(" + v1 + ", " + v2 + ")" + "}"
                reading = False
            currOP = w[i]
            reading = False


    return output
            

def add(v1,v2):
    return v1+v2

def mult(v1,v2):
    return v1*v2

strToFunc = {
    "+" : add,
    "*" : mult,
}

def parse(math : dict) -> int:
    #one operand
    if (len(math.keys()) == 1):
        k = list(math.keys())[0]
        if (k == "num"):
            return math[k]
        elif (k == "neg"):
            return -parse(math[k])

    #multiple operands
    for operation in math.keys():
        operands = math[operation]
        func = strToFunc[operation]
        
        s = 0
        s += func(parse(operands[0]), parse(operands[1]))

        for i in range(2, len(operands)):
            s = func(s, parse(operands[i]))

        return s

mathexpr = {
    "+": [ #num type
        {"+": [ #num type
            {"num": 1},
            {"num": 2},
        ]},
        {"neg": 
            {"*": [ #num type
                {"num": 2},
                {"num": 5},
            ]}
        }
    ]
}

print(parse(mathexpr))


#parse sine functions + : [ "sin", "sin" ] -> point list 
