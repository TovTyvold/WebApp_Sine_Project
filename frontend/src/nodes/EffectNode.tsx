import { useCallback, useState } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from '../components/NumberInput';

function FilterEffect1({ name, onChange }: any) {
  return (
    <>
      <NumberInput name={name} onChange={onChange} />
    </>
  );
}
function FilterEffect2(props: any) {
  return (
    <>
      <NumberInput name={props.name1} onChange={props.onChange} />
      <NumberInput name={props.name2} onChange={props.onChange} />
    </>
  );
}

const params: any = {};

function EffectNode({ data, id, selected }: any) {
  const [selection, setSelection] = useState('reverb');

  const onSelectionChange = useCallback((event: any) => {
    event.preventDefault();
    setSelection(event.target.value);
  }, []);

  const onChange = useCallback(
    (event: any) => {
      event.preventDefault();
      data.effectName = selection;
      params[event.target.name] = event.target.value;
      data.params = params;
    },
    [selection, data]
  );

  return (
    <div className={'eff-node' + (selected ? ' node-selected' : '')}>
      <Handle id={'in-' + id} type='target' position={Position.Left} />

      <b>Effect</b>
      <br />
      <div className='select'>
        <select name='effect-type' onChange={onSelectionChange}>
          <option value='reverb'>Reverb</option>
          <option value='lpf'>Low Pass Filter</option>
          <option value='hpf'>High Pass Filter</option>
          <option value='dirac'>Dirac Comb Filter</option>
          <option value='lfo-sin'>LFO Sine</option>
          <option value='lfo-saw'>LFO Saw</option>
          <option value='phase'>Phase Shifter</option>
        </select>
      </div>
      <hr />
      {
        {
          reverb: (
            <FilterEffect2
              name1={'duration'}
              name2={'mixPercent'}
              onChange={onChange}
            />
          ),
          lpf: <FilterEffect1 name={'cutoff'} onChange={onChange} />,
          hpf: <FilterEffect1 name={'cutoff'} onChange={onChange} />,
          dirac: (
            <FilterEffect2
              name1={'precision'}
              name2={'rate'}
              onChange={onChange}
            />
          ),
          'lfo-sin': <FilterEffect1 name={'rate'} onChange={onChange} />,
          'lfo-saw': <FilterEffect1 name={'rate'} onChange={onChange} />,
          phase: <FilterEffect1 name={'level'} onChange={onChange} />,
        }[selection]
      }

      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default EffectNode;
