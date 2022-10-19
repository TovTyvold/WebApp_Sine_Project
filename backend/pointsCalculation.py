import math
from enum import Enum
from typing import List
import random
import ADSR_mod
import functools
import soundGen
import pointsNoise
import filterAudio
import envelope
import operator
import bezierCurve


def square(x: float) -> float:
    return 2 * (2 * math.floor(x) - math.floor(2 * x) + 1 - 0.5)


def saw(x: float) -> float:
    return 2 * (x % 1) - 1


def sin(x: float) -> float:
    return math.sin(2 * math.pi * x)


def triangle(x: float) -> float:
    return (4 * abs(x - math.floor(x + 0.75) + 0.25) - 1)


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


def noteToFreq(note: str) -> float:
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


def genSamples(samples: int, seconds: float):
    return [i / samples for i in range(int(seconds * samples))]

def advSine(amplFunction, freqFunction, samples, seconds):
    offsets = [0]*seconds*samples
    for i in range(1,samples*seconds):
        fp = freqFunction((i-1)/samples)
        fn = freqFunction(i/samples)
        offsets[i] = 2*math.pi*(i/samples)*(fp-fn)

    #compute prefix sum
    for i in range(1,samples*seconds):
        offsets[i] += offsets[i-1]

    ypoints = [0]*seconds*samples
    for i in range(samples*seconds):
        x = i/samples
        ypoints[i] = amplFunction(x)*math.sin(2*math.pi*freqFunction(x)*x + offsets[i])

    return ypoints

def advSinePoints(ampls, freqs, samples, seconds, func=sin):
    offsets = [0]*seconds*samples
    for i in range(1,samples*seconds):
        fp = freqs[i-1]
        fn = freqs[i]
        offsets[i] = (i/samples)*(fp-fn)

    #compute prefix sum
    for i in range(1,samples*seconds):
        offsets[i] += offsets[i-1]

    ypoints = [0]*seconds*samples
    for i in range(samples*seconds):
        x = i/samples

        ypoints[i] = ampls[i]*func(freqs[i]*x + offsets[i])

    return ypoints

def newparse(data: dict, samples, seconds) -> List[float]:
    #TODO generate the xpoints here, and let recParse use them rather than generating them
    strToOp = {
        "+" : operator.add,
        "*" : operator.mul,
    }
    def recParse(data: dict) -> List[float]:
        for k in data.keys():
            v = data[k]

            if k == "wave":
                func = conversionTable[v["shape"]]
                (amplT, amplV) = recParse(v["amplitude"])
                (freqT, freqV) = recParse(v["frequency"])

                #xsamples = genSamples(samples, seconds)
                #ampls = bezierCurve.compositeOn(envelope.getSymmEnv([1,1,1,1], 0.75, xsamples[0], xsamples[-1]), xsamples)

                ampls = [amplV]*samples*seconds if amplT == "num" else amplV
                freqs = [freqV]*samples*seconds if freqT == "num" else freqV
        
                ypoints = advSinePoints(ampls, freqs, samples, seconds, func = func)
                return ("points", ypoints)

            if k == "bezier":  # v = [(1,1),(2,1),(3,2)]
                xsamples = genSamples(samples, seconds)
                return ("points", bezierCurve.compositeOn(v, xsamples))

            if k == "num":
                return ("num", v)

            if k == "+" or k == "*":
                l = [recParse(f) for f in v] # [("num", 1), ("num", 2), ("points", [1,2,3])]
                
                #if input is all one dim numbers then just sum
                if all([t=="num" for t,_ in l]):
                    return ("num", functools.reduce(strToOp[k], ([v for _, v in l])))

                l = [[v]*samples*seconds if t == "num" else v for (t, v) in l] #[[1,1,1], [2,2,2], [1,2,3]]
                ypoints = list(functools.reduce(
                    lambda xs, ys: map(strToOp[k], xs, ys), l)
                )

                return ("points", ypoints)

            if k == "mix":
                (percentT, percentV) = recParse(v["percent"]) #function on x with values from 0 to 1 
                (v1t, v1v) = recParse(v["v1"]) #v1 if percent 0
                (v2t, v2v) = recParse(v["v2"]) #v2 if percent 1, interpolate inbetween
                percents = [percentV]*samples*seconds if percentT == "num" else percentV
                v1s = [v1v]*samples*seconds if v1t == "num" else v1v
                v2s = [v2v]*samples*seconds if v2t == "num" else v2v

                ypoints = []
                for i in range(len(percents)):
                    percent = percents[i]
                    v1 = v1s[i]
                    v2 = v2s[i]
                    val = (1-percent)*v1 + percent*v2
                    ypoints.append(val)

                return ("points", ypoints)

            if k == "str":
                return ("str", v)
                    
            # note = {
            #     "mix" : {
            #         "percent" : {
            #             "lerp": [(0, 0), (0.5, 0.5), (1, 1)],
            #         },
            #         "v1" : { "str" : "sin"},
            #         "v2" : { "str" : "square"},
            #     }
            # }



        raise Exception("Unknown key: " + k)

    #normalize input
    ypoints = recParse(data)[1]
    yMax = max(ypoints)
    ypoints = [y / yMax for y in ypoints]

    return ypoints
             
