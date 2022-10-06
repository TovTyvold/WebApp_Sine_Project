// useForm.ts
import React, { useRef, useState } from "react";


const useForm = (callback: any) => {
    let freqsList: number[] = [];
    
    // States
    const [samples, setSamples] = useState(10);
    const [freqs, setFreqs] = useState([1, 2, 3]);
    

    // Set state when user inputs data
    const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {

        if (event.target.name === 'samples') {
            setSamples(parseInt(event.target.value));
        } else {
            freqsList.push(parseInt(event.target.value));
            console.log(freqsList);
            setFreqs(freqsList);
        }
    };

    // Call sendData funtion
    const onSubmit = async (event: React.ChangeEvent<HTMLFormElement>) => {
        event.preventDefault();
        await callback();
    }

    // Create data object to send via API
    const data = {
        samples: samples,
        freqs: freqs
    }


    return {
        onChange, onSubmit, data
    };


}

export default useForm;