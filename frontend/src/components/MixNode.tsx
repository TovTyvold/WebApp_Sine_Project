import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function MixNode({ data, id }: any) {
  const onChange = useCallback((event: any) => {
    data.value = event.target.value
  }, [data])

  return (
        <div className='mix-node'>
            <b>Mix</b>
            {/* <Handle type='source' position={Position.Right} /> */}
            <Handle id={'out-' + id} type='source' position={Position.Right} />
            <Handle id={'percent-' + id} type='target' position={Position.Left} style={{ top: 50 }}/>
            <Handle id={'value0-' + id} type='target' position={Position.Left} style={{ top: 130 }}/>
            <Handle id={'value1-' + id} type='target' position={Position.Left} style={{ top: 180 }}/>
            <br/>
            <label htmlFor='percent'>Percent</label>
            <br/>
            <input
                type='range'
                min='1'
                max='100'
                name='percent'
                onChange={onChange}
                className='slider nodrag'
            />
            <hr/>
            <NumberInput
                label='Value'
                name='value1'
                onChange={onChange}
            />
            <NumberInput 
                label='Value' 
                name='value0' 
                onChange={onChange} 
            />


        </div>
    );
}

export default MixNode;
