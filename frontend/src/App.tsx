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
  const ws = new WebSocket(API_WS);
  ws.binaryType = "arraybuffer";

  let channels = 1;
  const frameCount = 44100;
  let bytesRead = 0;
  const buffer = new AudioBuffer({
    numberOfChannels: channels,
    length: frameCount,
    sampleRate: 44100,
  });

  ws.onmessage = (message) => {
    const chunk = new Float32Array(message.data);
    if (message.data instanceof ArrayBuffer) {
      for (let i = 0; i < bytesRead; i++) {
        buffer.getChannelData(0)[i + bytesRead] = chunk[i];
      }
      bytesRead += chunk.length;
    }
  };

  function playAudio() {
    const source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(context.destination);
    source.start();
    source.onended = () => {
      console.log("Sound is done playing!");
    };
  }

  // useEffect(() => {
  //   testAudioStream();
  // }, []);

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

    ws.send(JSON.stringify(inputValues));

    console.log("Datapoints: ", dataPoints);
  };

  return (
    <div className='App'>
      <div className='container'>
        <header>Wave Generator</header>
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
                  value={element.frequency || ""}
                  onChange={(event) => handleInputChange(index, event)}
                />
                <input
                  type='number'
                  name='amplitude'
                  placeholder='Amplitude'
                  value={element.amplitude || ""}
                  onChange={(event) => handleInputChange(index, event)}
                />
                <input
                  type='text'
                  name='shape'
                  placeholder='Shape'
                  value={element.shape || ""}
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
