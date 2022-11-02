import math
from enum import Enum
from os import stat_result
import time
from typing import Callable, List, Dict, Union
import random
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
    offsets = [0]*int(seconds*samples)
    for i in range(1, int(samples*seconds)):
        fp = freqFunction((i-1)/samples)
        fn = freqFunction(i/samples)
        offsets[i] = 2*math.pi*(i/samples)*(fp-fn)

    #compute prefix sum
    for i in range(1, int(samples*seconds)):
        offsets[i] += offsets[i-1]

    ypoints = [0]*int(seconds*samples)
    for i in range(int(samples*seconds)):
        x = i/samples
        ypoints[i] = amplFunction(
            x)*math.sin(2*math.pi*freqFunction(x)*x + offsets[i])

    return ypoints


def advSinePoints(ampls, freqs, samples, seconds, func=sin):
    #changing frequencies yielsd differnet phases,
    #this syncs them
    offsets = [0]*int(samples*seconds)
    for i in range(1, int(samples*seconds)):
        fp = freqs[i-1]
        fn = freqs[i]
        offsets[i] = (i/samples)*(fp-fn) + offsets[i-1]

    ypoints = [0]*int(samples*seconds)
    for i in range(int(samples*seconds)):
        x = i/samples

        ypoints[i] = ampls[i]*func(freqs[i]*x + offsets[i])

    return ypoints

def parse(data: dict, samples, sustainTime, envelopeTime) -> List[float]:
    #TODO generate the xpoints here, and let recParse use them rather than generating them
    seconds = envelopeTime + sustainTime
    xpoints = genSamples(samples, seconds)
    strToOp = {
        "+": operator.add,
        "*": operator.mul,
    }

    #turn a ("num", 1) into samples*seconds 1s, ie.. [1,1,1,1,1,1]
    def dimensionalise(p): return [p[1]] * \
        int(samples*seconds) if p[0] == "num" else p[1]

    #recursively parse the ast
    def recParse(data: dict) -> Dict[str, Union[List[float], Union[float, int]]]:
        for k in data.keys():
            v = data[k]

            if k == "reverb":
                _, points = recParse(v["points"])
                _, duration = recParse(v["duration"])
                _, mixPercent = recParse(v["mixPercent"]) #float in 0, 100
                return ("points", filterAudio.Rev_Conv_Filter(points, duration, mixPercent)[0])

            if k == "lpf":
                _, points = recParse(v["points"])
                _, cutoff = recParse(v["cutoff"])
                return ("points", filterAudio.low_pass_Filter(points, cutoff))

            if k == "hpf":
                _, points = recParse(v["points"])
                _, cutoff = recParse(v["cutoff"])
                return ("points", filterAudio.high_pass_Filter(points, cutoff))

            if k == "lfo-sin":
                _, points = recParse(v["points"])
                _, rate = recParse(v["rate"])
                return ("points", filterAudio.Low_frequency_Oscillator_sine(points, rate))

            if k == "lfo-saw":
                _, points = recParse(v["points"])
                _, rate = recParse(v["rate"])
                return ("points", filterAudio.Low_frequency_Oscillator_saw(points, rate))

            if k == "dirac":
                _, points = recParse(v["points"])
                _, precision = recParse(v["precision"])
                _, rate = recParse(v["rate"])
                return ("points", filterAudio.dirac_comb_discrete(points, int(precision), int(rate)))

            if k == "wave":
                func = conversionTable[v["shape"]]
                (amplT, amplV) = recParse(v["amplitude"])
                (freqT, freqV) = recParse(v["frequency"])

                ampls = dimensionalise((amplT, amplV))
                freqs = dimensionalise((freqT, freqV))

                ypoints = advSinePoints(
                    ampls, freqs, samples, seconds, func=func)
                return ("points", ypoints)

            if k == "bezier":  # v = [(1,1),(2,1),(3,2)]
                return ("points", bezierCurve.compositeOn(v, xpoints))

            if k == "num":
                return ("num", v)

            if k == "list":
                return ("list", v)

            #pan = {percent : {}, points : {}}
            if k == "pan":
                percents = dimensionalise(recParse(v["percent"]))
                (_, points) = recParse(v["points"])

                points0 = [(1-per)*poi for per,poi in zip(percents, points)]
                points1 = [per*poi for per,poi in zip(percents, points)]

                return ("stereopoints", [points0, points1])

            if k == "envelope":
                (_, wave) = recParse(v["points"])
                (_, attack) = recParse(v["attack"])
                (_, decay) = recParse(v["decay"])
                (_, sustain) = recParse(v["sustain"])
                (_, release) = recParse(v["release"])

                adsr = envelope.getSymmEnv([attack, decay, sustain, release], 0.75, 0, sustainTime + (attack+decay+release))

                ypoints = list(
                    map(operator.mul, bezierCurve.compositeOn(adsr, xpoints), wave))
                return ("points", ypoints)

            if k == "+" or k == "*":
                # [("num", 1), ("num", 2), ("points", [1,2,3])]
                l = [recParse(f) for f in v]

                #if input is all one dim numbers then just sum
                if all([t == "num" for t, _ in l]):
                    return ("num", functools.reduce(strToOp[k], ([v for _, v in l])))

                #[[1,1,1], [2,2,2], [1,2,3]]
                l = [[v]*int(samples*seconds) if t ==
                     "num" else v for (t, v) in l]
                ypoints = list(functools.reduce(
                    lambda xs, ys: map(strToOp[k], xs, ys), l)
                )

                return ("points", ypoints)

            if k == "mix":
                percents = dimensionalise(recParse(v["percent"]))
                #TODO throw error / warning if percents has values not in (0,1)
                v1s = dimensionalise(recParse(v["value0"]))
                v2s = dimensionalise(recParse(v["value1"]))

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

        raise Exception("Unknown key: " + k)

    #normalize input
    t, parseddata = recParse(data)
    if t == "points":
        ypoints = parseddata
        yMax = max(ypoints)
        ypoints = [y / yMax for y in ypoints]
        return ypoints, 1
    elif t == "stereopoints":
        ypoints0, ypoints1 = parseddata
        yMax0 = max(ypoints0)
        yMax1 = max(ypoints1)
        yMax = (yMax0 + yMax1)/2
        ypoints0 = [y / yMax for y in ypoints0]
        ypoints1 = [y / yMax for y in ypoints1]
        return (ypoints0, ypoints1), 2


