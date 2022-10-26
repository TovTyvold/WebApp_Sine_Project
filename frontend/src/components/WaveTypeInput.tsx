export default function WaveTypeInput({ onChange }: any): JSX.Element {
  return (
    <>
      <label htmlFor='shape' className='osc-input-dd'>
        Wave Type
      </label>
      <div className='select'>
        <select name='shape' onChange={onChange}>
          <option value='sin'>Sine</option>
          <option value='saw'>Saw</option>
          <option value='square'>Square</option>
          <option value='triangle'>Triangle</option>
        </select>
      </div>
    </>
  );
}
