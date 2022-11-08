import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from '../components/NumberInput';

function OscillatorNode({ data, id, selected }: any) {
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
    <div className={'osc-node' + (selected ? ' node-selected' : '')}>
      <Handle
        id={'frequency-' + id}
        type='target'
        position={Position.Left}
        style={{ top: 75 }}
        onConnect={(p) => {
          console.log('freq handle connect', p);
        }}
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
        name='frequency'
        defaultValue={data.frequency}
        onChange={onChange}
      />
      <NumberInput
        name='amplitude'
        defaultValue={data.amplitude}
        onChange={onChange}
      />
      <label htmlFor='shape' className='osc-input-dd'>
        Wave Type
      </label>
      <div className='select'>
        <select name='shape' defaultValue={data.shape} onChange={onChange}>
          <option value='sin'>Sine</option>
          <option value='saw'>Saw</option>
          <option value='square'>Square</option>
          <option value='triangle'>Triangle</option>
        </select>
      </div>
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default OscillatorNode;
