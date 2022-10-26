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

//TODO: make AudioBufferSourceNode per CHUNK size https://stackoverflow.com/questions/28440262/web-audio-api-for-live-streaming
function App() {
  // Hooks
  const [buffer, setBuffer] = useState<AudioBuffer>(dBuffer);
  const [ws, setWs] = useState<WebSocket>(webSocket);
  const [tree, setTree] = useState<Object>();
  const floatsRead = useRef<number>(0);
  const seconds = useRef<number>(1.0);
  const expectedSampleCount = useRef<number>();
  const [isReady, setIsReady] = useState<boolean>(false)

  const composeAudio = (data: any, samplesCount: number) => {
    const chunk = new Float32Array(data);
    buffer.copyToChannel(chunk, 0, floatsRead.current);
    floatsRead.current += chunk.length;

    if (floatsRead.current >= samplesCount) {
      if (!isReady) {
        setIsReady(true);
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
      if (event.data instanceof ArrayBuffer) {
        if (expectedSampleCount.current) {
          composeAudio(event.data, expectedSampleCount.current);
        }
      }
      else {
        expectedSampleCount.current = event.data
      }
    };
    ws.addEventListener('close', onClose);
    //ws.onopen = () => (console.log(ws))

    return () => {
      ws.removeEventListener("close", onClose)
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
      playAudio();
    }
  }, [isReady]);

  const onSecondsChange = (event: any) => {
    event.preventDefault();

    seconds.current = (event.target.value);
    setBuffer(
      new AudioBuffer({
        numberOfChannels: CHANNELS,
        length: 44100 * seconds.current,
        sampleRate: 44100,
      })
    );
  };

  const playAudio = () => {
    if (buffer) {
      const source = context.createBufferSource();
      source.buffer = buffer;
      source.connect(context.destination);
      source.onended = () => {
        console.log('Sound is done playing!');
        console.log('floats read', floatsRead.current);
        setIsReady(false);
      };
      source.start();

      floatsRead.current = 0;
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
