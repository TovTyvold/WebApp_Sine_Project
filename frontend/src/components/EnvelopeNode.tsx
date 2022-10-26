import { useCallback, useState } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';
import SliderInput from './SliderInput';

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
        <SliderInput
          name='attack'
          defaultValue={1}
          unit='ms'
          min={1}
          max={1000}
          onChange={onChange}
        />
        <SliderInput
          name='decay'
          defaultValue={1}
          unit='ms'
          min={1}
          max={1000}
          onChange={onChange}
        />
        <SliderInput
          name='sustain'
          defaultValue={1}
          unit='%'
          min={1}
          max={100}
          onChange={onChange}
        />
        <SliderInput
          name='release'
          defaultValue={1}
          unit='ms'
          min={1}
          max={1000}
          onChange={onChange}
        />
      </div>

      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default EnvelopeNode;
