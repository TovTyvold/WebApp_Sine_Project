import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function SumNode({ id, selected }: any) {
  return (
    <div className={'sum-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Sum</b>
      <hr />
      <div style={{ fontSize: '32pt' }}>
        <b>+</b>
      </div>

      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default SumNode;
