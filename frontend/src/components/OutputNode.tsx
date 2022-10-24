import { Handle, Position } from 'reactflow';

function OutputNode() {
  return (
    <div className='out-node'>
      <Handle type='target' position={Position.Left} />
      <b>Output</b>
    </div>
  );
}

export default OutputNode;
