
import { useForm } from './useForm';
import './App.css';


const API_URL = 'https://localhost:5000/test';


function App() {

  const initialState = {
    freq1: null,
    freq2: null,
    freq3: null
  }

  const { onChange, onSubmit, values } = useForm(sendData, initialState);

 
  async function sendData() {
    try {
      let response = await fetch(API_URL, {
        method: 'POST',
        body: JSON.stringify(values)
      })
      return response;
    } catch (error) {
      console.log(error);
    }
    

  }



  return (
    <div className="App">
      <form onSubmit={onSubmit}>
        <div>
          <input type="number" name='freq1' onChange={onChange} />
          <input type="number" name='freq2' onChange={onChange} />
          <input type="number" name='freq3' onChange={onChange} />
          <button type='submit'>Generate</button>
        </div>
      </form>
    </div>
  );
}

export default App;
