import math
import ctypes
from enum import Enum
from typing import Union, List, Tuple
from pyaudio import paFloat32

def square(amplitude: float, frequency: int, x: float) -> float:
    return 2*amplitude*(2*math.floor(frequency*x) - math.floor(2*frequency*x)+1 - 0.5)

def saw(amplitude: float, frequency: int, x: float) -> float:
    return 2 * amplitude * frequency * (x % (1/frequency))-1

def sin(amplitude: float, frequency: int, x: float) -> float:
    return amplitude*math.sin(2*math.pi*frequency*x)

def triangle(amplitude: float, frequency: int, x: float) -> float:
    return amplitude*(4 * abs(frequency*x - math.floor(frequency*x + 0.75)+0.25) - 1)

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

def parse(s : str) -> Union[WaveType, None]:
    if s in conversionTable:
        return conversionTable[s]
    else:
        return None

class PeriodicFunc:
    shape: str
    amplitude: float
    frequency: int

    def __init__(self, shape, amplitude, frequency):
        self.shape = shape
        self.amplitude = amplitude
        self.frequency = frequency
  
def parseJSON(json):
    shape = json["shape"]
    amplitude = json["amplitude"]
    frequency = json["frequency"]
    return PeriodicFunc(shape, amplitude, frequency)

def getPoints(funcs : List[PeriodicFunc], sampleRate: int, debug: bool = False, seconds : float = 1.0) -> List[Tuple[float, float]]:
    points = []
    maxval = 0
    for i in range(0, int(sampleRate * seconds)):
        #-1 to get 0th and 1th value
        #both of which will be =0
        xsample : ctypes.c_float = i / (sampleRate-1) 

        ysample : ctypes.c_float = 0
        for func in funcs:
            ysample += conversionTable[func.shape](func.amplitude, func.frequency, xsample)
        
        if ysample > maxval:
            maxval = ysample

        points.append((xsample, ysample))

    #normalisation
    points = [(a, b/maxval) for (a, b) in points]

    if (debug):
        for p in points:
            print(str(p[0]) + ", " + str(p[1]))

    #points is sampleRate long
    return points