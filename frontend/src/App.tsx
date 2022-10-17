//App.tsx
import './App.css';
import React, { useState, useEffect } from 'react';
import Graph from './components/Graph';
import Oscillator from './components/Oscillator';
import EnvelopeADSR from './components/EnvelopeADSR';

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

let channels = 1;
let bytesRead = 0;
const frameCount = 44100;

const API_WS = 'ws://localhost:5000/sound';

let ws = new WebSocket(API_WS);
ws.binaryType = 'arraybuffer';
const context = new AudioContext();

function App() {
  // Hooks
  const [dataPoints, setDataPoints] = useState([]);
  const [inputValues, setInputValues] = useState<Wave[]>([defaultInput]);

  useEffect(() => {
    // Reopen socket if closed
    if (ws.readyState === 3) {
      ws = new WebSocket(API_WS);
      ws.binaryType = 'arraybuffer';
    }

    ws.onmessage = (message: any) => {
      const data = message.data;
      data instanceof ArrayBuffer
        ? composeAudio(data)
        : setDataPoints(JSON.parse(data).points);
    };
  });

  const buffer = new AudioBuffer({
    numberOfChannels: channels,
    length: frameCount,
    sampleRate: 44100,
  });

  function composeAudio(data: any) {
    const chunk = new Float32Array(data);

    if (data instanceof ArrayBuffer) {
      for (let i = 0; i < chunk.length; i++) {
        buffer.getChannelData(0)[i + bytesRead] = chunk[i];
      }
      bytesRead += chunk.length;
    } else {
      console.log(data);
    }
  }

  function playAudio() {
    const source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(context.destination);
    source.start();
    source.onended = () => {
      console.log('Sound is done playing!');
    };

    bytesRead = 0;
  }

  const handleInputChange = (
    index: number,
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.currentTarget;
    let val: number | string = value;
    if (name !== 'shape') {
      val = parseFloat(value);
    }
    const list: any = [...inputValues];
    if (
      name === 'attack' ||
      name === 'decay' ||
      name === 'sustain' ||
      name === 'release'
    ) {
      const adsr = 'adsr';
      switch (name) {
        case 'attack':
          list[index][adsr][0] = val;
          break;
        case 'decay':
          list[index][adsr][1] = val;
          break;
        case 'sustain':
          list[index][adsr][2] = val;
          break;
        case 'release':
          list[index][adsr][3] = val;
          break;
        default:
          console.log('Error: name is incorrect');
      }
    } else {
      list[index][name] = val;
    }
    setInputValues(list);
  };

  const addInput = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const newInput: Wave = {
      frequency: undefined,
      amplitude: undefined,
      shape: '',
      adsr: [1, 1, 3, 1],
    };
    setInputValues([...inputValues, newInput]);
  };

  const removeInput = (
    index: number,
    e: React.MouseEvent<HTMLButtonElement>
  ) => {
    e.preventDefault();
    let list = [...inputValues];
    list.splice(index, 1);
    setInputValues(list);
  };

  const submit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(inputValues);
    const payload: any = {
      funcs: inputValues,
    };
    ws.send(JSON.stringify(payload));
  };

  return (
    <div className='App'>
      <div className='container'>
        <header>
          <h1>Wave Generator</h1>
        </header>
        <section className='graph-section'>
          <Graph data={dataPoints} />
        </section>

        <form className='inputs-section' onSubmit={submit}>
          {inputValues.map((element, index) => {
            return (
              <div key={index} className='oscillator'>
                <Oscillator
                  element={element}
                  index={index}
                  handleInputChange={handleInputChange}
                  removeInput={removeInput}
                />
                <EnvelopeADSR
                  element={element}
                  index={index}
                  handleInputChange={handleInputChange}
                />
                <br />
              </div>
            );
          })}
          <button className='add-input-button' onClick={(e) => addInput(e)}>
            Add
          </button>
          <br />
          <button className='submit-button' type='submit'>
            Generate
          </button>
        </form>

        <button className='play-button' onClick={playAudio}>
          Play
        </button>
      </div>
    </div>
  );
}

export default App;

//TODO
// Add sound length, couple to framecount
// Figure out alternative to 'Generate' button
// Quadratic bezier visual input for envelope
// FFT frequency visualizer?
