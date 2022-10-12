import time
import numpy as np 
import matplotlib.pyplot as plt
from filterAudio import low_pass_Filter, high_pass_Filter, Low_frequency_Oscillator
#from soundGen import play
from pointsFrequency import signal_to_hertz
from ADSR_mod import ADSR
plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies,Fs, list_ADSR = 0):
    t0 = time.time()
    print("Timing started ADSR....")

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
        print("NOT NOT ADSR")
        t = 10
        Amp_array = 1
        N = Fs/t
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
        plt.show() """
        k += 1 
    #Apply low-pass filter


    normalzed_y = y_sum/np.max(y_sum) 
    plt.plot(t_vec, normalzed_y)
    plt.title("Normalized")
    plt.xlabel("t [s]")
    plt.ylabel("A [m]")
    plt.savefig(f"backend/figures/demo/Normalized.png")
    plt.show()


    cutoff_low = np.max(frequencies) - 10
    cutoff_high = np.min(frequencies) + 10

    print(cutoff_low)
    print(cutoff_high)

    y_filtered_low = low_pass_Filter(normalzed_y, Fs, cutoff_low, 5)

    y_filtered_high = high_pass_Filter(normalzed_y, Fs, cutoff_high, 5)
    
    y_filtered =  y_filtered_low + y_filtered_high

    #Apply low_frequency_oscillator
    """ LFO = Low_frequency_Oscillator(20, t_vec, amplitudes[0])
    y_sum_LFO = y_sum + LFO """


    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")

    plt.figure(1)
    plt.title("Filtered Low")
    plt.xlabel("t [s]")
    plt.ylabel("A [m]")
    plt.plot(t_vec, y_filtered_low)
    plt.savefig(f"backend/figures/demo/Filtered_low.png")

    
    plt.figure(2)
    plt.title("Filtered High")
    plt.xlabel("t [s]")
    plt.ylabel("A [m]")
    plt.plot(t_vec, y_filtered_high)
    plt.savefig(f"backend/figures/demo/Filtered_high.png")

    plt.figure(3)
    plt.title("Filtered High and Low with y on top")
    plt.xlabel("t [s]")
    plt.ylabel("A [m]")
    plt.plot(t_vec, y_filtered, label= "y filtered", color= 'b')
    plt.plot(t_vec, normalzed_y, label= "Normalized", color ='r', ls='--')
    plt.savefig(f"backend/figures/demo/Filtered_cutoff.png")
    plt.legend()
   
    plt.show() 

    return t_vec, normalzed_y, Fs, frequencies#, norm_max

t0_func = time.time()
print("Timing outside func started....")




t_vec, normalized_y_filtered, Fs, freqs = Create_Sine(np.array([10,3,5,14]), np.array([20, 90, 110, 140]), 44100, list_ADSR = 0)


signal_to_hertz(normalized_y_filtered, Fs, freqs)




""" t_vec, y_sum2, Fs = Create_Sine(np.array([40]), np.array([392]), 44100, list_ADSR = [10,10,-1,0])
t_vec, y_sum3, Fs = Create_Sine(np.array([40]), np.array([349]), 44100, list_ADSR = [10,10,-1,0])
t_vec, y_sum4, Fs = Create_Sine(np.array([40]), np.array([329.63]), 44100, list_ADSR = [10,10,-1,0])
y_sum_again = y_sum1 + y_sum2 + y_sum3 + y_sum4 """
""" plt.plot(t_vec, y_sum1)
plt.savefig("lyd1.png")
plt.show() """

# Making a long signal that is continuous
""" 
m = 7
len_y = len(y_sum_again)
ext_y = np.zeros(len_y*m)
beta = 1         # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
samples = len_y*m  # number of samples to generate (time series extension)

Color_noise = cn.powerlaw_psd_gaussian(beta, samples, fmin = 0.5)
Color_noise1 = cn.powerlaw_psd_gaussian(2, samples, fmin = 0.5)
Color_noise2 = cn.powerlaw_psd_gaussian(0, samples, fmin = 0.5)
 """

t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



