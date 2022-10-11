import asyncio
import pyaudio
from websockets import connect

# Initialize PyAudio
p = pyaudio.PyAudio()

async def hello(uri):
    async with connect(uri) as websocket:
        sampleCount = int(await websocket.recv())

        stream = p.open(format = pyaudio.paFloat32,
                        channels = 1,
                        rate = sampleCount,
                        output = True)

        message = await websocket.recv()
        while message:
            stream.write(message)
            message = await websocket.recv()
            if message == "SIGNAL STREAM END":
                break
        await(websocket.close())

asyncio.run(hello("ws://localhost:5000/sound"))