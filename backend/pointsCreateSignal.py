from importlib.util import set_loader
import time
import numpy as np 
import matplotlib.pyplot as plt
from filterAudio import low_pass_Filter, high_pass_Filter, Low_frequency_Oscillator_sine,\
     Low_frequency_Oscillator_saw, reverb_filter, delay, Delay_Comb
from soundGen import play
from pointsFrequency import signal_to_hertz
from ADSR_mod import ADSR
from pointsNoise import coloredNoise
from plotting import plot_array
from pointsCalculation import noteToFreq

plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies, Fs, list_ADSR = 0):
    t0 = time.time()

    if not amplitudes[0]:
        """ print("-------------------------------")
        print("No amplitudes, list is empty.")
        print(f"Generating {n} random amplitudes...")
        amplitudes = 50 * np.random.rand(1,n) """
        amplitudes = np.array([10])

    if not Fs:
        Fs = 5000
        print(f"Sampling is {Fs}")

    if not frequencies[0]:
        """ print("-------------------------------")
        print("No frequencies, list is empty.")
        print(f"Generating {n} random frequencies...")
        #n Frequencies between [0,100)
        list_numbers = np.linspace(30,max_freq_input,n)
        frequencies = list_numbers * np.random.rand(1,n) """
        frequencies = np.array([440])


    n_signals = len(frequencies)

    # Set variables
    T = 1/(Fs) 
    N = Fs
    

    #   ADSR(y, list_ADSR, N, sustainAmplitude = 0.7, maxAmplitude = 1):
    if isinstance(list_ADSR, list):
        print("APPLY ADSR", list_ADSR)


        t = np.sum(list_ADSR)
        omega = 2*np.pi*frequencies 
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
        t = 1

        Amp_array = 1
        N = Fs 
        omega = 2*np.pi*frequencies 
        t_vec = np.arange(N)*(T*t) 
        y = np.zeros((n_signals,len(t_vec)))
        k = 0
        y_sum = 0
        for i in omega:
            y[k] = (Amp_array * amplitudes[k]) * np.sin(i*t_vec)
            y_sum += y[k] 
            k += 1 


    normalized_y = y_sum/np.max(y_sum) 

    #plot_array(t_vec, normalized_y,  "Normalized", "t[s]", "A[m]", "y", "r", "-", True, "normalized.pdf")

    #Apply low-pass filter
    cutoff_low = np.max(frequencies)-20
    cutoff_high = np.min(frequencies)
    order = int(cutoff_low/2)


    y_low = low_pass_Filter(normalized_y, Fs, cutoff_low, order)
    """
    y_highlow = high_pass_Filter(y_low, Fs, cutoff_high, order)

    """




    """ 
   


    
    plt.figure()
    plot_array(t_vec, y_low_and_high,  "Filtered", "t[s]", "A[m]", "y", "r", "-", "True", "filtered.pdf")
    """
    #plt.show()
    #Variables for different function calls

    #Apply color
    #y_filtered_noise = coloredNoise(exponent = 2, y = normalzed_y, fmin = 0.1, noise_intensity=0.1)

    # PLot varibles
    #plt.plot(y, t_vec, title, xlabel, ylabel, label_graph, color_graph, ls_graph, save, filename):
    # plot_array(t_vec, y_sum,  "Y + Saw", "t[s]", "A[m]", "Saw", "r", "-", "False", "Saw.pdf")

    #Reverb signal
    
    """ 
    reverbed_signal = reverb_filter(y = normalized_y,  sampleRate = Fs, mixPercent = 50)
    reverbed_signal1_1 = reverb_filter(y = normalized_y,  sampleRate = Fs, mixPercent = 50)
    reverbed_signal1 = reverb_filter(y = y_low, sampleRate = Fs, mixPercent = 50)
    reverbed_signal2 = reverb_filter(y = normalized_y, sampleRate = Fs, mixPercent = 1)
    reverbed_signal3 = reverb_filter(y = normalized_y, sampleRate = Fs, mixPercent = 1) 
    """
 

    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")

    """ Array_of_various_signals = [[y_sum],[normalzed_y], [y_filtered_low],\
         [y_filtered_high] , [y_filtered], [LFO], [y_filtered_LFO], [y_filtered_noise], [saw], [y_filtered_saw]] """
    return t_vec, Fs, frequencies#, Array_of_various_signals#, norm_max



t0_func = time.time()
print("Timing outside func started....")

#t_vec, Fs, freqs, Array_of_various_signals = Create_Sine(np.array([10,10,10,10,10,10,10]), np.array([200, 400, 450, 500, 550, 600, 800]), 44100, list_ADSR = 0)
t_vec, Fs, freqs = Create_Sine(np.array([2, 1, 1, 2]), np.array([50, 100, 300, 350]), 44100, list_ADSR = 0)

t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



