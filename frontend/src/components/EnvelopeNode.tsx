import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function EnvelopeNode({ data, id }: any) {
  const onChange = useCallback((event: any) => {
    event.preventDefault();
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
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>ADSR Envelope</b>
      <hr />
      <div className='slidecontainer'>
        <label htmlFor='attack'>Attack</label>
        <input
          type='range'
          min='1'
          max='100'
          name='attack'
          onChange={onChange}
          className='slider nodrag'
        />
        <label htmlFor='decay'>Decay</label>
        <input
          type='range'
          min='1'
          max='100'
          name='decay'
          onChange={onChange}
          className='slider nodrag'
        />
        <label htmlFor='sustain'>Sustain</label>
        <input
          type='range'
          min='1'
          max='100'
          name='sustain'
          onChange={onChange}
          className='slider nodrag'
        />
        <label htmlFor='release'>Release</label>
        <input
          type='range'
          min='1'
          max='100'
          name='release'
          onChange={onChange}
          className='slider nodrag'
        />
      </div>
      {/* <NumberInput label='Attack' name='attack' onChange={onChange} />
      <NumberInput label='Decay' name='decay' onChange={onChange} />
      <NumberInput label='Sustain' name='sustain' onChange={onChange} />
      <NumberInput label='Release' name='release' onChange={onChange} /> */}
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default EnvelopeNode;
