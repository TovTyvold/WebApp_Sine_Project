import { useRef } from 'react';

const WIDTH = document.body.offsetWidth * 0.8;
const HEIGHT = 150;

interface IProps {
  audioCtx: AudioContext;
  audioSrc: AudioBufferSourceNode;
}

function BarGraphVisualizer({ audioCtx, audioSrc }: IProps) {
  const node = useRef<HTMLCanvasElement>(document.createElement('canvas'));

  const analyser = audioCtx.createAnalyser();
  audioSrc.connect(analyser);
  analyser.fftSize = 256; // 2048;

  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  const canvas = node.current;
  if (!canvas) return null;

  const context = canvas.getContext('2d');

  if (!context) return null;
  context.clearRect(0, 0, WIDTH, HEIGHT);

  const draw = () => {
    requestAnimationFrame(draw);

    analyser.getByteFrequencyData(dataArray);

    if (context) {
      context.fillStyle = 'whitesmoke';
      context.fillRect(0, 0, WIDTH, HEIGHT);
      const barWidth = (WIDTH / bufferLength) * 2.5; // 1
      let barHeight;
      let x = 0;
      for (let i = 0; i < bufferLength; i++) {
        barHeight = dataArray[i] / 2;

        context.fillStyle = `rgb(31, 147, 158)`;
        context.fillRect(x, HEIGHT - barHeight / 2, barWidth, barHeight);

        x += barWidth + 1;
      }
    }
  };

  draw();

  return (
    <canvas
      ref={node}
      width={WIDTH.toString()}
      height={HEIGHT.toString()}
      style={{
        border: '2px #1f939e solid',
        borderRadius: '10px',
      }}
    />
  );
}

export default BarGraphVisualizer;
