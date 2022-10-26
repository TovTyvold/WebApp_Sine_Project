import { Handle, Position } from 'reactflow';
import SliderInput from './SliderInput';

function OutputNode({ data, id }: any) {
  return (
    <div className='out-node'>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Output</b>
      <hr />
      <SliderInput
        name='Seconds'
        defaultValue={2}
        min={1}
        max={20}
        unit=''
        step={0.1}
        onChange={data.onchange}
      />
    </div>
  );
}

export default OutputNode;
