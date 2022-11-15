import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import SliderInput from '../components/SliderInput';

function VibratoNode({ data, id, selected }: any) {
  const onChange = useCallback(
    (event: any) => {
      data[event.target.name] = event.target.value;
    },
    [data]
  );
  return (
    <div className={'vibrato-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Vibrato</b>
      <hr />
      <SliderInput
        name='speed'
        min={0.1}
        max={5.0}
        step={0.1}
        defaultValue={data.speed}
        onChange={onChange}
      />
      <SliderInput
        name='intensity'
        min={0.0}
        max={1.0}
        step={0.01}
        defaultValue={data.intensity}
        onChange={onChange}
      />
      <SliderInput
        name='variation'
        min={0.0}
        max={30.0}
        step={0.1}
        defaultValue={data.variation}
        onChange={onChange}
      />
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default VibratoNode;
