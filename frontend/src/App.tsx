//App.tsx
import './App.css';
import { useState, useEffect, useRef } from 'react';
import Flow from './Flow';
import exp from 'constants';

const API_WS = 'ws://localhost:5000/sound';
const webSocket = new WebSocket(API_WS);
const context = new AudioContext();

//TODO: make AudioBufferSourceNode per CHUNK size https://stackoverflow.com/questions/28440262/web-audio-api-for-live-streaming
function App() {
  // Hooks
  // const [buffer, setBuffer] = useState<AudioBuffer>(dBuffer);
  const [ws, setWs] = useState<WebSocket>(webSocket);
  const [tree, setTree] = useState<Object>();
  const floatsRead = useRef<number>(0);
  const expectedSampleCount = useRef<number>();
  const startTime = useRef<number>(0.0);
  const seconds = useRef<number>(2.0);
  const buffer = useRef<AudioBuffer>();
  const [isReady, setIsReady] = useState<boolean>(false)

  const composeAudio = (data: any, startTime: any) => {
    const chunk = new Float32Array(data);
    if (floatsRead.current == 0) {
      startTime.current = context.currentTime;
      console.log("hellu")
    }

    let tmpBuff = new AudioBuffer({
      numberOfChannels: 1,
      length: chunk.length,
      sampleRate: 44100
    })
    tmpBuff.copyToChannel(chunk, 0, 0);

    const source = context.createBufferSource();
    source.buffer = tmpBuff
    source.connect(context.destination);
    source.start(startTime.current + floatsRead.current/44100);
    source.onended = () => {console.log("done")}

    console.log("time ",startTime.current + floatsRead.current/44100)

    floatsRead.current += chunk.length;
    if (floatsRead.current == expectedSampleCount.current) {
      floatsRead.current = 0
      console.log("recv all")
    }
  };

  const handleInput = (event: any) => {
    if (event.data instanceof ArrayBuffer) {
      if (expectedSampleCount.current) {
        composeAudio(event.data, buffer);
      }
    } 
    else {
      expectedSampleCount.current = JSON.parse(event.data).SampleCount;
      console.log(expectedSampleCount.current)
    }
  }

  //fix ws
  useEffect(() => {
    const onClose = () => {
      setTimeout(() => {
        setWs(new WebSocket(API_WS));
      }, 1000);
    };

    ws.binaryType = "arraybuffer";
    ws.onmessage = (event: MessageEvent) => {
      handleInput(event);
    };
    ws.addEventListener("close", onClose);
    //ws.onopen = () => (console.log(ws))

    return () => {
      ws.removeEventListener("close", onClose)
      ws.close(1000)
    }
  }, [ws, setWs]);

  //when a tree is ready send it
  useEffect(() => {
    if (ws.readyState === webSocket.OPEN && tree && !isReady) {
      const payload = { NodeTree: tree, SustainTime: seconds.current };
      ws.send(JSON.stringify(payload));
    }
  }, [ws, tree]);

  useEffect(() => {
    if (isReady) {
      // playAudio();
    }
  }, [isReady]);

  const onSecondsChange = (event: any) => {
    event.preventDefault();

    seconds.current = (event.target.value);
  };

  const submit = (tree: any) => {
    setTree(tree);
  };

  return (
    <div className='App'>
      <div className='container'>
        <header>
          <h1>W.O.K.</h1>
        </header>

        <div
          style={{
            width: '80vw',
            height: '70vh',
            border: '2px #1f939e solid',
            borderRadius: '10px',
          }}>
          <Flow submit={submit} onSecondsChange={onSecondsChange} />
        </div>
      </div>
    </div>
  );
}

export default App;

// TODO
// Move Replay button
// Make slider component
// Frequency visualizer?
