import { useCallback, useState } from 'react';

const ControllButtons = ({ getFlow, addNode }: any) => {
  const [nodeSelect, setNodeSelect] = useState('oscillator');
  const onChange = useCallback((event: any) => {
    setNodeSelect(event.target.value);
  }, []);
  return (
    <div style={{ zIndex: 4, position: 'absolute', display: 'flex' }}>
      <div style={{ marginRight: '1rem' }}>
        <button onClick={getFlow}>Submit</button>
      </div>
      <select name='node-type' onChange={onChange}>
        <option value='oscillator'>Oscillator</option>
        <option value='envelope'>Envelope</option>
        <option value='effect'>Effect</option>
        <option value='operation'>Operation</option>
      </select>
      <div>
        <button onClick={() => addNode(nodeSelect)}>Add Node</button>
      </div>
    </div>
  );
};
export default ControllButtons;
