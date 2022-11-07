import { useCallback, useState } from 'react';

function SliderInput({
  name,
  label,
  defaultValue,
  unit = '',
  step = 1,
  min,
  max,
  onChange,
}: any) {
  const [sliderValue, setSliderValue] = useState(defaultValue);
  const onValueChange = useCallback(
    (event: any) => {
      event.preventDefault();
      setSliderValue(event.target.value);
      onChange(event, unit);
    },
    [onChange, unit]
  );

  return (
    <div style={{ marginTop: '10px' }}>
      <div style={{ display: 'inline-block', width: '75px' }}>
        <label htmlFor={name} style={{ margin: '5px' }}>
          {label ? label : name.charAt(0).toUpperCase() + name.slice(1)}
        </label>
      </div>
      <input
        type='range'
        step={step}
        min={min}
        max={max}
        name={name}
        value={sliderValue}
        onChange={onValueChange}
        className='slider nodrag'
      />
      <span
        style={{ marginLeft: '10px', display: 'inline-block', width: '65px' }}>
        {sliderValue} {unit}
      </span>
    </div>
  );
}

export default SliderInput;
