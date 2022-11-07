//App.tsx
import './App.css';
import { useState, useEffect, useRef } from 'react';
import Flow from './Flow';
import BarGraphVisualizer from './components/BarGraphVisualizer';
import OscilloscopeVisualizer from './components/OscilloscopeVisualizer';

const API_WS = 'ws://localhost:5000/sound';
const webSocket = new WebSocket(API_WS);
const context = new AudioContext();

//TODO: make AudioBufferSourceNode per CHUNK size https://stackoverflow.com/questions/28440262/web-audio-api-for-live-streaming
function App() {
  // Hooks
  const [ws, setWs] = useState<WebSocket>(webSocket);
  const [tree, setTree] = useState<Object>();
  const floatsRead = useRef<number>(0);
  const expectedSampleCount = useRef<number>();
  const channels = useRef<number>(1);
  const buffer = useRef<AudioBuffer>();
  const [isReady, setIsReady] = useState<boolean>(false);
  const source = useRef<AudioBufferSourceNode>(context.createBufferSource());
  const [visToggle, setVisToggle] = useState(true);

  //when a tree is ready send it
  useEffect(() => {
    if (ws.readyState === webSocket.OPEN && tree && !isReady) {
      console.log(JSON.stringify(tree, null, 2));
      ws.send(JSON.stringify(tree));
    }
  }, [ws, tree]);

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

    return () => {
      ws.removeEventListener('close', onClose);
      ws.close(1000);
    };
  }, [ws, setWs]);

  useEffect(() => {
    if (isReady) playAudio();
  }, [isReady]);

  const composeAudio = (data: any, buffer: any) => {
    const chunk = new Float32Array(data);
    for (let ch = 0; ch < channels.current; ch++) {
      for (let i = 0; i < chunk.length / channels.current; i++) {
        buffer.current.getChannelData(ch)[
          Math.floor(floatsRead.current / channels.current) + i
        ] = chunk[channels.current * i + (ch % channels.current)];
      }
    }
    floatsRead.current += chunk.length;

    if (floatsRead.current >= channels.current * buffer.current.length) {
      if (!isReady) {
        setIsReady(true);
      }
    }
  };

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

  const handleInput = (event: MessageEvent) => {
    if (event.data instanceof ArrayBuffer) {
      if (expectedSampleCount.current) {
        composeAudio(event.data, buffer);
      }
    } else {
      const format = JSON.parse(event.data);
      expectedSampleCount.current = format.SampleCount;
      channels.current = format.Channels;

      console.log(expectedSampleCount.current, channels.current);

      if (expectedSampleCount.current) {
        buffer.current = new AudioBuffer({
          numberOfChannels: channels.current,
          length: expectedSampleCount.current,
          sampleRate: 44100,
        });
      }
    }
  };

  const submit = (tree: Object) => {
    setTree(tree);
  };

  return (
    <div className='App'>
      <header>
        <h1>W.O.K.</h1>
      </header>
      <main>
        <section
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}>
          {visToggle ? (
            <OscilloscopeVisualizer
              audioCtx={context}
              audioSrc={source.current}
            />
          ) : (
            <BarGraphVisualizer audioCtx={context} audioSrc={source.current} />
          )}
          <button
            style={{
              color: 'white',
              backgroundColor: '#1f939e',
              border: '2px #1f939e solid',
              width: '130px',
              padding: '3px',
              margin: '0.5rem',
              borderRadius: '10px',
            }}
            onClick={(e: any) => {
              e.preventDefault();
              setVisToggle(!visToggle);
            }}>
            {visToggle ? 'Frequency Graph' : 'Oscilloscope'}
          </button>
        </section>

        <section
          style={{
            width: '80vw',
            height: '65vh',
            border: '2px #1f939e solid',
            borderRadius: '10px',
          }}>
          <Flow submit={submit} />
        </section>
      </main>
    </div>
  );
}

export default App;
