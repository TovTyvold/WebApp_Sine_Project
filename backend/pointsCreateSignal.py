
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from matplotlib.widgets import Slider, Button

from filterAudio import low_pass_Filter, high_pass_Filter, dirac_comb_discrete, weierstrassFunc,\
    singleShift, vibratoFunc, whiteChorus, pitchChorus, Reverb_
from reverberator import main_reverb
from coloredNoise import plot_spectrum, white_noise, brownian_noise, violet_noise, pink_noise, blue_noise
from soundGen import play
from pointsFrequency import signal_to_hertz
from pointsNoise import cNoise
from plotting import plot_array
from pointsCalculation import noteToFreq
import envelope
import bezierCurve

plt.style.use('ggplot')

def Create_Sine(amplitudes, frequencies):
    Fs = 44100
    T = 1/(Fs) 
    N = Fs
    t = 1
    t_vec = np.arange(t*N) * (T * t)
    omega = 2* np.pi 
    #sine_add = np.sin(np.linspace(-4 * np.pi,4 * np.pi,len(t_vec)))
    #omega = 2 * np.pi* sine_add
    y_sum = 0
    k = 0
    for i in frequencies:
        y_sum += amplitudes[k] * np.sin(omega * i * t_vec)
    
    #adsr = envelope.getSymmEnv([0.2,0.2,0.6,0.2], 0.75, 0, t)
    #y_sum = list(map(lambda a,b : a*b, bezierCurve.compositeOn(adsr, t_vec), y_sum))

    norm_y = y_sum / np.max(np.abs(y_sum))

    """ plt.figure()
    plt.plot(t_vec, singleShift(norm_y.copy(), _shi), 'g', label= "Shifted numer")
    plt.plot(t_vec, norm_y2, 'y', label = "Shifted analy")
    plt.plot(t_vec, norm_y.copy(), 'k', label="MAIN")
    plt.legend()
    plt.show()  """
    """ plt.ion()
    plt.figure()
    plt.show()
    plt.pause(4)
    plt.ioff()  """
    return None
Create_Sine([1, 1, 1, 1], [100, 220, 300, 440])


