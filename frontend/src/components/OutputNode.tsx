import { Handle, Position } from 'reactflow';

function OutputNode({ id }: any) {
  return (
    <div className='out-node'>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Output</b>
    </div>
  );
}

export default OutputNode;
