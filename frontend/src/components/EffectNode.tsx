import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function EffectNode({ data, id, remove }: any) {
  const onChange = useCallback((event: any) => {
    console.log(event.target.value);
  }, []);

  return (
    <div className='eff-node'>
      <Handle type='target' position={Position.Left} />
      <label onClick={remove} style={{ float: 'right', paddingRight: '3px' }}>
        <b>X</b>
      </label>
      <b>Effect</b>
      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default EffectNode;
