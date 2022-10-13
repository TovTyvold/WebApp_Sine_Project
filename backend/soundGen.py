import numpy as np
import struct
import pyaudio
import pointsCalculation
from typing import List

samplesCount = 44100

class ChunkedBytes:
    bytesRead = 0
    b = bytes()

    def __init__(self, b : bytes):
        self.b = b

    def readChunk(self, size):
        out = self.b[self.bytesRead : self.bytesRead + size]
        self.bytesRead += size
        return out

    def empty(self):
        return len(self.b) <= self.bytesRead

def play(samples):
    samples = samplesToCB(samples)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
            channels=1,
            rate=samplesCount,
            output=True)

    while not samples.empty():
        stream.write(samples.readChunk(1024))

    stream.stop_stream()
    stream.close()

    p.terminate()

def samplesToCB(samples : List[float]) -> ChunkedBytes:
    return ChunkedBytes(struct.pack("%sf" % len(samples), *samples))