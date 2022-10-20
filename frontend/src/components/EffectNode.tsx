import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function EffectNode({ data }: any) {
  const onChange = useCallback((event: any) => {
    console.log(event.target.value);
  }, []);

  return (
    <div className='eff-node'>
      <Handle type='target' position={Position.Left} />
      <b>Effect</b>
      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default EffectNode;
