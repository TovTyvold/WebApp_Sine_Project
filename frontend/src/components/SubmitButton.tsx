import React from "react";
 
const SubmitButton = () => {

    const testData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            list: [50, 500, 5000]
        })
    }

    const handleSubmit = () => {
        fetch('https://10.99.3.251:5000/test', testData)
        console.log('button pressed');
    };


    return (
        <button onClick={handleSubmit}>Generate</button>
    )
};

export default SubmitButton;