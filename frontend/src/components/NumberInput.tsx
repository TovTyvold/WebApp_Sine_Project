export default function NumberInput({
  name,
  defaultValue,
  step = 'any',
  onChange,
}: any): JSX.Element {
  return (
    <label className='osc-input'>
      {name.charAt(0).toUpperCase() + name.slice(1)}
      <input
        type='number'
        step={step}
        min={0}
        name={name}
        defaultValue={defaultValue}
        onChange={onChange}
        required
      />
    </label>
  );
}
