from subprocess import ABOVE_NORMAL_PRIORITY_CLASS
import numpy as np
import ctypes
import pyaudio
import pointsCalculation

p = pyaudio.PyAudio()

volume = 0.5
fs = 44100
duration = 1.0
f = 4*440

samples = 44100
harmonics = 10

ampls = []
freqs = []
for i in range(1,harmonics+1):
    ampls.append(1.0/(2.0*f*i))
    freqs.append(f*i)

samples = [volume*b for (_,b) in pointsCalculation.getPoints(freqs, ampls, samples, debug=False)]
samples = np.array(samples).tobytes()

stream = p.open(format=pyaudio.paFloat32,
    channels=1,
    rate=fs,
    output=True)

while True:
    stream.write(samples)

stream.write(samples)

stream.stop_stream()
stream.close()

p.terminate()