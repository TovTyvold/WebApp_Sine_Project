//App.tsx
import "./App.css";
import React, { useState, useEffect } from "react";
import Graph from "./components/Graph";
import sendData from "./sendData";

type Wave = {
  frequency: number | undefined;
  amplitude: number | undefined;
  shape: string;
};

const defaultInput: Wave = {
  frequency: undefined,
  amplitude: undefined,
  shape: "",
};

const API_POINTS = "http://localhost:5000/points";
const API_WS = "ws://localhost:5000/sound";

function App() {
  // Hooks
  const [dataPoints, setDataPoints] = useState([]);
  const [inputValues, setInputValues] = useState<Wave[]>([defaultInput]);

  const context = new AudioContext();
  let chunks: any = [];
  const ws = new WebSocket(API_WS);
  ws.binaryType = "arraybuffer";

  ws.onmessage = (message) => {
    message.data instanceof ArrayBuffer
      ? chunks.push(message.data)
      : createSoundSource(chunks);
  };

  async function createSoundSource(data: any) {
    await Promise.all(
      data.map(async (chunk: any) => {
        const soundBuffer = await context.decodeAudioData(chunk);
        const soundSource = context.createBufferSource();
        soundSource.buffer = soundBuffer;
        soundSource.connect(context.destination);
        soundSource.start(0);
      })
    );
  }

  useEffect(() => {}, []);

  const handleInputChange = (
    index: number,
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.currentTarget;
    const list: any[] = [...inputValues];
    list[index][name] = value;
    setInputValues(list);
  };

  const addInput = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const newInput: Wave = {
      frequency: undefined,
      amplitude: undefined,
      shape: "",
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

  // Get values from inputs
  const submit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
    setDataPoints(await sendData(API_POINTS, inputValues));

    console.log("Datapoints: ", dataPoints);
  };

  return (
    <div className='App'>
      <div className='container'>
        <header>Wave Calculator</header>
        <section className='graph'>
          <Graph data={dataPoints} />
        </section>
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
      </div>
    </div>
  );
}

export default App;

//TODO
