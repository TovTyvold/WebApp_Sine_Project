import numpy as np
import matplotlib.pyplot as plt 

"""
Module for computing different types of coloured noise. 

Main function is noise_psd, which computes the Power Spectral Density of the proposed noise. 

To produce a colored-noise signal, call one of the noise functions and provide two scalars as argumentens.

The first scalar must be an integer and corresponds to the length of the colored-noise signal.  
The second scalar can be float/int and corresponds to the intensity of the signal. 
"""

def plot_spectrum(s):
    f = np.fft.rfftfreq(len(s))
    return plt.loglog(f, np.abs(np.fft.rfft(s)))[0]

def noise_psd(N, psd = lambda f: 1):
    X_white = np.fft.rfft(np.random.randn(N))
    S = psd(np.fft.rfftfreq(N))

    S = S / np.sqrt(np.mean(S * S))
    X_shaped = X_white * S 
    return np.fft.irfft(X_shaped)

def PSDGenerator(f):
    return lambda N, I: (noise_psd(N, f) / np.max(noise_psd(N, f))) * I
    #return lambda N: noise_psd(N, f)

@PSDGenerator
def white_noise(f):
    return 1 

@PSDGenerator
def blue_noise(f):
    return np.sqrt(f)

@PSDGenerator
def violet_noise(f):
    return f 

@PSDGenerator
def brownian_noise(f):
    return 1 / np.where(f == 0, float('inf'), f)

@PSDGenerator
def pink_noise(f):
    return 1 / np.where(f == 0, float('inf'), np.sqrt(f))
