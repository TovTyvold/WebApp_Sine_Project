export default function NumberInput({
  label,
  name,
  value,
  index,
  handleInputChange,
}: any): JSX.Element {
  return (
    <label className='osc-input'>
      {label}
      <input
        type='number'
        step='any'
        min={0}
        name={name}
        placeholder={label}
        value={value}
        onChange={(event) => handleInputChange(index, event)}
      />
    </label>
  );
}
