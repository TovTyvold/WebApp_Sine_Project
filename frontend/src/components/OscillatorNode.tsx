import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';
import WaveTypeInput from './WaveTypeInput';

function OscillatorNode({ data, id }: any) {
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
      <Handle
        id={'frequency-' + id}
        type='target'
        position={Position.Left}
        style={{ top: 75 }}
      />
      <Handle
        id={'amplitude-' + id}
        type='target'
        position={Position.Left}
        style={{ top: 130 }}
      />
      <b>Oscillator</b>

      <hr />
      <NumberInput
        label='Frequency (Hz)'
        name='frequency'
        defaultValue={data.frequency}
        onChange={onChange}
      />
      <NumberInput
        label='Amplitude'
        name='amplitude'
        defaultValue={data.amplitude}
        onChange={onChange}
      />
      <WaveTypeInput onChange={onChange} />
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default OscillatorNode;
