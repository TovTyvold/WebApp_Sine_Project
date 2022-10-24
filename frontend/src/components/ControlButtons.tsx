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
    </div>
  );
};
export default ControllButtons;
