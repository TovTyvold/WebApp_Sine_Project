import numpy as np
import ctypes
import pyaudio
import pointsCalculation

p = pyaudio.PyAudio()

volume = 0.5
fs = 44100
duration = 1.0
f = 4*440

samplesCount = 44100
harmonics = 1

ampls = []
freqs = []
#for i in range(1,harmonics+1):
#    ampls.append(440 * 1.0/(2.0*f*i))
#    freqs.append(440 * f*i)

ampls = [1 for _ in range(harmonics)]
freqs = [440]

samples = [volume*b for (_,b) in pointsCalculation.getPoints(freqs, ampls, ["sin" for _ in range(harmonics)], samplesCount, debug=False)]
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