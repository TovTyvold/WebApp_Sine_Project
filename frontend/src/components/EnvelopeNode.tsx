import { useCallback, useState } from 'react';
import { Handle, Position } from 'reactflow';
import SliderInput from './SliderInput';

function EnvelopeNode({ data, id, selected }: any) {
  const onChange = useCallback((event: any) => {
    event.preventDefault();
    const value = event.target.value;
    switch (event.target.name) {
      case 'attack':
        data.attack = { ms: value };
        break;
      case 'decay':
        data.decay = { ms: value };
        break;
      case 'sustain':
        data.sustain = { percent: value };
        break;
      case 'release':
        data.release = { ms: value };
        break;
      default:
        console.log('Error: incorrect target');
    }
  }, []);

  return (
    <div className={'env-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>ADSR Envelope</b>
      <hr />
      <div className='slidecontainer'>
        <SliderInput
          name='attack'
          defaultValue={data.attack.ms}
          unit='ms'
          min={1}
          max={1000}
          onChange={onChange}
        />
        <SliderInput
          name='decay'
          defaultValue={data.decay.ms}
          unit='ms'
          min={1}
          max={1000}
          onChange={onChange}
        />
        <SliderInput
          name='sustain'
          defaultValue={data.sustain.percent}
          unit='%'
          min={1}
          max={100}
          onChange={onChange}
        />
        <SliderInput
          name='release'
          defaultValue={data.release.ms}
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