#TODO: save some envelopes so that they don't need to be recomputed all the time
#       maybe the 5? most recent
#dataTypes: num, points
#functions: +[], noise(points), envelope(points, list[int]), wave
#parse AST given by data generating point samples
def parse(data: dict, samples, seconds) -> List[float]:
    for k in data.keys():
        v = data[k]

        #TODO amplitude should possibly be a function,
        # this would then do the same as envelope
        if k == "wave":
            func = conversionTable[v["shape"]]
            ampl = v["amplitude"]
            freq = v["frequency"]

            xpoints = genSamples(samples, seconds)
            ypoints = list(map(lambda x: func(ampl, freq, x), xpoints))
            return ypoints

        if k == "advwave":
            func = conversionTable[v["shape"]]
            ampl = parse(v["amplitude"], samples, seconds)
            freq = parse(v["frequency"], samples, seconds)

            xpoints = genSamples(samples, seconds)
    
            # freqFunction = lambda x : freq + params[0]*math.sin(params[1]*math.pi*2*x)
            # return advSine(lambda x : 1,  freqFunction, samples, seconds)

            if freq[0] == "func": 
                ypoints = advSine(lambda x : 1, freq[1], samples, seconds)
            else:
                ypoints = list(map(lambda x : func(ampl, freq, x), xpoints))

            ypoints = list(map(lambda a : a*ampl, ypoints))

            return ypoints

        if k == "bezier":  # v = [1,2,3,4,5]
            return ("func", bezierCurve.compositeFunc(v))

        #TODO make this take another wave as an argument
        if k == "vibrato":
            w = v["wave"]
            func = conversionTable[w["shape"]]
            ampl = w["amplitude"]
            freq = w["frequency"]

            params = parse(v["args"], samples, seconds)
    
            freqFunction = lambda x : freq + params[0]*math.sin(params[1]*math.pi*2*x)
            return advSine(lambda x : 1,  freqFunction, samples, seconds)
        
        if k == "glissando":
            w = v["wave"]
            func = conversionTable[w["shape"]]
            ampl = w["amplitude"]
            freq = w["frequency"]

            #toFreq, inTime
            params = parse(v["args"], samples, seconds) 

            f0, f1 = freq, params[0]
            freqFunction = lambda x : f0 if x < 1 else (f1-f0)*(x-1) + f0 if x < 2 else f1 
            return advSine(lambda x : 1,  freqFunction, samples, seconds)
        
        if k == "envelope":
            points = parse(v["points"], samples, seconds)
            adsr = parse(v["numbers"], samples, seconds)
            adsrSum = sum(adsr)
            adsr = list(map(lambda x: (x/adsrSum)*seconds, adsr))

            #return ADSR_mod.ADSR(points, adsr, int(samples*seconds), sustainAmplitude=0.5, maxAmplitude=1)
            return envelope.symmetricEnvelope(adsr, genSamples(samples, seconds), points, 0.75)

        if k == "noise":
            params = parse(v["numbers"], samples, seconds)
            return pointsNoise.coloredNoise(parse(v["points"], samples, seconds), params[0], params[1], params[2])

        if k == "num":
            return v

        if k == "reverb":
            params = parse(v["numbers"], samples, seconds)
            return filterAudio.reverb_filter(parse(v["points"], samples, seconds), params[0], params[1])

        if k == "list":
            return [parse(num, samples, seconds) for num in v]

        if k == "+":
            l = ([parse(f, samples, seconds) for f in data[k]])

            ypoints = list(functools.reduce(
                lambda xs, ys: map(lambda x, y: x+y, xs, ys), l))
            yMax = max(ypoints)
            ypoints = [y / yMax for y in list(ypoints)]

            return ypoints


