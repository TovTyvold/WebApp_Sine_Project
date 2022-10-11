import FreqInput from "./FreqInput";
import AmpInput from "./AmpInput";
import WaveTypeInput from "./WaveTypeInput";

export default function InputBox(): JSX.Element {
  return (
    <>
      <FreqInput />
      <AmpInput />
      <WaveTypeInput />
    </>
  );
}
