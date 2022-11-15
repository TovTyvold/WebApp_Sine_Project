import { Handle, Position } from 'reactflow';

function MultiNode({ id, selected }: any) {
  return (
    <div className={'multi-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Multi</b>
      <hr />
      <div style={{ fontSize: '32pt' }}>
        <b>×</b>
      </div>

      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default MultiNode;
