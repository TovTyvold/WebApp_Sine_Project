import NumberInput from './NumberInput';
import WaveTypeInput from './WaveTypeInput';
export default function Oscillator({
  element,
  index,
  onChange,
  removeInput,
}: any): JSX.Element {
  return (
    <>
      <NumberInput
        label='Frequency (Hz)'
        name='frequency'
        value={element.frequency}
        index={index}
        onChange={onChange}
      />
      <NumberInput
        label='Amplitude'
        name='amplitude'
        value={element.amplitude}
        index={index}
        onChange={onChange}
      />
      <WaveTypeInput value={element.shape} index={index} onChange={onChange} />

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
