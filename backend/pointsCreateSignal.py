
from ast import Mod
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from torch import sign

from filterAudio import low_pass_Filter, high_pass_Filter, dirac_comb_discrete, weierstrassFunc,\
     Rev_Conv_Filter, semitoneFunc, singleShift, vibratoFunc, whiteChorus, reverberatorFunc
from reverberator import main
from soundGen import play
from pointsFrequency import signal_to_hertz
from ADSR_mod import ADSR
from pointsNoise import coloredNoise
from plotting import plot_array
from pointsCalculation import noteToFreq

plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies, Fs):
    t0 = time.time()
    n_signals = len(frequencies)

    # Set variables
    T = 1/(Fs) 
    N = Fs
    
    t = 2
    Amp_array = 1
    N = Fs 
    t_vec = np.arange(t*N)*(T*t) 
    y = np.zeros((n_signals,len(t_vec)))
    k = 0
    y_sum = 0
    omega = 2 * np.pi
    sine_add = np.sin(np.linspace(-12 * np.pi,12 * np.pi,len(t_vec)))
    omega = 2 * np.pi* sine_add
    for i in range(n_signals):
        y[k] = (Amp_array * amplitudes[k]) * np.sin(omega* frequencies[i] * t_vec)
        y_sum += y[k] 
        k += 1  


    normalized_y = y_sum/np.max(abs(y_sum)) 
    #play(normalized_y.copy())
    #width = 0.001
    #Modfreq = 2.5 # Hertz to passs to sine wave, Should be between 0.1-5 Hz
    #W = 2
    #y_shifted = singleShift(normalized_y.copy(), n=2, shift_ = 200)
    
    #y_vibrato = vibratoFunc(normalized_y.copy(), Modfreq, width, W)
    #y_chorus = whiteChorus(normalized_y.copy(), width) 
    """ ya = 0
    k = 0
    for i in frequencies:
        ya += amplitudes[k] * np.sin(omega * (i+200) * t_vec)
        k+=1
    ya = ya / np.max(np.abs(ya)) """
    #rev_y, t_vec_r = Rev_Conv_Filter(normalized_y.copy(), Duration_inp=t+ 2, DryWet_ = 100)
    #reverberator = reverberatorFunc(normalized_y.copy(), DryWet = 0.7)
    rev_out = main(normalized_y.copy()) 
    Fs_n = len(rev_out)
    T = 1/Fs
    N = Fs_n 
    t_vec_r = np.arange(int(N))*(T*t)

    plt.figure()
    plt.plot(t_vec_r, rev_out, 'g')
    plt.figure()
    plt.plot(t_vec, normalized_y.copy(), 'y')

    #play(y_vibrato)
    plt.ion()
    play(list(normalized_y.copy()) + list(rev_out))
    #play(rev_out)
    plt.show()
    plt.pause(2)
    plt.ioff() 

    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")
    return t_vec, Fs, frequencies



t0_func = time.time()
print("Timing outside func started....")

Create_Sine([1], [50], 44100)


t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



