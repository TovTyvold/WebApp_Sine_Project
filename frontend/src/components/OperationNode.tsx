import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function OperationNode({ data }: any) {
  return (
    <div className='op-node'>
      <Handle type='target' position={Position.Left} />
      <b>Operation</b>
      <br />

      <b>Sum</b>
      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default OperationNode;
