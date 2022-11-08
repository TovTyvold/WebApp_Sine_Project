import { useCallback, useState } from 'react';
import { Handle, Position } from 'reactflow';

import SliderInput from '../components/SliderInput';

const params: any = {};

function EffectNode({ data, id, selected }: any) {
  let defaultSelect: string = 'reverb';
  if (data.effectName) defaultSelect = data.effectName;

  const [selection, setSelection] = useState(defaultSelect);

  const onSelectionChange = useCallback((event: any) => {
    event.preventDefault();
    data.effectName = selection;
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
        <select
          name='effect-type'
          defaultValue={defaultSelect}
          onChange={onSelectionChange}>
          <option value='reverb'>Reverb</option>
          <option value='vibrato'>Vibrato</option>
          <option value='lpf'>Low Pass Filter</option>
          <option value='hpf'>High Pass Filter</option>
          <option value='dirac'>Dirac Comb Filter</option>
        </select>
      </div>
      <hr />
      {
        {
          reverb: (
            <SliderInput
              name='roomsize'
              label='Room Size'
              min={0.0}
              max={1.0}
              step={0.01}
              defaultValue={0.5}
              onChange={onChange}
            />
          ),
          dirac: (
            <>
              <SliderInput
                name='precision'
                min={0.1}
                max={5.0}
                step={0.1}
                defaultValue={0.5}
                onChange={onChange}
              />
              <SliderInput
                name='rate'
                min={0.0}
                max={1.0}
                step={0.01}
                defaultValue={0.5}
                onChange={onChange}
              />
            </>
          ),
          vibrato: (
            <>
              <SliderInput
                name='speed'
                min={0.1}
                max={5.0}
                step={0.1}
                defaultValue={0.5}
                onChange={onChange}
              />
              <SliderInput
                name='intensity'
                min={0.0}
                max={1.0}
                step={0.01}
                defaultValue={0.5}
                onChange={onChange}
              />
              <SliderInput
                name='variation'
                min={0.0}
                max={30.0}
                step={0.1}
                defaultValue={1}
                onChange={onChange}
              />
            </>
          ),
          tune: (
            <SliderInput
              name='shift'
              min={-3000}
              max={3000}
              unit='Hz'
              defaultValue={1}
              onChange={onChange}
            />
          ),
          lpf: (
            <SliderInput
              name={'cutoff'}
              unit='Hz'
              min={20}
              max={5000}
              defaultValue={200}
              onChange={onChange}
            />
          ),
          hpf: (
            <SliderInput
              name={'cutoff'}
              unit='Hz'
              min={20}
              max={5000}
              defaultValue={800}
              onChange={onChange}
            />
          ),
          // 'lfo-sin': <SliderInput name={'rate'} unit='Hz' onChange={onChange} />,
          // 'lfo-saw': <SliderInput name={'rate'} unit='Hz' onChange={onChange} />,
        }[selection]
      }

      <Handle id={'out-' + id} type='source' position={Position.Right} />
    </div>
  );
}

export default EffectNode;
