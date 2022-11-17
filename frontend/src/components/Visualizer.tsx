import { useRef } from 'react';

const WIDTH = document.body.offsetWidth * 0.38 - 100;
const HEIGHT = 150;

interface IProps {
  audioCtx: AudioContext;
  audioSrc: AudioBufferSourceNode;
}

function Oscilloscope(props: any) {
  const ref = useRef<HTMLCanvasElement>(document.createElement('canvas'));
  const canvasCtx = ref.current.getContext('2d');

  if (!canvasCtx) return null;
  canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

  const { analyzer, bufferLength, dataArray } = props;

  const draw = () => {
    analyzer.getByteTimeDomainData(dataArray);
    canvasCtx.fillStyle = 'whitesmoke';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);
    canvasCtx.lineWidth = 2;
    canvasCtx.beginPath();

    const sliceWidth = WIDTH / bufferLength;
    let x = 0;
    for (let i = 0; i < bufferLength; i++) {
      const v = dataArray[i] / 128.0;
      const y = v * (HEIGHT / 2);
      if (i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }
      x += sliceWidth;
    }

    canvasCtx.lineTo(WIDTH, HEIGHT / 2);
    canvasCtx.stroke();
    requestAnimationFrame(draw);
  };

  draw();
  return (
    <canvas
      id='audiovisualizer'
      ref={ref}
      width={WIDTH.toString()}
      height={HEIGHT.toString()}
      style={{ border: '2px #1f939e solid', borderRadius: '10px' }}
    />
  );
}

function BarGraph(props: any) {
  const ref = useRef<HTMLCanvasElement>(document.createElement('canvas'));
  const canvasCtx = ref.current.getContext('2d');

  if (!canvasCtx) return null;
  canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

  const { analyzer, bufferLength, dataArray } = props;

  const draw = () => {
    requestAnimationFrame(draw);

    analyzer.getByteFrequencyData(dataArray);

    canvasCtx.fillStyle = 'whitesmoke';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);
    const barWidth = (WIDTH / bufferLength) * 2.5; // 1
    let barHeight;
    let x = 0;
    for (let i = 0; i < bufferLength; i++) {
      barHeight = dataArray[i] / 1.2;

      canvasCtx.fillStyle = `rgb(31, 147, 158)`;
      canvasCtx.fillRect(x, HEIGHT - barHeight / 2, barWidth, barHeight);

      x += barWidth + 1;
    }
  };

  draw();

  return (
    <canvas
      id='audiovisualizer'
      ref={ref}
      width={WIDTH.toString()}
      height={HEIGHT.toString()}
      style={{ border: '2px #1f939e solid', borderRadius: '10px' }}
    />
  );
}

export default function Visualizer({ audioCtx, audioSrc }: IProps) {
  const analyzer = audioCtx.createAnalyser();
  audioSrc.connect(analyzer);
  analyzer.fftSize = 4096;
  const bufferLength = analyzer.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  return (
    <>
      <Oscilloscope
        analyzer={analyzer}
        bufferLength={bufferLength}
        dataArray={dataArray}
      />
      <BarGraph
        analyzer={analyzer}
        bufferLength={bufferLength}
        dataArray={dataArray}
      />
    </>
  );
}
