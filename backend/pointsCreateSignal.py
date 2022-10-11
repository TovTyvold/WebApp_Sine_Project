from matplotlib.ft2font import BOLD
import time
import numpy as np 
import matplotlib.pyplot as plt
from envelope import fade_in_func, decay_func, fade_out_func, sustain_func
from filterAudio import low_pass_Filter
plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies,Fs):
    n = np.random.randint(3,10)
    t0 = time.time()
    print("Timing started....")
    if not amplitudes:
        """ print("-------------------------------")
        print("No amplitudes, list is empty.")
        print(f"Generating {n} random amplitudes...")
        amplitudes = 50 * np.random.rand(1,n) """
        amplitudes = np.array([10])

    if not Fs:
        Fs = 5000
        print(f"Sampling is {Fs}")


    if not frequencies:
        max_freq_input = Fs/2
        """ print("-------------------------------")
        print("No frequencies, list is empty.")
        print(f"Generating {n} random frequencies...")
        #n Frequencies between [0,100)
        list_numbers = np.linspace(30,max_freq_input,n)
        frequencies = list_numbers * np.random.rand(1,n) """
        frequencies = np.array([Fs/2])


    n_signals = len(frequencies)

    """ min_freq = np.min(frequencies)
    max_freq = np.max(frequencies)
    """
    # Set variables
    T = 1/(Fs) # sampling period
    #t = max_freq/(n_signals * (1/2) * min_freq) # seconds of sampling
    t = 1
    N = (Fs*t)/10 # total points in signal
    omega = 2*np.pi*frequencies # angular frequency for sine waves
    t_vec = np.arange(N)*T # time vector for plotting
    y = np.zeros((n_signals,len(t_vec)))

    k = 0
    y_sum = 0
    for i in omega:
        y[k] = amplitudes[k] * np.sin(i*t_vec)
        #y[k] = np.sin(i[k]*t_vec) #Amplitude == 1
        y_sum += y[k] 
        k += 1 
    
    """
    Blocks for ENVELOPE
    """
    duration = N


    """ def envelope_slice(y_sum) """
    # List is [Fade_in, Decay, Sustain, Fade_out]
    boolean_env = [True, True, True, True]
    #boolean_env = [True, False, False, True]
    
    dur_scale = boolean_env.count(True)
    n_dur = int(duration / dur_scale)
    dur_list = [0, 0, 0, 0]



    counter = 0
    for i in boolean_env:
        if i == True:
            dur_list[counter] = n_dur
        counter += 1

    fade_in_duration = dur_list[0]
    decay_duration = dur_list[1]
    sustain_duration = dur_list[2]
    fade_out_duration = dur_list[3]

    if boolean_env[0] == True:
        y_sum = fade_in_func(y_sum, fade_in_duration)
    
    #Decay
    if boolean_env[1] == True:
        if boolean_env[0] == True:
            y_sum, decay_val = decay_func(y_sum, decay_duration, fade_in_duration)
            
        else:
            y_sum, decay_val = decay_func(y_sum, decay_duration, fade_duration = 0)

    #Sustain
    if boolean_env[2] == True:
        if boolean_env[1] == True:
            y_sum, sustain_val = sustain_func(y_sum, sustain_duration, fade_in_duration, decay_duration, decay_val)

        elif boolean_env[1] == False:
            y_sum, sustain_val = sustain_func(y_sum, sustain_duration, fade_in_duration, decay_duration, decay_val = 1)


    #Fade out
    if boolean_env[3] == True: 
        y_sum = fade_out_func(y_sum, fade_out_duration, sustain_val)


    #Apply low-pass filter
    y_filtered = low_pass_Filter(t_vec, y_sum, Fs)
                
    
    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped! It took {total:0.7f}s")

    plt.figure()
    plt.title(f"Attack: {boolean_env[0]}, Decay: {boolean_env[1]}, Sustain: {boolean_env[2]} and Release: {boolean_env[3]}. ", fontsize=8)
    #plt.xscale('log')
    plt.plot(t_vec, y_filtered)
    plt.savefig(f"enve{dur_scale, Fs}.png")
    #plt.show()

    #norm_max = y_sum/np.max(y_sum)
    return t_vec, y_sum, Fs#, norm_max

t0_func = time.time()
print("Timing outside func started....")
for i in range(2,5):
    Fs = 10**i
    Create_Sine([], [], Fs)

t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")
