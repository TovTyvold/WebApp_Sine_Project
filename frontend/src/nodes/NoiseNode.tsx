import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import SliderInput from '../components/SliderInput';

function NoiseNode({ data, id, selected }: any) {
  const onSelectionChange = useCallback((event: any) => {
    data.color = event.target.value;
  }, []);
  const onChange = useCallback((event: any) => {
    data.intensity = event.target.value;
  }, []);

  return (
    <div className={'noise-node' + (selected ? ' node-selected' : '')}>
      <b>Noise</b>

      <div className='select'>
        <select name='noise-type' onChange={onSelectionChange}>
          <option value='white'>White</option>
          <option value='pink'>Pink</option>
          <option value='blue'>Blue</option>
          <option value='violet'>Violet</option>
          <option value='brownian'>Brown</option>
        </select>
      </div>
      <hr />
      <SliderInput
        name='intensity'
        min={0}
        max={2}
        step={0.1}
        onChange={onChange}
      />
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default NoiseNode;
