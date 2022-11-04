import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function OperationNode({ data, id, selected }: any) {
  const onChange = useCallback(
    (event: any) => {
      data.opType = event.target.value;
    },
    [data]
  );
  return (
    <div className={'op-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Operation</b>
      <hr />
      <div className='select'>
        <select name='op' onChange={onChange}>
          <option value='sum'>Sum +</option>
          <option value='multi'>Times ×</option>
        </select>
      </div>

      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default OperationNode;
