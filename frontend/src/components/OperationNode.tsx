import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function OperationNode({ data, id, remove }: any) {
  return (
    <div className='op-node'>
      <Handle type='target' position={Position.Left} />
      <b>{id}</b>
      <label onClick={remove} style={{ float: 'right', paddingRight: '3px' }}>
        <b>X</b>
      </label>
      <b>Sum</b>
      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default OperationNode;
