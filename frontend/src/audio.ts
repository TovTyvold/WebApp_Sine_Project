

let channels = 1;
const frameCount = 44100;
let bytesRead = 0;

const buffer = new AudioBuffer({
  numberOfChannels: channels,
  length: frameCount,
  sampleRate: 44100,
});

export function composeAudio(data: any) {
  
  const chunk = new Float32Array(data);
  
  if (data instanceof ArrayBuffer) {
    for (let i = 0; i < chunk.length; i++) {
      buffer.getChannelData(0)[i + bytesRead] = chunk[i];
    }
    bytesRead += chunk.length;
  } else {
    console.log(data);
  }
  
}

export function playAudio(context: AudioContext) {
  const source = context.createBufferSource();
  source.buffer = buffer;
  source.connect(context.destination);
  source.start();
  source.onended = () => {
    console.log("Sound is done playing!");
  };

  bytesRead = 0;
}