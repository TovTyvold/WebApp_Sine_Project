import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function OutputNode({ data }: any) {
  const onChange = useCallback((event: any) => {
    console.log(event.target.value);
  }, []);

  return (
    <div className='out-node'>
      <Handle type='target' position={Position.Left} />
      <b>Output</b>
    </div>
  );
}

export default OutputNode;
