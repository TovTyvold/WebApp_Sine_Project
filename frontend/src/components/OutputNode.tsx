import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function OutputNode({ data, id }: any) {
  // const onChange = useCallback((event: any) => {
  //   data.seconds = event.target.value;
  // }, []);

  return (
    <div className='out-node'>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Output</b>
      <hr />
      <label htmlFor='seconds'>Seconds</label>
      <input
        type='range'
        min='1'
        max='20'
        name='seconds'
        onChange={data.onchange}
        className='slider nodrag'
      />
    </div>
  );
}

export default OutputNode;
