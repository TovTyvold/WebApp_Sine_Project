//App.tsx
import "./App.css";
import Graph from "./components/Graph";
import React, { useState, useEffect, useRef } from "react";

type dataStructure = {
  samples: number;
  freqs: number[];
  ampls: number[];
  types: string[];
};

// Globals
const API_URL = "http://localhost:5000/points";

function App() {
  // Hooks
  const freqRef1 = useRef<HTMLInputElement>(null);
  const freqRef2 = useRef<HTMLInputElement>(null);
  const freqRef3 = useRef<HTMLInputElement>(null);
  const sampleRef = useRef<HTMLInputElement>(null);
  const [datapoints, setDatapoints] = useState([]);
  // const [inputList, setInputList] = useState([{frequency: null}])

  // Get values from inputs
  const onSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();

    const freq1 = freqRef1?.current?.value;
    const freq2 = freqRef2?.current?.value;
    const freq3 = freqRef3?.current?.value;
    const samples = sampleRef?.current?.value;

    if (!freq1 || !freq2 || !freq3 || !samples) {
      console.log("Error: One or more inputs is null or undefined");
    } else {
      // Create data object to send via API
      const data = {
        samples: parseInt(samples),
        freqs: [parseInt(freq1), parseInt(freq2), parseInt(freq3)],
      };

      setDatapoints(await sendData(data));

      console.log("Datapoints: ", datapoints);
    }
  };

  async function sendData(data: Object) {
    console.log(JSON.stringify(data));

    try {
      let response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const responseData = await response.json();
      return responseData.points;
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div className='App'>
      <div className='container'>
        <header>Wave Calculator</header>
        <div className='graph'>
          <Graph props={datapoints} />
        </div>
        <form onSubmit={onSubmit} className='inputs'>
          <div className='input-wrapper'>
            <label htmlFor='freq1'>1st Frequency</label>
            <input
              type='number'
              name='freq1'
              id='freq1'
              ref={freqRef1}
              required
            />
          </div>
          <div className='input-wrapper'>
            <label htmlFor='freq2'>2nd Frequency</label>
            <input
              type='number'
              name='freq2'
              id='freq2'
              ref={freqRef2}
              required
            />
          </div>
          <div className='input-wrapper'>
            <label htmlFor='freq3'>3rd Frequency</label>
            <input
              type='number'
              name='freq3'
              id='freq3'
              ref={freqRef3}
              required
            />
          </div>
          <div className='input-wrapper'>
            <label htmlFor='samples'>Samples</label>
            <input
              type='number'
              name='samples'
              id='samples'
              ref={sampleRef}
              required
            />
          </div>
          <button type='submit'>Generate</button>
        </form>
      </div>
    </div>
  );
}

export default App;

//TODO
