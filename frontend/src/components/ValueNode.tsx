import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function ValueNode({ data }: any) {
  const onChange = useCallback((event: any) => {
    data.value = event.target.value
  }, [])

  return (
    <div className='val-node'>
      <b>Value</b>
      <Handle type='source' position={Position.Right} />
      <NumberInput  label="Value" name="Value" onchange={onChange}/>
    </div>
  );
}

export default ValueNode;
