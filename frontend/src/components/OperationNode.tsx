import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function OperationNode({ data, id }: any) {
  const onChange = useCallback((event: any) => {
    data.opType = event.target.value;
  }, []);
  return (
    <div className='op-node'>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Operation</b>
      <hr />

      <div className='op-radio' onChange={onChange}>
        <input type='radio' name='operation' value='sum' />
        <label>
          <b>+</b>
        </label>
        <br />
        <input type='radio' name='operation' value='multi' />
        <label>
          <b>×</b>
        </label>
        <br></br>
      </div>

      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default OperationNode;
