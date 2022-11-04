import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from '../components/NumberInput';

function ValueNode({ data, id, selected }: any) {
  const onChange = useCallback(
    (event: any) => {
      data.value = event.target.value;
    },
    [data]
  );

  return (
    <div className={'val-node' + (selected ? ' node-selected' : '')}>
      <b>Value</b>
      <hr />
      {/* <Handle type='source' position={Position.Right} /> */}
      <Handle id={'out-' + id} type='source' position={Position.Right} />
      <NumberInput defaultValue={data.value} name='value' onChange={onChange} />
    </div>
  );
}

export default ValueNode;
