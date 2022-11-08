
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from matplotlib.widgets import Slider, Button
from wave_to_file import wave_file
from filterAudio import low_pass_Filter, high_pass_Filter, dirac_comb_discrete,\
    singleShift, vibratoFunc, Reverb_
from coloredNoise import plot_spectrum, white_noise, brownian_noise, violet_noise, pink_noise, blue_noise
from soundGen import play
from pointsNoise import cNoise
from pointsCalculation import noteToFreq
import envelope
import bezierCurve

plt.style.use('ggplot')

def Create_Sine(amplitudes, frequencies):
    Fs = 44100
    T = 1/(Fs) 
    N = Fs
    t = 0.1
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
    N_ = 2 
    K_ = 5
    dirac = dirac_comb_discrete(norm_y.copy(), N_, K_)
    plt.figure()
    plt.title(f"Plot with t = {t}")
    plt.xlabel("t[s]")
    plt.ylabel("A[Hz]")
    plt.plot(t_vec, norm_y.copy(), 'g', label="Normalized y")
    t_vec = np.arange((len(dirac))) * T * t
    plt.plot(t_vec, dirac, 'y', label="Dirac Comb")
    plt.legend()
    plt.savefig(f"figures/diracComb_{t}_{N_}_{K_}.pdf")
    #plt.show()



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
Create_Sine([1, 1, 1, 1], [100, 220, 50, 150])


