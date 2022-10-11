# sampling a sine wave programmatically
import sys
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
plt.style.use('ggplot')

"""
-----------------------------------------------------------------
PYTHON SCRIPT MADE TO TEST SIGNALS WITH VARYING AMPLITUDES
-----------------------------------------------------------------
"""

"""
-----------------------------------------------------------------
CHANGES TO BE MADE:
    - MANAGE RELATIONS BETWEEN ADDING AMPLITUDES
    AND THE VARIABLE "t" AS WELL AS "max_freq_input".
-----------------------------------------------------------------
"""

# Number of signals i.e. functions
n_signals = 5

#List for multiple colors for multiple plots
color_mix = cm.rainbow(np.linspace(0, 1, n_signals))

#Cap at 22000
max_freq_input = 100
a = np.random.rand(1,n_signals)

#n Frequencies between [0,100)
list_numbers = np.linspace(1,max_freq_input,n_signals)
list_rand_freq = list_numbers * np.random.rand(1,n_signals)
#print(list_rand_freq)


#n Amplitudes between [0,15)
list_rand_amps = 5 * np.random.rand(1,n_signals)

#Temporary for debugging
""" list_rand_amps = np.array([[12, 3, 1, 9, 7]])
list_rand_freq = np.array([[5, 10, 15, 20, 25]]) """



min_freq = np.min(list_rand_freq)
max_freq = np.max(list_rand_freq)

# sampling information
# Prone to be changed, might be too high
Fs = max_freq_input*2 # sample rate
T = 1/Fs # sampling period
t = max_freq/(n_signals * (1/2) * min_freq) # seconds of sampling
N = Fs*t # total points in signal
t_vec = np.arange(N)*T # time vector for plotting



""" freq = np.array([50, 400, 180, 2000, 140, 350]) # in hertz, the desired natural frequency
amp = [7, 2, 5, 1, 3.5, 1.5] """




omega = 2*np.pi*list_rand_freq # angular frequency for sine waves

y = np.zeros((n_signals,len(t_vec)))

# Need to fix the intervall
k = 0
y_sum = 0
for i in omega[0]:
    y[k] = list_rand_amps[0][k] * np.sin(i*t_vec)
    #y[k] = np.sin(i*t_vec) #Amplitude == 1
    y_sum += y[k] 
    #plt.plot(t_vec,y[k], color = color_mix[k])
    k += 1 
    
#plt.show() 


# In the future, this will be the audio submitted
norm_max = y_sum/np.max(y_sum)
plt.plot(t_vec,norm_max)
#plt.show()


def chaos_to_hertz(norm_max):
    """  
        Function that outputs frequencies after taking in a signal with/without noise/chaos using fft. 
        ---------
        norm_max - dtype ndarray: An ndarray with (x,y) values 
        Fs - dtype int: The sample rate

        Returns
        --------

    """
    length = len(norm_max)
    
    Y_k = np.fft.fft(norm_max)[0:int(length/2)]/length # FFT function from numpy
    Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
    Pxx = np.abs(Y_k) # be sure to get rid of imaginary part
    

    f = Fs*np.arange((length/2))/length; # frequency vector

    freq_list = []
    power_list = []
    Amps = []

    for k in range(1,len(Pxx)-1):
        if Pxx[k-1] < Pxx[k] and Pxx[k] > Pxx[k+1]:
            power_list.append(Pxx[k])
            freq_list.append(f[k])
            Amps.append(Pxx[k]/length)


    return f, Pxx, freq_list, power_list, length, Amps


#Compare the values, used when method above is also used
#----------------------------------------------------------------------------
""" 
#The other way, CAN BE USED FOR COMPARISON
Y_s = np.fft.fft(norm_max)
Pxx2 = np.abs(Y_s/N)
Pxx1 = Pxx2[0:int(N/2)]
Pxx1[1:-1] = 2 * Pxx1[1:-1]
 """

""" print(np.shape(Pxx))
print(np.shape(Pxx1))
tol = 1e-7
for k in range(len(Pxx)):
    if tol > abs(Pxx[k] - Pxx1[k]):
        print(Pxx[k])
        print(Pxx1[k])
        print("Not Alike")
        break """




#Check Frequencies gathered
#----------------------------------------------------------------------------
print("Checking frequencies...")
sorted_rand_freq = np.sort(list_rand_freq)
f, Pxx, freq_list, power_list, length, Amps = chaos_to_hertz(norm_max)

print("-----------------------------")
np.set_printoptions(threshold=sys.maxsize)
print(f"Number of elements in freq_list: {np.shape(freq_list)[0]:.0f}")
print(freq_list)
print(f"Number of elements in list_rand_freq: {np.shape(sorted_rand_freq)[1]:.0f}")
print(np.sort(sorted_rand_freq))



tol = 1
for k in range(n_signals):
    if tol < abs(sorted_rand_freq[0][k] - freq_list[k]):
        print(sorted_rand_freq[0][k])
        print(freq_list[k])
        print("Not Alike")
        print("-------------")
    else:
        print(sorted_rand_freq[0][k])
        print(freq_list[k])
        print("-------------")


