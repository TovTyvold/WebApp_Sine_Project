//App.tsx
import './App.css';
import Graph from './components/Graph';
import React, { useState, useRef } from 'react';

// Globals
const API_URL = 'http://localhost:5000/';

function App() {

  // Hooks
  const freqRef1 = useRef<HTMLInputElement>(null);
  const freqRef2 = useRef<HTMLInputElement>(null);
  const freqRef3 = useRef<HTMLInputElement>(null);
  const sampleRef = useRef<HTMLInputElement>(null);

  const onSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();

    const freq1 = freqRef1?.current?.value;
    const freq2 = freqRef2?.current?.value;
    const freq3 = freqRef3?.current?.value;
    const samples = sampleRef?.current?.value;

    // Create data object to send via API
    if(freq1 && freq2 && freq3 && samples) {
      const data = {
        samples: parseInt(samples),
        freqs: [parseInt(freq1), parseInt(freq2), parseInt(freq3)]
      }
      sendData(data);
    } else {
      console.log('Error: One or more inputs is null or undefined');
    }
  }


  async function sendData(data: Object) {
  

    console.log(JSON.stringify(data));

    try {
      let response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      })
      console.log(response.json());
      
      const responseData = await response.json()

      responseData.forEach((element: any) => {
        console.log(element);
      });

      
    } catch (error) {
      console.log(error);
    }
  
  }


  return (
    <div className="App">
    <>
      <form onSubmit={onSubmit}>
        <div>
          <label htmlFor='freq1'>
            1st Frequency
            <input type="number" name='freq1' id='freq1' ref={freqRef1} required />
          </label>
          <label htmlFor="freq2">
            2nd Frequency
            <input type="number" name='freq2' id='freq2' ref={freqRef2} required />
          </label>
          <label htmlFor="freq3">
            3rd Frequency
            <input type="number" name='freq3' id='freq3' ref={freqRef3} required />
          </label>
          <label htmlFor="samples">
            Samples
            <input type="number" name='samples' id='samples' ref={sampleRef} required/>
          </label>
          <button type='submit'>Generate</button>
        </div>
        <div>
          <Graph></Graph>
        </div>
      </form>
      <div>
        <Graph></Graph>
      </div>
     
      
    </>
    </div>

    
  );
}

export default App;
