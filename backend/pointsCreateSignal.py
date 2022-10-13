import time
import numpy as np 
import matplotlib.pyplot as plt
from filterAudio import low_pass_Filter, high_pass_Filter, Low_frequency_Oscillator_sine, Low_frequency_Oscillator_saw, reverb_filter
from soundGen import play
from pointsFrequency import signal_to_hertz
from ADSR_mod import ADSR
from pointsNoise import coloredNoise
from plotting import plot_array

plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies,Fs, list_ADSR = 0):
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
    
    if isinstance(list_ADSR, list):
        print("APPLY ADSR")
        for i in range(4):
            list_ADSR[i] = np.random.randint(1,7)

        print(list_ADSR)
        t = np.sum(list_ADSR)

        Amp_array = ADSR(list_ADSR, N, t)


        omega = 2*np.pi*frequencies 
        t_vec = np.arange(N)*T 
        y = np.zeros((n_signals,len(t_vec)))

    
    else:
        t = 5
        Amp_array = 1
        N = Fs*t
        omega = 2*np.pi*frequencies 
        t_vec = np.arange(N)*T 
        y = np.zeros((n_signals,len(t_vec)))

    k = 0
    y_sum = 0
    for i in omega:
        y[k] = (Amp_array * amplitudes[k]) * np.sin(i*t_vec)
        y_sum += y[k] 
        """ plt.figure(k+1)
        plt.plot(t_vec,y[k])
        plt.title(f"Plot of Wave nr:{k+1}")
        plt.xlabel("t [s]")
        plt.ylabel("A [m]") 
        plt.savefig(f"backend/figures/demo/wave_nr_{k+1}.png")
        #plt.show() """
        k += 1 
    #Apply low-pass filter


    normalzed_y = y_sum/np.max(y_sum) 
    """ plt.plot(t_vec, normalzed_y)
    plt.title("Normalized")
    plt.xlabel("t [s]")
    plt.ylabel("A [m]")
    plt.savefig(f"backend/figures/demo/Normalized.png")
    #plt.show() """


    cutoff_low = np.max(frequencies)+10
    cutoff_high = np.min(frequencies)

    """ #plt.figure()
    y_filtered_low = low_pass_Filter(normalzed_y, Fs, cutoff_low, 5)
    signal_to_hertz(y_filtered_low, Fs, frequencies, label = "Low")
    

    #plt.figure()
    y_filtered_high = high_pass_Filter(normalzed_y, Fs, cutoff_high, 5)
    signal_to_hertz(y_filtered_high, Fs, frequencies, label = "High")
    #plt.show()

    y_filtered =  y_filtered_low + y_filtered_high



    # FFT FETCH
    #plt.figure()
    signal_to_hertz(y_filtered, Fs, frequencies, label = "")

    #plt.figure()
    signal_to_hertz(normalzed_y, Fs, frequencies, label = "Before Filter")
    #plt.show()

    #Apply low_frequency_oscillator sine/saw
    LFO = Low_frequency_Oscillator_sine(20, t_vec, np.max(y_filtered)/10)
    y_filtered_LFO = y_filtered + LFO

    saw = Low_frequency_Oscillator_saw(np.min(frequencies[0]), t_vec, 1)
    y_filtered_saw = y_filtered + saw
 """

    #Apply color
    #y_filtered_noise = coloredNoise(exponent = 2, y = normalzed_y, fmin = 0.1, noise_intensity=0.1)

    #(y, t_vec, title, xlabel, ylabel, label_graph, color_graph, ls_graph):

    # amp is amp of impulse response
    reverb_y = reverb_filter(y_sum, mode = 'same', amp = 30)
    play(reverb_y + y_sum)
    plt.figure
    plot_array(t_vec, reverb_y,  "Reverb", "t[s]", "A[m]", "y with reverb", "r", "--")
    plt.show()


    """ plt.figure
    plot_array(t_vec, y_filtered_noise,  "Noise", "t[s]", "A[m]", "y filtered noise", "r", "--")

    plt.figure()
    plot_array(t_vec, normalzed_y, "Filtered", "t[s]", "A[m]", "y filtered", "r", "--")
    plt.show() """


    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")

    """ Array_of_various_signals = [[y_sum],[normalzed_y], [y_filtered_low],\
         [y_filtered_high] , [y_filtered], [LFO], [y_filtered_LFO], [y_filtered_noise], [saw], [y_filtered_saw]] """
    return t_vec, Fs, frequencies#, Array_of_various_signals#, norm_max



t0_func = time.time()
print("Timing outside func started....")

#t_vec, Fs, freqs, Array_of_various_signals = Create_Sine(np.array([10,10,10,10,10,10,10]), np.array([200, 400, 450, 500, 550, 600, 800]), 44100, list_ADSR = 0)
t_vec, Fs, freqs = Create_Sine(np.array([10,10,10,10,10,10,10]), np.array([200, 400, 450, 500, 550, 600, 800]), 44100, list_ADSR = 0)


""" print("PLAYING SOUNDS")
#play(Array_of_various_signals[5][0])
for i in Array_of_various_signals:
    play(i[0])
    time.sleep(0.5) """

t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



