import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function OperationNode({ data, id }: any) {
  return (
    <div className='op-node'>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Operation</b>
      <br />

      <b>Sum</b>
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default OperationNode;
