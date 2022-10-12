from matplotlib.ft2font import BOLD
import time
import numpy as np 
import matplotlib.pyplot as plt
import colorednoise as cn
from filterAudio import low_pass_Filter, high_pass_Filter
from soundGen import play
import subprocess as sp
FFMPEG_BIN = "ffmpeg.exe"
plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies,Fs, list_ADSR):

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

    """ if not phase[0]:
        print("-------------------------------")
        print("No phase, list is empty.")
        print(f"Generating {n} random phases...")
        #n phases between [0,5)
        list_numbers = np.linspace(1,5,n)
        frequencies = list_numbers * np.random.rand(1,n)
        phase = np.array([1]) """




    n_signals = len(frequencies)

    # Set variables
    T = 1/(Fs) 
    t_org = 1
    t = t_org + np.sum(list_ADSR)
    N = (Fs) 
    omega = 2*np.pi*frequencies 
    t_vec = np.arange(N)*T 
    y = np.zeros((n_signals,len(t_vec)))


    if t != 0:
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

    k = 0
    y_sum = 0

    for i in omega:
        y[k] = (Amp_array * amplitudes[k]) * np.sin(i*t_vec)
        y_sum += y[k] 
        k += 1 

    #Apply low-pass filter
    frequencies = sorted(frequencies)
    cutoff_high = frequencies[-1]
    print(cutoff_high)
    order_low = 5
    y_filtered_high = high_pass_Filter(y_sum, Fs, cutoff_high, order_low)

    cutoff_low = frequencies[0]
    order_high = 10
    y_filtered_low = low_pass_Filter(y_sum, Fs, cutoff_low, order_high)
    
    y_filtered = y_filtered_high + y_filtered_low
    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped! It took {total:0.7f}s")

    """ plt.figure()
    plt.plot(t_vec, y_filtered)
    plt.show() """

    return t_vec, y_filtered, Fs#, norm_max

t0_func = time.time()
print("Timing outside func started....")

t_vec, y_sum1, Fs = Create_Sine(np.array([40]), np.array([440]), 44100, list_ADSR = [10,10,-1,0])
t_vec, y_sum2, Fs = Create_Sine(np.array([40]), np.array([392]), 44100, list_ADSR = [10,10,-1,0])
t_vec, y_sum3, Fs = Create_Sine(np.array([40]), np.array([349]), 44100, list_ADSR = [10,10,-1,0])
t_vec, y_sum4, Fs = Create_Sine(np.array([40]), np.array([329.63]), 44100, list_ADSR = [10,10,-1,0])
y_sum_again = y_sum1 + y_sum2 + y_sum3 + y_sum4
""" plt.plot(t_vec, y_sum_again)
plt.savefig("lyd1.png")
plt.show() """

""" m = 7
len_y = len(y_sum_again)
ext_y = np.zeros(len_y*m)
beta = 1         # the exponent: 0=white noite; 1=pink noise;  2=red noise (also "brownian noise")
samples = len_y*m  # number of samples to generate (time series extension)

Color_noise = cn.powerlaw_psd_gaussian(beta, samples, fmin = 0.5)
Color_noise1 = cn.powerlaw_psd_gaussian(2, samples, fmin = 0.5)
Color_noise2 = cn.powerlaw_psd_gaussian(0, samples, fmin = 0.5)
 """

""" for i in range(m):
    ext_y[i*len_y:(i+1)*len_y] = 
 """


""" ext_y[:len_y] = y_sum1
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


""" pipe = sp.Popen([ FFMPEG_BIN,
       '-y', # (optional) means overwrite the output file if it already exists.
       "-f", 's16le', # means 16bit input
       "-acodec", "pcm_s16le", # means raw 16bit input
       '-r', "44100", # the input will have 44100 Hz
       '-ac','2', # the input will have 2 channels (stereo)
       '-i', '-', # means that the input will arrive from the pipe
       '-vn', # means "don't expect any video input"
       '-acodec', "libfdk_aac" # output audio codec
       '-b', "3000k", # output bitrate (=quality). Here, 3000kb/second
       'my_awesome_output_audio_file.mp3'],
        stdin=sp.PIPE,stdout=sp.PIPE, stderr=sp.PIPE)
print("yo")
ext_y.astype("int16").tofile(pipe)
 """
t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")





print("Running with Brage's point calc")
from pointsCalculation import getPoints, parseDict

periodicFunc_list = [parseDict({"shape" : "sin","frequency" : 440,"amplitude": 1})]
sampleRate = 44100
y_sum_brage = getPoints(periodicFunc_list, 44100)
play(y_sum_brage[1])

y_filtered_low = low_pass_Filter(y_sum_brage[1], Fs, 0.7*periodicFunc_list[0].frequency, 10)
plt.figure(1)
plt.title("Low Pass")
plt.plot(t_vec,y_filtered_low)
play(y_filtered_low)
plt.show()


y_filtered_high = high_pass_Filter(y_sum_brage[1], Fs, 0.3*periodicFunc_list[0].frequency, 10)
plt.figure(2)
plt.title("High Pass")
plt.plot(t_vec, y_filtered_high)
play(y_filtered_high)

plt.show()


