import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import SliderInput from './SliderInput';

function OutputNode({ data, id }: any) {
  const onChange = useCallback((event: any) => {
    if (event.target.name === 'pan') data.pan.percent = event.target.value;
    if (event.target.name === 'sustain')
      data.sustainTime.sec = event.target.value;
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
        defaultValue={data.pan.percent}
        min={0}
        max={100}
        unit='%'
        onChange={onChange}
      />
      <SliderInput
        name='sustain'
        defaultValue={data.sustainTime.sec}
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
