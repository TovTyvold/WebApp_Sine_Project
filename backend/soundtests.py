import wave

import uvicorn
import soundGen
import pointsCalculation
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

filename = r'C:\users\brage.bakkane\Desktop\Cantina.wav'
 
chunkSize = 1024 
app = FastAPI()

origins = ["http://localhost"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

harmonicCount = 2
samplesCount = 44100

ampls = [harmonicCount - i for i in range(harmonicCount)]
freqs = [440*i for i in range(harmonicCount)]

samples = [b for (_, b) in pointsCalculation.getPoints(freqs, ampls, [
    "sin" for _ in range(harmonicCount)], samplesCount, debug=False, seconds=1)]


@app.websocket("/sound")
async def websocket_endpoint(websocket : WebSocket):
    await websocket.accept()

    await websocket.send_text(str(samplesCount))

    cb = soundGen.samplesToCB(samples)
    data = cb.readChunk(chunkSize)
    while data:
        await websocket.send_bytes(data)
        data = cb.readChunk(chunkSize)

    await websocket.send_text("SIGNAL STREAM END")

    await websocket.close()

if __name__ == "__main__":
    config = uvicorn.Config("soundtests:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()