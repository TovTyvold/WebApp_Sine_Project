import { useCallback, useState } from 'react';
import { Handle, Position } from 'reactflow';
import NumberInput from './NumberInput';

function FilterEffect1({ label, name, onChange }: any) {
  return (
    <>
      <NumberInput label={label} name={name} onChange={onChange} />
    </>
  );
}
function FilterEffect2(props: any) {
  return (
    <>
      <NumberInput
        label={props.label1}
        name={props.name1}
        onChange={props.onChange}
      />
      <NumberInput
        label={props.label2}
        name={props.name2}
        onChange={props.onChange}
      />
    </>
  );
}

const params: any = {};

function EffectNode({ data }: any) {
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
    [selection]
  );

  return (
    <div className='eff-node'>
      <Handle type='target' position={Position.Left} />

      <b>Effect</b>
      <br />
      <select name='effect-type' onChange={onSelectionChange}>
        <option value='reverb'>Reverb</option>
        <option value='lpf'>Low Pass Filter</option>
        <option value='hpf'>High Pass Filter</option>
        <option value='dirac'>Dirac Comb Filter</option>
        <option value='lfo-sin'>LFO Sine</option>
        <option value='lfo-saw'>LFO Saw</option>
        <option value='phase'>Phase Shifter</option>
      </select>
      <hr />
      {
        {
          reverb: (
            <FilterEffect2
              label1={'Duration'}
              name1={'duration'}
              label2={'Wet/Dry'}
              name2={'mixPercent'}
              onChange={onChange}
            />
          ),
          lpf: (
            <FilterEffect1
              label={'Cutoff'}
              name={'cutoff'}
              onChange={onChange}
            />
          ),
          hpf: (
            <FilterEffect1
              label={'Cutoff'}
              name={'cutoff'}
              onChange={onChange}
            />
          ),
          dirac: (
            <FilterEffect2
              label1={'Precision'}
              name1={'precision'}
              label2={'Rate'}
              name2={'rate'}
              onChange={onChange}
            />
          ),
          'lfo-sin': (
            <FilterEffect1 label={'Rate'} name={'rate'} onChange={onChange} />
          ),
          'lfo-saw': (
            <FilterEffect1 label={'Rate'} name={'rate'} onChange={onChange} />
          ),
          phase: (
            <FilterEffect1 label={'Level'} name={'level'} onChange={onChange} />
          ),
        }[selection]
      }

      <Handle type='source' position={Position.Right} />
    </div>
  );
}

export default EffectNode;
