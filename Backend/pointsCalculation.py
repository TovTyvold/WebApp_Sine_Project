import math

def getPoints(freqs: list, sampleRate: int, debug: bool = False) -> list:
    points = []
    maxval = 0
    for i in range(0, sampleRate):
        xsample = i / sampleRate

        ysample = 0
        for freq in freqs:
            ysample += math.sin(2*math.pi*freq*xsample);
        
        if ysample > maxval:
            maxval = ysample

        points.append((xsample, ysample))

    points = [(a, b/maxval) for (a, b) in points];

    if (debug):
        for p in points:
            print('{:.6}'.format(p[0]) + ", " +('{:.6}'.format(p[1])))

    return points