def freqToProfile(freq):
    return {'envelope': 
        {'attack': {'num': 0.11}, 'decay': {'num': 0.129}, 'sustain': {'num': 0.6}, 'release': {'num': 0.375}, 'points': {'wave': {'frequency': {'num': freq}, 'amplitude': {'num': 1.0}, 'shape': 'sin'}}}
    }

def noteNumToSamples(noteNum: int) -> float:
    freq = 440.0*math.pow(2, (noteNum-69)/12)

    samples, _ = parse(freqToProfile(freq), 22100, 0.125, 0.129+0.375+0.11)

    return samples

def noteNameToSamples(note):
    freq = noteToFreq(note)

    return freqToProfile(freq)


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

class Generator:
    t: int = 0.0
    sampleRate: int = 44100
    func = lambda x, state: x
    state: dict = {}

    def __init__(self, profile:dict, sampleRate:int):
        self.sampleRate = sampleRate
        self.func = parseNote(profile)

    def get(self):
        y = self.func(self.t, self.state)
        self.t += 1.0 / self.sampleRate
        return y

def advSine(func, amplFunction, freqFunction, t, state):
    # return amplFunction(t, state)*func(freqFunction(t, state)*t)
    if freqFunction not in state:
        state[freqFunction] = {}

    po = state[freqFunction]["prevoffset"] if "prevoffset" in state[freqFunction] else 0
    pf = state[freqFunction]["prevfreq"] if "prevfreq" in state[freqFunction] else freqFunction(0, {})
    
    f = freqFunction(t, state)
    o = t*(pf-f) + po

    state[freqFunction]["prevoffset"] = o
    state[freqFunction]["prevfreq"] = f
    return amplFunction(t, state)*func(freqFunction(t, state)*t + o)

def parseNote(data: dict):
    def recParse(data: dict) -> Callable[[float, dict], float]:
        for k in data.keys(): #should only have one key
            v = data[k]

            if k == "wave":
                func = conversionTable[v["shape"]]
                ampl = recParse(v["amplitude"])
                freq = recParse(v["frequency"])

                return lambda t, state : advSine(func, ampl, freq, t, state)

            if k == "num":
                return lambda t, state : v

            if k == "f":
                return lambda t, state : t/v

            if k == "+":
                return lambda t, state : sum([recParse(operand)(t, state) for operand in v])
        raise Exception("Unknown key: " + k)
    return recParse(data)


if __name__ == "__main__":
    sampleRate = 44100
    profile = {"+": [
         {"wave": {"frequency": {"num": 440}, "amplitude": {"num": 1}, "shape": "sin"}},
        {"wave": {"frequency": {"num": 880}, "amplitude": {"num": 0.5}, "shape": "sin"}},
        {"wave": {"frequency": {"num": 1100}, "amplitude": {"num": 0.25}, "shape": "sin"}},
        {"wave": {"frequency": {"num": 1100}, "amplitude": {"num": 0.25}, "shape": "sin"}},
        {"wave": {"frequency": {"num": 1100}, "amplitude": {"num": 0.25}, "shape": "sin"}},
        {"wave": {"frequency": {"num": 1100}, "amplitude": {"num": 0.25}, "shape": "sin"}},
    ]}

    aprofile = {"+" : [{"wave": {"frequency": {"num": 1.5}, "amplitude": {"num": 2.5}, "shape": "sin"}}, {"num": 220}]}
    profile = {"wave": {"frequency": aprofile, "amplitude": {"num": 1}, "shape": "sin"}}
    # profile = {"wave": {"frequency": {"num": 220}, "amplitude": {"num": 1}, "shape": "sin"}}


    gen = Generator(profile, sampleRate)
    ypoints = []
    times = []
    t1 = time.time()
    for i in range(6*sampleRate):
        # print(i/sampleRate, ",", gen.get())
        t2 = time.time()
        ypoints.append(gen.get())
        t3 = time.time()

        times.append(t3-t2)
    t2 = time.time()
    print(t2-t1)
    print(44100 * sum(times)/len(times))
    # soundGen.play(ypoints)

    t1 = time.time()
    ypoints = parse(profile, 44100, 6, 0)[0]
    t2 = time.time()
    print(t2-t1)
    # soundGen.play(ypoints)