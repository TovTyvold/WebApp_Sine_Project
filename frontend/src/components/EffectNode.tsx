import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

const effects = {};

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
      <select name='effect-type' onChange={onChange}>
        <option value='reverb'>Reverb</option>
        <option value='lpf'>Low Pass Filter</option>
        <option value='hpf'>High Pass Filter</option>
        <option value='dirac'>Dirac Comb Filter</option>
        <option value='lfo-sin'>LFO Sine</option>
        <option value='lfo-saw'>LFO Saw</option>
        <option value='phase'>Phase Shifter</option>
      </select>
      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default EffectNode;
