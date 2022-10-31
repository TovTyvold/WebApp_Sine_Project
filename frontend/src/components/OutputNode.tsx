import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import SliderInput from './SliderInput';

function OutputNode({ data, id }: any) {
  const onChange = useCallback((event: any, unit: string) => {
    if (event.target.name === 'pan') data.pan = `${event.target.value}${unit}`;
    if (event.target.name === 'sustain')
      data.sustainTime = `${event.target.value}${unit}`;
  }, []);
  return (
    <div className='out-node'>
      <Handle
        id={`pan-${id}`}
        type='target'
        position={Position.Left}
        style={{ top: 70 }}
      />
      <Handle
        id={`in-${id}`}
        type='target'
        position={Position.Left}
        style={{ top: 30 }}
      />
      <b>Output</b>
      <hr />
      <SliderInput
        name='pan'
        defaultValue={data.pan}
        min={0}
        max={100}
        unit='%'
        onChange={onChange}
      />
      <SliderInput
        name='sustain'
        defaultValue={data.seconds}
        min={1}
        max={20}
        unit='sec'
        step={0.1}
        onChange={onChange}
      />
    </div>
  );
}

export default OutputNode;
