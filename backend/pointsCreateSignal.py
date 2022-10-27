
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from torch import sign
from filterAudio import low_pass_Filter, high_pass_Filter, dirac_comb_discrete, weierstrassFunc,\
     pitch_12_up, Rev_Conv_Filter, semitoneFunc, singleShift
from soundGen import play
from pointsFrequency import signal_to_hertz
from ADSR_mod import ADSR
from pointsNoise import coloredNoise
from plotting import plot_array
from pointsCalculation import noteToFreq

plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies, Fs, list_ADSR = 0):
    list_of_waves = []
    t0 = time.time()
    n_signals = len(frequencies)

    # Set variables
    T = 1/(Fs) 
    N = Fs
    
    t = 0.1
    Amp_array = 1
    N = Fs 
    t_vec = np.arange(N)*(T*t) 
    y = np.zeros((n_signals,len(t_vec)))
    k = 0
    y_sum = 0
    omega = 2 * np.pi
    #sine_add = np.sin(np.linspace(-8 * np.pi,8 * np.pi,len(t_vec)))
    #omega = 2 * np.pi* sine_add
    for i in range(n_signals):
        y[k] = (Amp_array * amplitudes[k]) * np.sin(omega* frequencies[i] * t_vec)
        y_sum += y[k] 
        k += 1 



    normalized_y = y_sum/np.max(y_sum) 
    """ Duration = 3
    t_vec_r = np.arange(int(N * Duration)) * T * t
    rev_y = Rev_Conv_Filter(normalized_y.copy(), Duration, 25)
    f, Pxx = signal_to_hertz(rev_y) """
    ya = np.sin(omega * (frequencies[0] + 20) * t_vec) #+ np.sin(omega * (frequencies[1] + 20) * t_vec)
    changed = semitoneFunc(y_sum.copy(), n = 1, shift_ = 20)

    plt.figure()
    plt.plot(t_vec, changed[:len(t_vec)], 'r')
    #plt.plot(t_vec, ya, 'y--')
    plt.plot(t_vec, y_sum, 'k')
    #plt.ion()
    plt.show()
    #plt.pause(4)
    #plt.ioff() 
    """ play(y_sum)
    play(changed[:len(t_vec)]) """
    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")

    return t_vec, Fs, frequencies, list_of_waves#, Array_of_various_signals#, norm_max



t0_func = time.time()
print("Timing outside func started....")

Create_Sine([1], [500], 44100, list_ADSR = 0)


t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



