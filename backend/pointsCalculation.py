import math

def square(ampl: int, freq: int, x: float) -> float:
    return 2*ampl*(2*math.floor(freq*x) - math.floor(2*freq*x)+1 - 0.5)

def saw(ampl: int, freq: int, x: float) -> float:
    return 2 * ampl * freq * (x % (1/freq))-1

def sin(ampl: int, freq: int, x: float) -> float:
    return ampl*math.sin(2*math.pi*freq*x)

def triangle(ampl: int, freq: int, x: float) -> float:
    return ampl*(4 * abs(freq*x - math.floor(freq*x + 0.75)+0.25) - 1)

typeToFunc = {
    "square": square,
    "saw": saw,
    "sin": sin,
    "triangle": triangle,
}

def getPoints(freqs: list, ampls: list, types:list, sampleRate: int, debug: bool = False) -> list:
    points = []
    maxval = 0
    for i in range(0, sampleRate):
        #-1 to get 0th and 1th value
        #both of which will be =0
        xsample = i / (sampleRate-1) 

        ysample = 0
        for j in range(len(freqs)):
            freq = freqs[j]
            ampl = ampls[j]

            ysample += typeToFunc[types[j]](ampl, freq, xsample)
        
        if ysample > maxval:
            maxval = ysample

        points.append((xsample, ysample))

    #normalisation
    points = [(a, b/maxval) for (a, b) in points]

    if (debug):
        for p in points:
            print('{:.6}'.format(p[0]) + ", " +('{:.6}'.format(p[1])))

    return points