def freqToSamples(freq):
    return {'+': [
        {'envelope':
            {
                'points': {'wave': {'shape': 'sin', 'frequency': freq, 'amplitude': 15}},
                'numbers': {'list': [
                    {'num': 100}, 
                    {'num': 200}, 
                    {'num': 50}, 
                    {'num': 100}
                ]}
            }
         }
    ]}


def noteNameToSamples(note):
    freq = noteToFreq(note)

    return freqToSamples(freq)


#generate samples for imperial march from star wars
def starWars():
    def noteToSound(p): 
        return parse(noteNameToSamples(p[0]), 44100, p[1])

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
    # soundGen.play(starWars())
    
    note1 = {
        "wave": {
            "shape": "sin",
            "frequency": {
                "+": [
                    {"*": [
                        {"bezier": envelope.getSymmEnv([1, 1, 1, 1], 0.75, 0, 4)},
                        {"num": 440}
                    ]},
                    {"num": 220}
                ]
            }, 
            "amplitude": {
                "+": [
                    {"wave": {"shape": "sin", "frequency": {"num": 5}, "amplitude": {"num": 0.5}}},
                    {"num": 0.5}
                ]
            }
        },
    }
    soundGen.play(newparse(note1, 44100, 4))

    note2 = {
        "wave": {
            "shape": "sin",
            "frequency": {
                "+": [
                    {"wave": {"shape": "sin", "frequency": {"num": 2}, "amplitude": {"num": 20}}},
                    {"num": 440}
                ]
            }, 
            "amplitude": {
                "+": [
#                    {"wave": {"shape": "sin", "frequency": {"num": 5}, "amplitude": {"num": 0.5}}},
                    {"num": 0.5}
                ]
            }
        },
    }
    soundGen.play(newparse(note2, 44100, 4))


    w1 = {"wave": {"shape": "sin", "frequency": {"num": 440}, "amplitude": {"num": 1}}}
    w2 = {"wave": {"shape": "triangle", "frequency": {"num": 440}, "amplitude": {"num": 1}}}
    mixT = {
        "mix" : {
            "percent" : {
                # "+" : [
                #     {"wave": {"shape": "sin", "frequency": {"num": 1}, "amplitude": {"num": 0.5}}},
                #     {"num" : 0.5},
                # ]
                "bezier": [(1, 0), (2, 0.5), (3, 1)],
            },
            "v1": w1,
            "v2": w2,
        }
    }
    soundGen.play(newparse(mixT, 44100, 4))

    mixT = {
        "mix" : {
            "percent" : {
                # "+" : [
                #     {"wave": {"shape": "sin", "frequency": {"num": 1}, "amplitude": {"num": 0.5}}},
                #     {"num" : 0.5},
                # ]
                "bezier": [(1, 0), (3, 0.5), (5, 1)],
            },
            "v1": note1,
            "v2": note2,
        }
    }
    soundGen.play(newparse(mixT, 44100, 6))
