import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function EnvelopeNode({ data }: any) {
  const onChange = useCallback((event: any) => {
    const value = event.target.value;
    switch (event.target.name) {
      case 'attack':
        data.attack = value;
        break;
      case 'decay':
        data.decay = value;
        break;
      case 'sustain':
        data.sustain = value;
        break;
      case 'release':
        data.release = value;
        break;
      default:
        console.log('Error: incorrect target');
    }
  }, []);

  return (
    <div className='env-node'>
      <Handle type='target' position={Position.Left} />
      <NumberInput label='Attack' name='attack' onChange={onChange} />
      <NumberInput label='Decay' name='decay' onChange={onChange} />
      <NumberInput label='Sustain' name='sustain' onChange={onChange} />
      <NumberInput label='Release' name='release' onChange={onChange} />
      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default EnvelopeNode;