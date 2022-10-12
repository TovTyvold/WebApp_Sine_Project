import asyncio
import pyaudio
import json
from websockets import connect

# Initialize PyAudio
p = pyaudio.PyAudio()

async def hello(uri):
    async with connect(uri) as websocket:
        waveData = json.dumps({
            "funcs": [
                {
                    "shape": "sin",
                    "frequency": 440,
                    "amplitude": 1
                },
                {
                    "shape": "sin",
                    "frequency": 2*440,
                    "amplitude": 1/6
                },
                {
                    "shape": "sin",
                    "frequency": 3*440,
                    "amplitude": 1/10
                },
            ]
        })
        await websocket.send(waveData)

        stream = p.open(format = pyaudio.paFloat32,
                        channels = 1,
                        rate = 44100,
                        output = True)

        message = await websocket.recv()
        while message:
            stream.write(message)
            message = await websocket.recv()
            if message == "SIGNAL STREAM END":
                break
        await websocket.close()

asyncio.run(hello("ws://localhost:5000/sound"))