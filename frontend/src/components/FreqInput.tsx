export default function FreqInput(props: any) {
  return (
    <label>
      Frequency (Hz)
      <input
        type='number'
        placeholder='Hz'
        value={props.input.freq}
        onChange={props.onChange}
      />
    </label>
  );
}
