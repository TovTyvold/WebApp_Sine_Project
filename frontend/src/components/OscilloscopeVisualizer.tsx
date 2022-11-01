import { useRef } from 'react';

const WIDTH = document.body.offsetWidth * 0.8;
const HEIGHT = 100;

interface IProps {
  audioCtx: AudioContext;
  audioSrc: AudioBufferSourceNode;
}

function OscilloscopeVisualizer({ audioCtx, audioSrc }: IProps) {
  const node = useRef<HTMLCanvasElement>(document.createElement('canvas'));
  const canvas = node.current;

  const canvasCtx = canvas.getContext('2d');

  const analyzer = audioCtx.createAnalyser();
  audioSrc.connect(analyzer);
  analyzer.fftSize = 4096;
  const bufferLength = analyzer.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  if (!canvasCtx) return null;
  canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

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
    <>
      <canvas
        id='audiovisualizer'
        ref={node}
        width={WIDTH.toString()}
        height={HEIGHT.toString()}
        style={{ border: '2px #1f939e solid', borderRadius: '10px' }}
      />
    </>
  );
}
export default OscilloscopeVisualizer;
