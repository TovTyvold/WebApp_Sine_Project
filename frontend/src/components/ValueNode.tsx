import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function ValueNode({ data, id }: any) {
  const onChange = useCallback(
    (event: any) => {
      data.value = event.target.value;
    },
    [data]
  );

  return (
    <div className='val-node'>
      <b>Value</b>
      <hr />
      {/* <Handle type='source' position={Position.Right} /> */}
      <Handle id={'out-' + id} type='source' position={Position.Right} />
      <NumberInput defaultValue={data.value} name='value' onChange={onChange} />
    </div>
  );
}

export default ValueNode;
