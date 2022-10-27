from re import L
import numpy as np
import struct
import pyaudio
import pointsCalculation
import functools
from typing import List, Tuple, Union

samplesCount = 44100

class ChunkedBytes:
    bytesRead = 0
    b = bytes()

    def __init__(self, b: bytes):
        self.b = b

    def readChunk(self, size):
        out = self.b[self.bytesRead: self.bytesRead + size]
        self.bytesRead += size
        return out

    def empty(self):
        return len(self.b) <= self.bytesRead


def play(samples, dim=1):
    cachedS = samplesToCB(samples)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=dim,
                    rate=samplesCount,
                    output=True)

    while not cachedS.empty():
        stream.write(cachedS.readChunk(1024))

    stream.stop_stream()
    stream.close()

    p.terminate()

#if samples is multidimensional then interleave the datapoints
#i.e. ([l0,l1,l2], [r0,r1,r2]) -> [l0,r0,l1,r1,l2,r2, ...]
def samplesToCB(samples: Union[List[float], Tuple]) -> ChunkedBytes:
    if type(samples) is tuple:
        samples = list(zip(*samples))
        samples = [lr for pair in samples for lr in pair]

    arraybytes = struct.pack("%sf" % len(samples), *samples)
    return ChunkedBytes(arraybytes)


if __name__ == "__main__":
    #test multi-channel input
    play((pointsCalculation.parse(pointsCalculation.noteNameToSamples("C6"), samples=44100, seconds=5),
          pointsCalculation.parse(pointsCalculation.noteNameToSamples("C#4"), samples=44100, seconds=5)),
         dim=2)
