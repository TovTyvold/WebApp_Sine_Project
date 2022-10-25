//App.tsx
import './App.css';
import React, { useState, useEffect, useRef, useCallback } from 'react';
import Flow from './Flow';
import NumberInput from './components/NumberInput';
import Graph from './components/Graph';
import Oscillator from './components/Oscillator';
import EnvelopeADSR from './components/EnvelopeADSR';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import { Socket } from 'dgram';

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
  length: 44100 * 1,
  sampleRate: 44100,
});

const API_WS = 'ws://localhost:5000/sound';
const webSocket = new WebSocket(API_WS);
const context = new AudioContext();

function App() {
  // Hooks
  const [buffer, setBuffer] = useState<AudioBuffer>(dBuffer);
  const [ws, setWs] = useState<WebSocket>(webSocket);
  const [tree, setTree] = useState<Object>();
  const bytesRead = useRef<number>(0);
  const seconds = useRef<number>(1);
  const [isReady, setIsReady] = useState<boolean>(false);

  const composeAudio = useCallback(
    (data: any) => {
      setIsReady(true);
      if (data instanceof ArrayBuffer) {
        const chunk = new Float32Array(data);
        buffer.copyToChannel(chunk, 0, bytesRead.current);
        bytesRead.current += chunk.length;
      }
    },
    [buffer]
  );

  //fix ws
  useEffect(() => {
    const onClose = () => {
      setTimeout(() => {
        setWs(new WebSocket(API_WS));
        console.log(ws);
      }, 1000);
    };

    ws.binaryType = 'arraybuffer';
    ws.onmessage = (event: MessageEvent) => {
      composeAudio(event.data);
    };
    ws.addEventListener('close', onClose);
    //ws.onopen = () => (console.log(ws))

    // return () => {
    //     ws.removeEventListener("close", onClose)
    // }
  }, [ws, setWs, composeAudio]);

  //when a tree is ready send it
  useEffect(() => {
    if (ws.readyState === webSocket.OPEN && tree) {
      const payload = { NodeTree: tree, Seconds: seconds.current };
      console.log(JSON.stringify(payload, null, 2));
      ws.send(JSON.stringify(payload));
    }
  }, [ws, tree]);

  useEffect(() => {
    if (isReady) {
      playAudio();
    }
  }, [isReady]);

  const onSecondsChange = useCallback(
    (event: any) => {
      event.preventDefault();

      seconds.current = event.target.value;
      setBuffer(
        new AudioBuffer({
          numberOfChannels: CHANNELS,
          length: 44100 * seconds.current,
          sampleRate: 44100,
        })
      );
    },
    [setBuffer]
  );

  const playAudio = useCallback(() => {
    if (buffer) {
      const source = context.createBufferSource();
      source.buffer = buffer;
      source.connect(context.destination);
      source.start();
      source.onended = () => {
        console.log('Sound is done playing!');
        setIsReady(false);
      };

      bytesRead.current = 0;
    }
  }, [buffer]);

  const sanitize = (tree: any) => {
    Object.keys(tree).forEach((key) => {
      let keep: boolean = desiredFields.includes(key);

      if (!keep) {
        delete tree[key];
      }
      if (tree['children']) {
        tree['children'].forEach((child: any) => {
          sanitize(child);
        });
      }
    });

    return tree;
  };

  let submit = (tree: any) => {
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

          <button onClick={playAudio}>play</button>
        </div>
      </div>

      {/* <BezierEditor
        onChange={() => (console.log("a"))}
        xAxisLabel="Time Percentage"
        yAxisLabel="Progress Percentage"
      /> */}

      {/* <form className='inputs-section' onSubmit={submit}>
          <Button className='submit-button' variant='contained' type='submit'>
            Generate
          </Button>
          {inputValues.map((element, index) => {
            return (
              <div key={index} className='oscillator'>
                <Oscillator
                  element={element}
                  index={index}
                  onChange={handleInputChange}
                  removeInput={removeInput}
                />
                <EnvelopeADSR
                  element={element}
                  index={index}
                  onChange={handleInputChange}
                />
                <br />
              </div>
            );
          })}

          <br />
        </form>
        <Button
          className='add-input-button'
          variant='outlined'
          onClick={(e) => addInput(e)}>
          <AddIcon />
        </Button>

        <Button variant='contained' className='play-button' onClick={playAudio}>
          Play
        </Button> */}
    </div>
  );
}

export default App;

// TODO
// Move Replay button
// Make slider component
// Frequency visualizer?
