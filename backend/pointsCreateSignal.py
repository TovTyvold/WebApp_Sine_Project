import time
import numpy as np 
import matplotlib.pyplot as plt
from filterAudio import low_pass_Filter, high_pass_Filter, Low_frequency_Oscillator
#from soundGen import play
from ADSR_mod import ADSR
plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies,Fs, list_ADSR = False):
    t0 = time.time()
    print("Timing started....")

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
    t_org = 1
    t = np.sum(list_ADSR)
    N = (Fs) 
    omega = 2*np.pi*frequencies 
    t_vec = np.arange(N)*T 
    y = np.zeros((n_signals,len(t_vec)))

    Amp_array = ADSR(list_ADSR, N, t)

    """ if t != 1 and isinstance(list_ADSR, list):
        Amp_array = np.zeros(N)
        A_time = int((len(t_vec)*list_ADSR[0])/t)
        D_time = int((len(t_vec)*list_ADSR[1])/t)
        S_time = int((len(t_vec)*(t_org + list_ADSR[2]))/t)
        R_time = int((len(t_vec)*list_ADSR[3])/t)
        A = np.zeros(A_time)
        D = np.zeros(D_time)
        S = np.zeros(S_time)
        R = np.zeros(R_time)

        A_lin = np.linspace(0,4,A_time)
        D_lin = np.linspace(4,0.5,D_time)
        R_lin = np.linspace(0.5,0,R_time)
        Attack = A + A_lin
        Decay = D + D_lin
        Sustain = S + 0.5
        Release = R + R_lin

        Prog_1 = A_time + D_time
        Prog_2 = A_time + D_time + S_time
    

        Amp_array[:A_time] = Attack
        Amp_array[A_time:Prog_1] = Decay
        Amp_array[Prog_1:Prog_2] = Sustain
        Amp_array[Prog_2:Prog_2 + R_time] = Release

    else:
        Amp_array = 1
        t = 1
        N = Fs*t
        omega = 2*np.pi*frequencies 
        t_vec = np.arange(N)*T 
        y = np.zeros((n_signals,len(t_vec)))
 """
    k = 0
    y_sum = 0

    for i in omega:
        y[k] = (Amp_array * amplitudes[k]) * np.sin(i*t_vec)
        y_sum += y[k] 
        k += 1 

    #Apply low-pass filter
    y_filtered_low = low_pass_Filter(y_sum, Fs, 0.7*frequencies[0], 5)

    y_filtered_high = high_pass_Filter(y_sum, Fs, 0.3*frequencies[0], 10)
    
    y_filtered = y_filtered_high + y_filtered_low

    #Apply low_frequency_oscillator
    LFO = Low_frequency_Oscillator(20, t_vec, amplitudes[0])
    y_sum_LFO = y_sum + LFO





    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")

    plt.figure(1)
    plt.plot(t_vec, y_sum)


    plt.figure(2)
    plt.plot(t_vec, y_sum_LFO)
    plt.show() 

    return t_vec, y_filtered, Fs#, norm_max

t0_func = time.time()
print("Timing outside func started....")

t_vec, y_sum1, Fs = Create_Sine(np.array([40]), np.array([440]), 44100, list_ADSR = [0,0,1,1])
""" t_vec, y_sum2, Fs = Create_Sine(np.array([40]), np.array([392]), 44100, list_ADSR = [10,10,-1,0])
t_vec, y_sum3, Fs = Create_Sine(np.array([40]), np.array([349]), 44100, list_ADSR = [10,10,-1,0])
t_vec, y_sum4, Fs = Create_Sine(np.array([40]), np.array([329.63]), 44100, list_ADSR = [10,10,-1,0])
y_sum_again = y_sum1 + y_sum2 + y_sum3 + y_sum4 """
plt.plot(t_vec, y_sum1)
plt.savefig("lyd1.png")
plt.show()

# Making a long signal that is continuous
""" m = 7
len_y = len(y_sum_again)
ext_y = np.zeros(len_y*m)
beta = 1         # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
samples = len_y*m  # number of samples to generate (time series extension)

Color_noise = cn.powerlaw_psd_gaussian(beta, samples, fmin = 0.5)
Color_noise1 = cn.powerlaw_psd_gaussian(2, samples, fmin = 0.5)
Color_noise2 = cn.powerlaw_psd_gaussian(0, samples, fmin = 0.5)

ext_y[:len_y] = y_sum1
ext_y[len_y:2*len_y] = y_sum1 
ext_y[2*len_y:3*len_y] = y_sum1
ext_y[3*len_y:4*len_y] = y_sum4
ext_y[4*len_y:int(4.5*len_y)] = y_sum3[:22050]
ext_y[int(4.5*len_y):5*len_y] = y_sum3[:22050]
ext_y[5*len_y:6*len_y] = y_sum4
ext_y[6*len_y:int(6.5*len_y)] = y_sum3[:22050]
ext_y[int(6.5*len_y):7*len_y] = y_sum3[:22050]

ext_y = ext_y + Color_noise/20 + Color_noise1/20 + Color_noise2/20
 """

t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



