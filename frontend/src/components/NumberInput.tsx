export default function NumberInput({
  name,
  defaultValue,
  step = 'any',
  onChange,
}: any): JSX.Element {
  return (
    <div style={{ display: 'block', margin: '1rem' }}>
      <div style={{ display: 'inline-block', width: '6rem' }}>
        <label style={{ margin: '0.5rem' }}>
          {name.charAt(0).toUpperCase() + name.slice(1)}
        </label>
      </div>
      <input
        style={{ width: '3rem' }}
        type='number'
        step={step}
        min={0}
        name={name}
        defaultValue={defaultValue}
        onChange={onChange}
        required
      />
    </div>
  );
}
