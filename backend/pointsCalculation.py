import math
from enum import Enum
from typing import Union, List, Tuple
import random
import ADSR_mod
import functools

def square(amplitude: float,  frequency: float, x: float) -> float:
    return 2 * amplitude * (2 * math.floor(frequency * x) - math.floor(2 * frequency * x) + 1 - 0.5)

def saw(amplitude: float,  frequency: float, x: float) -> float:
    return 2 * amplitude * frequency * (x % (1 / frequency)) - 1

def sin(amplitude: float,  frequency: float, x: float) -> float:
    return amplitude * math.sin(2 * math.pi * frequency * x)

def triangle(amplitude: float,  frequency: float, x: float) -> float:
    return amplitude * (4 * abs(frequency * x - math.floor(frequency * x + 0.75) + 0.25) - 1)

def whitenoise(amplitude: float) -> float:
    return 2*amplitude*(random.random()-0.5)

class WaveType(Enum):
    SIN = sin
    SQUARE = square
    SAW = saw
    TRIANGLE = triangle

conversionTable = {
    "sin": WaveType.SIN,
    "square": WaveType.SQUARE,
    "saw": WaveType.SAW,
    "triangle": WaveType.TRIANGLE,
}

class PeriodicFunc:
    shape: str
    amplitude: float
    frequency: float

    def __init__(self, shape, amplitude, frequency):
        self.shape = shape
        self.amplitude = amplitude
        self.frequency = frequency
  
def parseDict(d):
    shape = d["shape"]
    amplitude = d["amplitude"]
    frequency = d["frequency"]
    return PeriodicFunc(shape, amplitude, frequency)

def getPoints(funcs : List[PeriodicFunc], sampleRate: int, debug: bool = False, seconds : float = 1.0) -> Tuple[List[float], List[float]]:
    xpoints: List[float] = []
    ypoints: List[float] = []
    maxval: float = 0

    for i in range(0, int(sampleRate * seconds)):
        #-1 to get 0th and 1th value
        #both of which will be =0
        xsample : float = i / (sampleRate-1) 
        ysample : float = 0

        for func in funcs:
            ysample += conversionTable[func.shape](func.amplitude, func.frequency, xsample)
        
        if ysample > maxval:
            maxval = ysample

        xpoints.append(xsample)
        ypoints.append(ysample)

    #normalisation
    ypoints = [y/maxval for y in ypoints]
    
    if (debug):
        for p in zip(xpoints, ypoints):
            print(str(p[0]) + ", " + str(p[1]))

    #points is sampleRate long
    return (xpoints, ypoints)


samples = 10

def genSamples(sampleCount : int, seconds : float):
    return [i / sampleCount for i in range(int(seconds * sampleCount))]

def parseSine(data : dict) -> List[float]:
    for k in data.keys():
        v = data[k]
        if k == "wave": #-> points
            func = conversionTable[v["shape"]]
            #def square(amplitude: float, frequency: int, x: float) -> float:
            ampl = v["amplitude"]
            freq = v["frequency"]
            xpoints = genSamples(samples, 1.0)
            return (map(lambda x : func(ampl, freq, x), xpoints))

        if k == "envelope": #points, A,D,S,R -> points
            points = parseSine(v["points"])
            A = parseSine(v["A"])
            D = parseSine(v["D"])
            S = parseSine(v["S"])
            R = parseSine(v["R"])
            return points

        if k == "num": # -> num
            return v

        if k == "+": # points, points, ... -> points
            l = ([parseSine(f) for f in data[k]] )
            return list(functools.reduce(lambda xs, ys: map(lambda x, y: x+y, xs, ys), l))


if __name__ == "__main__":
    l = parseSine({"+":
                   [
                       {
                           "envelope": {
                               "points": {
                                   "+": [
                                       {"wave": {"shape": "sin",
                                                 "frequency": 1, "amplitude": 1}},
                                       {"wave": {"shape": "sin",
                                                 "frequency": 1, "amplitude": 1}}
                                   ],
                               },
                               "A": {
                                   "num": 1
                               },
                               "D": {
                                   "num": 1
                               },
                               "S": {
                                   "num": 1
                               },
                               "R": {
                                   "num": 1
                               }
                           }
                       },
                       {
                           "wave": {
                               "shape": "sin", "frequency": 3, "amplitude": 2
                           }
                       }
                   ]
                   })

    for i in range(10):
        print("(" + str(i/10) + ", " + str(l[i]) + ")")

    #def getPoints(funcs : List[PeriodicFunc], sampleRate: int, debug: bool = False, seconds : float = 1.0) -> Tuple[List[float], List[float]]:
    points = getPoints([parseDict({"shape": "sin", "frequency": 2, "amplitude": 1})], 100, debug = False, seconds = 4)
    points = (points[0], ADSR_mod.ADSR(points[1], [1,1,1,1], 100*4, sustainAmplitude=0.7, maxAmplitude=1))
    
    for p in zip(*points):
        print(str(p[0]) + ", " + str(p[1]))