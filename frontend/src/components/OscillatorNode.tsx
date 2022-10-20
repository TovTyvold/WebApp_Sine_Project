import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';
import WaveTypeInput from './WaveTypeInput';

function OscillatorNode({ data }: any) {
  const onChange = useCallback(
    (event: any) => {
      const value = event.target.value;
      switch (event.target.name) {
        case 'frequency':
          data.frequency = value;
          break;
        case 'amplitude':
          data.amplitude = value;
          break;
        case 'shape':
          data.shape = value;
          break;
        default:
          console.log('Error: incorrect target');
      }
    },
    [data]
  );

  return (
    <div className='osc-node'>
      <br />
      <NumberInput
        label='Frequency (Hz)'
        name='frequency'
        onChange={onChange}
      />
      <NumberInput label='Amplitude' name='amplitude' onChange={onChange} />
      <WaveTypeInput onChange={onChange} />
      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default OscillatorNode;
