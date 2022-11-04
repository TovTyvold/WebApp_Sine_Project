import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from '../components/NumberInput';
import SliderInput from '../components/SliderInput';

function MixNode({ data, id, selected }: any) {
  const onChange0 = useCallback(
    (event: any, unit: string) => {
      data.value0 = `${event.target.value}${unit}`;
    },
    [data]
  );
  const onChange1 = useCallback(
    (event: any) => {
      data.value1 = event.target.value;
    },
    [data]
  );
  const onChangePercent = useCallback(
    (event: any) => {
      data.percent = event.target.value;
    },
    [data]
  );

  return (
    <div className={'mix-node' + (selected ? ' node-selected' : '')}>
      <b>Mix</b>
      {/* <Handle type='source' position={Position.Right} /> */}
      <Handle id={'out-' + id} type='source' position={Position.Right} />
      <Handle
        id={'percent-' + id}
        type='target'
        position={Position.Left}
        style={{ top: 50 }}
      />
      <Handle
        id={'value0-' + id}
        type='target'
        position={Position.Left}
        style={{ top: 130 }}
      />
      <Handle
        id={'value1-' + id}
        type='target'
        position={Position.Left}
        style={{ top: 180 }}
      />
      <br />
      <SliderInput
        name='percent'
        defaultValue={50}
        min={0}
        max={100}
        unit='%'
        onChange={onChangePercent}
      />
      <hr />
      <NumberInput
        label='Value'
        name='value0'
        onChange={onChange0}
        defaultValue={data.value0}
      />
      <NumberInput
        label='Value'
        name='value1'
        onChange={onChange1}
        defaultValue={data.value1}
      />
    </div>
  );
}

export default MixNode;
