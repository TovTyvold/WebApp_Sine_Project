import numpy as np
class Modulated_Vibrato:
    def __init__(self, Modfreq, width, W, sample_rate=44100):
        self.Modfreq = Modfreq 
        self.width = width
        self.W = W 
        self.sample_rate = sample_rate
        self.Delay = self.width
        self.DELAY = int(self.Delay * self.sample_rate)
        self.WIDTH = int(self.Delay * self.sample_rate)

    def get_Modfreq(self):
        if self.W == 0 or self.W == 1:
            MODFREQ = self.Modfreq / self.sample_rate + np.zeros(self.sample_rate)
        
        else:
            if 0 < self.W < 1:
                MODFREQ = np.linspace(self.Modfreq, self.Modfreq * self.W, self.sample_rate) / self.sample_rate

            elif self.W > 1:
                MODFREQ = np.linspace(self.Modfreq / self.W, self.Modfreq, self.sample_rate) / self.sample_rate

        return MODFREQ

    def solve(self, ):
        x = np.zeros_like()
        L = 1 + self.DELAY + self.WIDTH * self.get_Modfreq()

        [iter(osc) for osc in self.oscillators]
        [iter(modulator) for modulator in self.modulators]

        for n in range(self.sample_rate):
            DelayLineS = []
            M = self.get_Modfreq()
            MOD = np.sin(M[n] * 2 * np.pi * n)
            TAP = 1 + self.DELAY + self.WIDTH * MOD
            i = int(np.floor(TAP))
            frac = TAP - i 
            DelayLineS.append()
            Delayline = list(DelayLineS) + list(Delayline[:L-1])

            x[n] = Delayline[i+1] * frac + Delayline[i] * (1-frac)


    def __iter__(self):
        return x




