import bezierCurve

#percentages above 0.5 yields superlinear, under yields sublinear, equal yields linear
#adsr: array of 4 with attack duration, decay duration, sustain duration and release duration
def symmetricEnvelope(adsr, xsamples, ysamples, percent):
    (A,D,S,R) = adsr
    susLevel = 0.6

    l = [(xsamples[0], 0), (A*percent, (1-percent)), (A, 1), (A+D*(1-percent), susLevel + (1-percent)*(1-susLevel)),
         (A+D, susLevel), (A+D+S*0.5, susLevel), (A+D+S, susLevel), (A+D+S+R*(1-percent), (1-percent)*susLevel), (xsamples[-1], 0)]

    bz = list(map(bezierCurve.compositeFunc(l), xsamples))

    return list(map(lambda a,b : a*b, ysamples, bz))

def getSymmEnv(adsr, percent, first, final):
    (A,D,S,R) = adsr
    susLevel = 0.6

    l = [(first, 0), (A*percent, (1-percent)), (A, 1), (A+D*(1-percent), susLevel + (1-percent)*(1-susLevel)),
         (A+D, susLevel), (A+D+S*0.5, susLevel), (A+D+S, susLevel), (A+D+S+R*(1-percent), (1-percent)*susLevel), (final, 0)]
    return l

if __name__ == "__main__":
    samples = 20
    adsr = [1,1,1,1]
    seconds = sum(adsr)

    totSamples = int(samples*seconds)+1
    xsamples = [i/samples for i in range(totSamples)]

    for (x, y) in zip(xsamples, symmetricEnvelope(adsr, xsamples, [1]*totSamples, 0.75)):
        print(str(x) + ", " + str(y))
