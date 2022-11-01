
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from matplotlib.widgets import Slider, Button 

from filterAudio import low_pass_Filter, high_pass_Filter, dirac_comb_discrete, weierstrassFunc,\
    semitoneFunc, singleShift, vibratoFunc, whiteChorus
from reverberator import main_reverb
from coloredNoise import plot_spectrum, white_noise, brownian_noise, violet_noise, pink_noise, blue_noise
from soundGen import play
from pointsFrequency import signal_to_hertz
from pointsNoise import cNoise
from plotting import plot_array
from pointsCalculation import noteToFreq

plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies):
    Fs = 44100
    T = 1/(Fs) 
    N = Fs
    t = 5
    t_vec = np.arange(t*N) * (T * t)
    omega = 2* np.pi 
    sine_add = np.sin(np.linspace(-4 * np.pi,4 * np.pi,len(t_vec)))
    omega = 2 * np.pi* sine_add
    y_sum = 0
    k = 0
    for i in frequencies:
        y_sum += amplitudes[k] * np.sin(omega * i * t_vec)

    normy = y_sum / np.max(np.abs(y_sum))
    #play(low_pass_Filter(normy, 290))
    #play(normy.copy())
    # Set variables
    width = 0.03
    wChorus = whiteChorus(normy.copy(), width)
    #play(normy.copy())
    play(wChorus)
    


    """ plt.ion()
    plt.figure()
    plt.show()
    plt.pause(4)
    plt.ioff()  """
    return Fs, frequencies
Create_Sine([1, 1, 1], [300, 100, 140])