print("mean freq:", np.mean(freq_list))
print("-------------")
freq_mean2 = np.mean(freq_list)
for j in range(len(freq_list)-1):
    if abs(freq_list[j+1] - freq_list[j]) > freq_mean2:
        freq_list = freq_list[:j]
        break 
      

#Find the Amplitudes using the Power list with physics(seems to require mechanical waves, whatever that means)
#----------------------------------------------------------------------------
""" #Mass of the signal: m == 1
m = 1
#Length of the signal: length == length
L = length 
#Linear density of the wave
mu = m/L
#Set wave speed to 1
v = 1
#The angular frequency
#omega_list = 2 * np.pi * freq_list
#Rearrange formula found in https://openstax.org/books/university-physics-volume-1/pages/16-4-energy-and-power-of-a-wave#:~:text=The%20time%2Daveraged%20power%20of,by%20a%20factor%20of%20four.
A = np.zeros(len(freq_list))
for i in range(len(freq_list)):
    omega_iterate = 2 * np.pi * freq_list[i]
    A[i] = np.sqrt(2 * power_list[i] * L)/omega_iterate

#Check if the relationship P ~ A^2 
A_new = np.zeros(len(freq_list))
for i in range(len(freq_list)):
    A_new[i] = np.sqrt(power_list[i]) """



def chaos_to_Amps(norm_max, freq_list):
    from scipy.signal import kaiserord, lfilter, firwin, freqz, find_peaks_cwt
    """  
        Function that outputs amplitudes after taking in a signal with/without noise using filtering. 
        ---------

        Inputs
        ---------
        norm_max - dtype ndarray: An ndarray with (x,y) values 
        Fs - dtype int: The sample rate

        Returns
        --------

    """
    max_freq = np.max(freq_list)
    min_freq = np.min(freq_list)
    t = max_freq/(len(freq_list) * (1/2) * min_freq)

    length = len(norm_max)
    print(length)
    samples = length
    sample_rate = samples/2

    total_points = samples*t
    T = 1/samples # sampling period
    t_vec = np.arange(total_points)*T # time vector for plotting




    # Prone to be changed, might be too high
    Fs = max_freq_input*2 # sample rate
    T = 1/Fs # sampling period
    t = max_freq/(n_signals * (1/2) * min_freq) # seconds of sampling
    N = Fs*t # total points in signal
    t_vec = np.arange(N)*T # time vector for plotting









    nyq_rate = sample_rate/2
    width = 5/nyq_rate
    ripple_db = 60.0
    # The cutoff frequency of the filter.
    cutoff_hz = 10.0
    
    



    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)

    

    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    filtered_x = lfilter(taps, 1.0, norm_max)

    plt.plot(t_vec, filtered_x)
    #plt.savefig(f"filter{cutoff_hz, ripple_db, width}.png")
    plt.show()

    return filtered_x

amps = chaos_to_Amps(norm_max, freq_list)


#Check Amplitudes gathered
#----------------------------------------------------------------------------
""" print("Checking Amplitudes...")
sorted_rand_amp = np.sort(list_rand_amps)
sort_amp_list = np.sort(Amps)
#Print amplitudes from fucn returns
print("Print size of amplitudes from func returns: ", np.shape(Amps))

print("-----------------------------")
np.set_printoptions(threshold=sys.maxsize)
print(f"Number of elements in sort_amp_list: {np.shape(sort_amp_list)[0]:.0f}")
print(sort_amp_list)
print(f"Number of elements in list_rand_amp: {np.shape(list_rand_amps)[1]:.0f}")
print(np.sort(list_rand_amps))

#np. set_printoptions(threshold=np. inf)
tol = 1
for k in range(n_signals):
    if tol < abs(sorted_rand_amp[0][k] - sort_amp_list[k]):
        print(sorted_rand_amp[0][k])
        print(sort_amp_list[k])
        print("Not Alike")
        print("-------------")
    else:
        print(sorted_rand_amp[0][k])
        print(sort_amp_list[k])
        print("-------------")


print("mean amp:", np.mean(Amps))
print("-------------")
amp_mean2 = np.mean(Amps)
for j in range(len(Amps)-1, 1,-1):
    if abs(sort_amp_list[j]- sort_amp_list[j-1]) < amp_mean2:
        continue
    else:
        sort_amp_list = sort_amp_list[j:]
        break  """

        







""" print(f"All the frequencies are, in ascending order, {freq_list}")
print(f"All the amplitudes are, in ascending order, {amp_list}")
 """


#Plotting section
#----------------------------------------------------------------------------
""" print("Plotting")
fig,ax = plt.subplots()
if len(f) != len(Pxx):
    a = len(f) - len(Pxx) 
    f = f[:-a]
plt.plot(f,Pxx, marker='o', ms=5, markerfacecolor='blue')
ax.set_xscale('log')
#ax.set_yscale('log')
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
#plt.savefig(f"fft' {n_signals, Fs, max_freq_input}'.png")
plt.show()
#print(f"Saved plot as: fft {n_signals, Fs, max_freq_input}")
 """