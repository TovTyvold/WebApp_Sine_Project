import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import SliderInput from '../components/SliderInput';

function DiracNode({ data, id, selected }: any) {
  const onChange = useCallback(
    (event: any) => {
      data[event.target.name] = event.target.value;
    },
    [data]
  );
  return (
    <div className={'dirac-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Dirac Comb Filter</b>
      <hr />
      <SliderInput
        name='precision'
        min={1}
        max={10}
        step={1}
        defaultValue={data.precision}
        onChange={onChange}
      />
      <SliderInput
        name='rate'
        min={0.1}
        max={30.0}
        step={0.1}
        defaultValue={data.rate}
        onChange={onChange}
      />
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default DiracNode;
