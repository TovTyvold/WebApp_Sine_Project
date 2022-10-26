import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function MixNode({ data, id }: any) {
  const onChange0 = useCallback((event: any) => {
    data.value0 = event.target.value
  }, [data])
  const onChange1 = useCallback((event: any) => {
    data.value1 = event.target.value
  }, [data])
  const onChangePercent = useCallback((value: any) => {
    data.percent = value.target.value
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
                onChange={onChangePercent}
                className='slider nodrag'
            />
            <hr/>
            <NumberInput
                label='Value'
                name='value0'
                onChange={onChange0}
            />
            <NumberInput 
                label='Value' 
                name='value1' 
                onChange={onChange1}
            />
        </div>
    );
}

export default MixNode;
