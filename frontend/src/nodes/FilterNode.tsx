import { useCallback, useState } from 'react';
import { Handle, Position } from 'reactflow';

import SliderInput from '../components/SliderInput';

function FilterNode({ data, id, selected }: any) {
  const [selection, setSelection] = useState(data.filterType);

  const onChange = useCallback((event: any) => {
    data[event.target.name] = event.target.value;
  }, []);
  return (
    <div className={'filter-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />
      <b>Filter</b>
      <br />
      <div className='select'>
        <select
          name='filterType'
          defaultValue={data.filterType}
          onChange={onChange}>
          <option value='hpf'>High Pass Filter</option>
          <option value='lpf'>Low Pass Filter</option>
        </select>
      </div>
      <hr />
      <SliderInput
        name={'cutoff'}
        unit='Hz'
        min={20}
        max={5000}
        defaultValue={data.cutoff}
        onChange={onChange}
      />
      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default FilterNode;
