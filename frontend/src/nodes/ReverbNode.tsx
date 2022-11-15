import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import SliderInput from '../components/SliderInput';

function ReverbNode({ data, id, selected }: any) {
  const onChange = useCallback(
    (event: any) => {
      data[event.target.name] = event.target.value;
    },
    [data]
  );
  return (
    <div className={'reverb-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Reverb</b>
      <hr />
      <SliderInput
        name='roomsize'
        label='Room Size'
        min={0.1}
        max={1.0}
        step={0.1}
        defaultValue={data.roomsize}
        onChange={onChange}
      />
      <SliderInput
        name='wet'
        min={0.01}
        max={0.99}
        step={0.01}
        defaultValue={data.wet}
        onChange={onChange}
      />
      <SliderInput
        name='dry'
        min={0.01}
        max={0.99}
        step={0.01}
        defaultValue={data.dry}
        onChange={onChange}
      />
      <SliderInput
        name='width'
        min={0.01}
        max={1.0}
        step={0.1}
        defaultValue={data.width}
        onChange={onChange}
      />
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default ReverbNode;
