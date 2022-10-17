export default function EnvelopeADSR({
  element,
  index,
  handleInputChange,
}: any): JSX.Element {
  return (
    <div className='envelope'>
      <input
        type='number'
        name='attack'
        placeholder='Attack'
        value={element.adsr[0]}
        onChange={(event) => handleInputChange(index, event)}
      />
      <input
        type='number'
        name='decay'
        placeholder='Decay'
        value={element.adsr[1]}
        onChange={(event) => handleInputChange(index, event)}
      />
      <input
        type='number'
        name='sustain'
        placeholder='Sustain'
        value={element.adsr[2]}
        onChange={(event) => handleInputChange(index, event)}
      />
      <input
        type='number'
        name='release'
        placeholder='Release'
        value={element.adsr[3]}
        onChange={(event) => handleInputChange(index, event)}
      />
    </div>
  );
}
