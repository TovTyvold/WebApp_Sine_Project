import math
from enum import Enum
from typing import Union, List, Tuple
import random
import ADSR_mod
import functools
import soundGen

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

notes = {"C": 0,
         "C#": 1,
         "Db": 1,
         "D": 2,
         "D#": 3,
         "Eb": 3,
         "E": 4,
         "E#": 5,
         "F": 5,
         "F#": 6,
         "Gb": 6,
         "G": 7,
         "G#": 8,
         "Ab": 8,
         "A": 9,
         "A#": 10,
         "Bb": 10,
         "B": 11}

def noteToFreq(note : str) -> float:
    noteName = ""
    pitch = ""
    for c in note:
        if c.isdecimal():
            pitch += c
        else:
            noteName += c

    stepsAway = notes[noteName] + (int(pitch) - 4) * 12

    cPitch = 440.0*math.pow((math.pow(2.0, 1.0/12.0)), -9)

    return cPitch*math.pow((math.pow(2.0, 1.0/12.0)), stepsAway)

#Deprecated, use parse
class PeriodicFunc:
    shape: str
    amplitude: float
    frequency: float

    def __init__(self, shape, amplitude, frequency, adsr):
        self.shape = shape
        self.amplitude = amplitude
        self.frequency = frequency
  
#Deprecated, use parse
def parseDict(d):
    shape = d["shape"]
    amplitude = d["amplitude"]
    frequency = d["frequency"]
    adsr = d["adsr"]
    return PeriodicFunc(shape, amplitude, frequency, adsr)

#Deprecated, use parse
def getPoints(funcs : List[PeriodicFunc], sampleRate: int, debug: bool = False, seconds : float = 1.0, adsr = None) -> Tuple[List[float], List[float]]:
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

def genSamples(sampleCount : int, seconds : float):
    return [i / sampleCount for i in range(int(seconds * sampleCount))]


#dataTypes: num, points
#functions: +[], noise(points), envelope(points, list[int]), wave

#parse AST given by data generating point samples
def parse(data : dict, samples, seconds) -> List[float]:
    for k in data.keys():
        v = data[k]

        if k == "wave": #-> points
            func = conversionTable[v["shape"]]
            ampl = v["amplitude"]
            freq = v["frequency"]

            xpoints = genSamples(samples, seconds)
            ypoints = list(map(lambda x : func(ampl, freq, x), xpoints))
            return ypoints

        if k == "envelope": #points, A,D,S,R -> points
            points = parse(v["points"], samples, seconds)
            adsr = parse(v["numbers"], samples, seconds)
            adsrSum = sum(adsr)
            adsr = list(map(lambda x : (x/adsrSum)*seconds, adsr))
            return ADSR_mod.ADSR(points, adsr, int(samples*seconds))

        if k == "noise":
            coloredNoise = lambda x : x
            params = parse(v["numbers"], samples, seconds)
            return coloredNoise(v)

        if k == "num": # -> num
            return v
        
        if k == "list":
            return [parse(num, samples, seconds) for num in v]

        if k == "+": # points, points, ... -> points
            l = ([parse(f, samples, seconds) for f in data[k]] )

            ypoints = list(functools.reduce(lambda xs, ys: map(lambda x, y: x+y, xs, ys), l))
            yMax = max(ypoints)
            ypoints = [y / yMax for y in list(ypoints)]
            return ypoints


l = {"+": [
        {"noise" : { 
            "points": {"wave": {"shape": "sin", "frequency": 1, "amplitude": 5}},
            "numbers": {"list": [{"num": 2}]}
        }},
        {"wave": {"shape": "sin", "frequency": 2, "amplitude": 1}}
    ]
}

#generate samples for imperial march from star wars
def starWars():
    l = lambda note : {'+': [
        {'envelope': 
            {'points': {'wave': {'shape': 'sin', 'frequency': noteToFreq(note), 'amplitude': 15}}, 'numbers': {'list': [{'num': 1}, {'num': 1}, {'num': 5}, {'num': 1}]}}
        },
        {'envelope': 
            {'points': {'wave': {'shape': 'sin', 'frequency': 2*noteToFreq(note), 'amplitude': 3}}, 
            'numbers': {'list': [{'num': 1}, {'num': 1}, {'num': 5}, {'num': 1}]}}
        },
        {'envelope': 
            {'points': {'wave': {'shape': 'sin', 'frequency': 3*noteToFreq(note), 'amplitude': 1}}, 'numbers': {'list': [{'num': 1}, {'num': 1}, {'num': 5}, {'num': 1}]}}
        }
    ]}
    noteToSound = lambda p : parse(l(p[0]), 44100, p[1])

    completeSounds = []
    s = """
            G4,1 G4,1 G4,1 Eb4,0.75 Bb4,0.25
            G4,1 Eb4,0.75 A#4,0.25 G4,2 
            D5,1 D5,1 D5,1 Eb5,0.75 Bb4,0.25 
            F#4,1 Eb4,0.75 Bb4,0.25 G4,2
            G5,1 G4,0.75 G4,0.25 G5,1 F#5,0.75 F5,0.25
            E5,0.25 E5b,0.25 E5,0.5 D0,0.5 Ab4,0.5 Db5,1 C5,0.75 B4,0.25
            Bb4,0.25 A4,0.25 Bb4,0.5 D0,0.5 Eb4,0.5 F#4,1 Eb4,0.75 F#4,0.25
            Bb4,1 G4,0.75 Bb4,0.25 D5,2
            G5,1 G4,0.75 G4,0.25 G5,1 F#5,0.75 F5,0.25 
            E5,0.25 E5b,0.25 E5,0.5 D0,0.5 Ab4,0.5 Db5,1 C5,0.75 B4,0.25
            Bb4,0.25 Ab4,0.25 Bb4,0.5 D0,0.5 Eb4,0.5 F#4,1 Eb4,0.75 Bb4,0.25
            G4,1 Eb4,0.75 Bb4,0.25 G4,2
        """

    a = []
    for n in s.split(" "):
        if not (n == '\n' or n == ''):
            print(n)
            q = n.split(",")
            a.append((q[0], 0.66*float(q[1])))

    for p in a:
        completeSounds += noteToSound(p)

    return completeSounds

if __name__ == "__main__":
    soundGen.play(starWars())