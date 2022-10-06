import math

def getPoints(freqs: list, ampls: list, sampleRate: int, debug: bool = False) -> list:
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
            
            ysample += ampl*math.sin(2*math.pi*freq*xsample)
        
        if ysample > maxval:
            maxval = ysample

        points.append((xsample, ysample))

    #normalisation
    points = [(a, b/maxval) for (a, b) in points]

    if (debug):
        for p in points:
            print('{:.6}'.format(p[0]) + ", " +('{:.6}'.format(p[1])))

    return points