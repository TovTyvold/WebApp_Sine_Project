import NumberInput from './NumberInput';
import WaveTypeInput from './WaveTypeInput';
export default function Oscillator({
  element,
  index,
  handleInputChange,
  removeInput,
}: any): JSX.Element {
  return (
    <>
      <NumberInput
        label='Frequency (Hz)'
        name='frequency'
        value={element.frequency}
        index={index}
        handleInputChange={handleInputChange}
      />
      <NumberInput
        label='Amplitude'
        name='amplitude'
        value={element.amplitude}
        index={index}
        handleInputChange={handleInputChange}
      />
      <WaveTypeInput
        value={element.shape}
        index={index}
        handleInputChange={handleInputChange}
      />

      <button
        className='remove-button'
        style={{ visibility: index ? 'visible' : 'hidden' }}
        onClick={(event) => {
          removeInput(index, event);
        }}>
        Remove
      </button>
    </>
  );
}
