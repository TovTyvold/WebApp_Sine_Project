
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from filterAudio import reverb_filter, Impulse_Rev, low_pass_Filter, high_pass_Filter
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

    if not amplitudes:
        """ print("-------------------------------")
        print("No amplitudes, list is empty.")
        print(f"Generating {n} random amplitudes...")
        amplitudes = 50 * np.random.rand(1,n) """
        amplitudes = [10]

    if not Fs:
        Fs = 5000
        print(f"Sampling is {Fs}")

    if not frequencies:
        """ print("-------------------------------")
        print("No frequencies, list is empty.")
        print(f"Generating {n} random frequencies...")
        #n Frequencies between [0,100)
        list_numbers = np.linspace(30,max_freq_input,n)
        frequencies = list_numbers * np.random.rand(1,n) """
        frequencies = [440]


    n_signals = len(frequencies)

    # Set variables
    T = 1/(Fs) 
    N = Fs
    

    #   ADSR(y, list_ADSR, N, sustainAmplitude = 0.7, maxAmplitude = 1):
    if isinstance(list_ADSR, list):
        print("APPLY ADSR", list_ADSR)


        t = np.sum(list_ADSR)
        omega = 2*np.pi*all(frequencies) 
        t_vec = np.arange(N)*T 
        y = np.zeros((n_signals,len(t_vec)))
        k = 0
        y_sum = 0

        Amp_array = ADSR(list_ADSR, N, t)


        for i in omega:
            y[k] = (Amp_array * amplitudes[k]) * np.sin(i*t_vec)
            y_sum += y[k] 
            k += 1 
    
    else:
        t = 0.1
        Amp_array = 1
        N = Fs 
        t_vec = np.arange(N)*(T*t) 
        y = np.zeros((n_signals,len(t_vec)))
        k = 0
        y_sum = 0
        for i in range(n_signals):
            omega = 2*np.pi #*frequencies[i]
            y[k] = (Amp_array * amplitudes[k]) * np.sin(omega*t_vec)
            y_sum += y[k] 
            k += 1 


    normalized_y = y_sum/np.max(y_sum) 
    plt.figure()
    plot_array(t_vec, y_sum, "y", "t[s]", "A[m]", "y", "r", "-", True, "y.pdf")
    plt.ion()
    #play(normalized_y)
    # PLot varibles
    #plt.plot(y, t_vec, title, xlabel, ylabel, label_graph, color_graph, ls_graph, save, filename):
    # plot_array(t_vec, y_sum,  "Y + Saw", "t[s]", "A[m]", "Saw", "r", "-", False, "Saw.pdf")
    cutoff_low = np.max(frequencies)-1
    cutoff_high = np.min(frequencies)+1
    order = np.max(frequencies)/2
    lowpass = low_pass_Filter(normalized_y.copy(), Fs, cutoff = cutoff_low, order = order)
    highpass = high_pass_Filter(normalized_y.copy(), Fs, cutoff = cutoff_high, order = order)
    plt.figure()
    plt.plot(lowpass, t_vec)
    plt.show()
    plt.pause(2)
    plt.ioff()
    print("play sound...")

    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")

    return t_vec, Fs, frequencies, list_of_waves#, Array_of_various_signals#, norm_max



t0_func = time.time()
print("Timing outside func started....")

#t_vec, Fs, freqs, Array_of_various_signals = Create_Sine(np.array([10,10,10,10,10,10,10]), np.array([200, 400, 450, 500, 550, 600, 800]), 44100, list_ADSR = 0)
Create_Sine([1], [200], 44100, list_ADSR = 0)

t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



