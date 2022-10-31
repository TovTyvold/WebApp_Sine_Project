//App.tsx
import './App.css';
import { useState, useEffect, useRef } from 'react';
import Flow from './Flow';

type Wave = {
  frequency: number | undefined;
  amplitude: number | undefined;
  shape: string;
  adsr?: number[];
};

const defaultInput: Wave = {
  frequency: 440,
  amplitude: 1,
  shape: 'sin',
  adsr: [1, 1, 3, 1],
};

const desiredFields = ['id', 'type', 'data', 'children'];

const CHANNELS = 1;
const dBuffer = new AudioBuffer({
  numberOfChannels: CHANNELS,
  length: 44100 * 2,
  sampleRate: 44100,
});

const API_WS = 'ws://localhost:5000/sound';
const webSocket = new WebSocket(API_WS);
const context = new AudioContext();

//const source = context.createBufferSource();

//TODO: make AudioBufferSourceNode per CHUNK size https://stackoverflow.com/questions/28440262/web-audio-api-for-live-streaming
function App() {
  // Hooks
  // const [buffer, setBuffer] = useState<AudioBuffer>(dBuffer);
  const [ws, setWs] = useState<WebSocket>(webSocket);
  const [tree, setTree] = useState<Object>();
  const floatsRead = useRef<number>(0);
  const expectedSampleCount = useRef<number>();
  const channels = useRef<number>(1);
  const buffer = useRef<AudioBuffer>();
  const [isReady, setIsReady] = useState<boolean>(false);
  const source = useRef<AudioBufferSourceNode>(context.createBufferSource());


  const composeAudio = (data: any, buffer: any) => {
    const chunk = new Float32Array(data);
    for (let ch = 0; ch < channels.current; ch++) {
      for (let i = 0; i < chunk.length / channels.current; i++) {
        buffer.current.getChannelData(ch)[Math.floor(floatsRead.current / channels.current) + i] = chunk[channels.current * i + ch % channels.current];
      }
    }

    floatsRead.current += chunk.length;

    console.log(buffer.current.length)
    if (floatsRead.current >= channels.current*buffer.current.length) {
      if (!isReady) {
        setIsReady(true);
      }
    }
  };

  const handleInput = (event: any) => {
    if (event.data instanceof ArrayBuffer) {
      if (expectedSampleCount.current) {
        composeAudio(event.data, buffer);
      }
    } 
    else {
      const format = JSON.parse(event.data)
      expectedSampleCount.current = format.SampleCount;
      channels.current = format.Channels;

      console.log(expectedSampleCount.current, channels.current)

      if (expectedSampleCount.current) {
        buffer.current = (
          new AudioBuffer({
            numberOfChannels: channels.current,
            length: expectedSampleCount.current,
            sampleRate: 44100,
          })
        );
      }
    }
  };

  //fix ws
  useEffect(() => {
    const onClose = () => {
      setTimeout(() => {
        setWs(new WebSocket(API_WS));
      }, 1000);
    };

    ws.binaryType = 'arraybuffer';
    ws.onmessage = (event: MessageEvent) => {
      handleInput(event);
    };
    ws.addEventListener('close', onClose);
    //ws.onopen = () => (console.log(ws))

    return () => {
      ws.removeEventListener("close", onClose)
      ws.close(1000)
    }
  }, [ws, setWs]);

  //when a tree is ready send it
  useEffect(() => {
    if (ws.readyState === webSocket.OPEN && tree && !isReady) {
      ws.send(JSON.stringify(tree));
    }
  }, [ws, tree]);

  useEffect(() => {
    if (isReady) {
      playAudio();
    }
  }, [isReady]);

  const playAudio = () => {
    if (buffer) {
      if (buffer.current) {
        const src = source.current;
        src.buffer = buffer.current;
        src.connect(context.destination);
        src.onended = () => {
          console.log('Sound is done playing!');
          setIsReady(false);
        };
        src.start();
        source.current = context.createBufferSource();
        floatsRead.current = 0;
      }
    }
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
          <Flow submit={submit} />
        </div>
      </div>
    </div>
  );
}

export default App;
