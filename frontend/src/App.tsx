//App.tsx
import "./App.css";
import React, { useState, useEffect, useRef } from "react";
import Graph from "./components/Graph";
import sendData from "./sendData";
import AddADSR from "./components/AddADSR";


type Wave = {
  frequency: number | undefined;
  amplitude: number | undefined;
  shape: string;
  attack: number;
  decay: number;
  sustain: number;
  release: number;
};

const defaultInput: Wave = {
  frequency: undefined,
  amplitude: undefined,
  shape: "",
  attack: 1,
  decay: 1,
  sustain: 3,
  release: 1,
};

const API_POINTS = "http://localhost:5000/points";
const API_WS = "ws://localhost:5000/sound";

let ws = new WebSocket(API_WS);
ws.binaryType = "arraybuffer";
const context = new AudioContext();

function App() {
  // Hooks
  const [dataPoints, setDataPoints] = useState([]);
  const [inputValues, setInputValues] = useState<Wave[]>([defaultInput]);

  let channels = 1;
  let bytesRead = 0;
  const frameCount = 44100;

  if (ws.readyState == 3) {
    ws = new WebSocket(API_WS);
    ws.binaryType = "arraybuffer";
  }

  useEffect(() => {
    ws.onmessage = (message: any) => {
      console.log(message.type);
      if (message.data instanceof ArrayBuffer) {
        composeAudio(message.data);
      } else {
        console.log(JSON.parse(message.data).points);
        setDataPoints(JSON.parse(message.data).points);
      }
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
      console.log("Sound is done playing!");
    };

    bytesRead = 0;
  }

  const handleInputChange = (
    index: number,
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.currentTarget;
    let val: any = value;
    if (name != "shape") {
      val = parseInt(value);
    }
    const list: any[] = [...inputValues];
    list[index][name] = val;
    setInputValues(list);
  };

  const addInput = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const newInput: Wave = {
      frequency: undefined,
      amplitude: undefined,
      shape: "",
      attack: 1,
      decay: 1,
      sustain: 3,
      release: 1,
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
    const payload: any = {
      funcs: inputValues,
    };
    ws.send(JSON.stringify(payload));
  };


  return (
    <div className='App'>
      <div className='container'>
        <header>Wave Generator</header>
        <section className='graph'>
          <Graph data={dataPoints} />
        </section>
        <div>
          <p style={{float:"left", width:"13.5%"}}><b>Frequency:</b></p>
          <p style={{float:"left", width:"13.5%"}}><b>Amplitude:</b></p>
          <p style={{float:"left", width:"13.5%"}}><b>Shape:</b></p>
          <p style={{float:"left", width:"13.5%"}}><b>Attack:</b></p>
          <p style={{float:"left", width:"13.5%"}}><b>Decay:</b></p>
          <p style={{float:"left", width:"13.5%"}}><b>Sustain:</b></p>
          <p style={{float:"left", width:"13.5%"}}><b>Release:</b></p>
        </div>
        <form onSubmit={submit}>
          {inputValues.map((element, index) => {
            return (
              <div key={index}>
                <input
                  type='number'
                  name='frequency'
                  placeholder='Hz'
                  value={element.frequency}
                  onChange={(event) => handleInputChange(index, event)}
                />
                <input
                  type='number'
                  name='amplitude'
                  placeholder='Amplitude'
                  value={element.amplitude}
                  onChange={(event) => handleInputChange(index, event)}
                />
                <input
                  type='text'
                  name='shape'
                  placeholder='Shape'
                  value={element.shape}
                  onChange={(event) => handleInputChange(index, event)}
                />
                <input
                  type='number'
                  name='attack'
                  placeholder='Attack'
                  value={element.attack}
                  onChange={(event) => handleInputChange(index, event)}
                  />
                  <input
                  type='number'
                  name='decay'
                  placeholder='Decay'
                  value={element.decay}
                  onChange={(event) => handleInputChange(index, event)}
                  />
                  <input
                  type='text'
                  name='sustain'
                  placeholder='Sustain'
                  value={element.sustain}
                  onChange={(event) => handleInputChange(index, event)}
                  />
                  <input
                  type='text'
                  name='release'
                  placeholder='Release'
                  value={element.release}
                  onChange={(event) => handleInputChange(index, event)}
                  />
                {index ? (
                  <button
                    onClick={(event) => {
                      removeInput(index, event);
                    }}>
                    Remove
                  </button>
                ) : null}
              </div>
            );
          })}
          <button onClick={(e) => addInput(e)}>Add</button>
          <button type='submit'>Generate</button>
        </form>

        <button onClick={playAudio}>Play</button>
      </div>
    </div>
  );
}

export default App;

//TODO
