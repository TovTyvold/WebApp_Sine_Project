//App.tsx
import './App.css';
import React, { useState, useEffect } from 'react';
import Flow from './Flow';
import Graph from './components/Graph';
import Oscillator from './components/Oscillator';
import EnvelopeADSR from './components/EnvelopeADSR';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';

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
const frameCount = 44100;
let bytesRead = 0;

const API_WS = 'ws://localhost:5000/sound';

let ws = new WebSocket(API_WS);
ws.binaryType = 'arraybuffer';
const context = new AudioContext();

function App() {
  // Hooks
  const [dataPoints, setDataPoints] = useState([]);
  const [inputValues, setInputValues] = useState<Wave[]>([defaultInput]);

  useEffect(() => {
    ws.onmessage = (message: any) => {
      const data = message.data;
      console.log(data);
      data instanceof ArrayBuffer
        ? composeAudio(data)
        : setDataPoints(JSON.parse(data).points);
    };
  });

  const buffer = new AudioBuffer({
    numberOfChannels: CHANNELS,
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

  // const handleInputChange = (
  //   index: number,
  //   e: React.ChangeEvent<HTMLInputElement>
  // ) => {
  //   const { name, value } = e.currentTarget;
  //   let val: number | string = value;
  //   if (name !== 'shape') {
  //     val = parseFloat(value);
  //   }
  //   const list: any = [...inputValues];
  //   if (
  //     name === 'attack' ||
  //     name === 'decay' ||
  //     name === 'sustain' ||
  //     name === 'release'
  //   ) {
  //     const adsr = 'adsr';
  //     switch (name) {
  //       case 'attack':
  //         list[index][adsr][0] = val;
  //         break;
  //       case 'decay':
  //         list[index][adsr][1] = val;
  //         break;
  //       case 'sustain':
  //         list[index][adsr][2] = val;
  //         break;
  //       case 'release':
  //         list[index][adsr][3] = val;
  //         break;
  //       default:
  //         console.log('Error: name is incorrect');
  //     }
  //   } else {
  //     list[index][name] = val;
  //   }
  //   setInputValues(list);
  // };

  // const addInput = (e: React.MouseEvent<HTMLButtonElement>) => {
  //   e.preventDefault();
  //   const newInput: Wave = {
  //     frequency: undefined,
  //     amplitude: undefined,
  //     shape: '',
  //     adsr: [1, 1, 3, 1],
  //   };
  //   setInputValues([...inputValues, newInput]);
  // };

  // const removeInput = (
  //   index: number,
  //   e: React.MouseEvent<HTMLButtonElement>
  // ) => {
  //   e.preventDefault();
  //   let list = [...inputValues];
  //   list.splice(index, 1);
  //   setInputValues(list);
  // };

  // const submit = async (e: React.ChangeEvent<HTMLFormElement>) => {
  //   e.preventDefault();
  //   console.log(inputValues);
  //   const payload: any = {
  //     funcs: inputValues,
  //   };
  //   ws.send(JSON.stringify(payload));
  // };

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

  const submit = async (tree: any) => {
    const payload = sanitize(tree);
    console.log(JSON.stringify(payload, null, 2));
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
      <div
        style={{
          height: '880px',
          border: '1px #1f939e solid',
          marginBottom: '10rem',
        }}>
        <Flow submit={submit} />
        <button onClick={playAudio}>play</button>
      </div>
    </div>
  );
}

export default App;

// TODO
// Get flowchart to work with backend
// Add sound length, couple to framecount
// Figure out alternative to 'Generate' button
// Quadratic bezier visual input for envelope
// FFT frequency visualizer?
// Oscilliscope on oscillator node
