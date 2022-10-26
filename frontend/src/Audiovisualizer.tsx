import { useEffect, useRef } from 'react';

function AudioVisualiser({ audioData, audioContext }: any) {
  const node = useRef<HTMLCanvasElement>(null);
  const analyser = audioContext.createAnalyser();
  analyser.fftSize = 256;
  const bufferLength = audioData.length; //analyser.frequencyBinCount;
  //const dataArray = new Uint8Array(audioData.getChannelData(0).length);// new Uint8Array(bufferLength);
  const dataArray = audioData.getChannelData(0);
  console.log('DataArray:', dataArray);
  const WIDTH = 300;
  const HEIGHT = 300;
  console.log(audioData.getChannelData(0));
  //const data = audioData.getChannelData(0);
  useEffect(() => {
    console.log('here', dataArray);
    const canvas = node.current;
    if (canvas) {
      const context = canvas.getContext('2d');
      if (context) {
        context.clearRect(0, 0, WIDTH, HEIGHT);
        //const drawVisual = requestAnimationFrame(draw);
        //analyser.getByteFrequencyData(dataArray);
        context.fillStyle = 'rgb(0, 0, 0)';
        context.fillRect(0, 0, WIDTH, HEIGHT);
        const barWidth = (WIDTH / bufferLength) * 2.5;
        let barHeight;
        let x = 0;
        for (let i = 0; i < bufferLength; i++) {
          barHeight = dataArray[i] / 2;
          context.fillStyle = `rgb(${barHeight + 100}, 50, 50)`;
          context.fillRect(x, HEIGHT - barHeight / 2, barWidth, barHeight);
          x += barWidth + 1;
        }
      }
    }
  }, [audioData]);
  return (
    <canvas
      ref={node}
      width='300'
      height='300'
      style={{ border: '1px solid #D3D3D3' }}
    />
  );
}
export default AudioVisualiser;
