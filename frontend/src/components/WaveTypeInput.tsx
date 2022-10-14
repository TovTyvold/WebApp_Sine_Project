export default function WaveTypeInput({
  value,
  index,
  handleInputChange,
}: any): JSX.Element {
  return (
    <label className='osc-input-dd'>
      Wave Type
      <select
        name='shape'
        value={value}
        onChange={(event) => handleInputChange(index, event)}>
        <option value='sin'>Sine</option>
        <option value='saw'>Saw</option>
        <option value='square'>Square</option>
        <option value='triangle'>Triangle</option>
      </select>
    </label>
  );
}
