# sampling a sine wave programmatically
from distutils import core
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
plt.style.use('ggplot')


# Number of signals i.e. functions
n_signals = 10

#List for multiple colors for multiple plots
color_mix = cm.rainbow(np.linspace(0, 1, n_signals))


a = np.random.rand(1,n_signals)
#n Frequencies between [0,100)
list_numbers = np.linspace(30,1000,n_signals)
list_rand_freq = list_numbers * np.random.rand(1,n_signals)
print(list_rand_freq)
#n Amplitudes between [0,15)
list_rand_amps = 15 * np.random.rand(1,n_signals)

min_freq = np.min(list_rand_freq)
max_freq = np.max(list_rand_freq)

# sampling information
# Prone to be changed, might be too high
Fs = 44100 # sample rate
T = 1/Fs # sampling period

t = max_freq/(n_signals * (1/2) * min_freq) # seconds of sampling
N = Fs*t # total points in signal




""" freq = np.array([50, 400, 180, 2000, 140, 350]) # in hertz, the desired natural frequency
amp = [7, 2, 5, 1, 3.5, 1.5] """




omega = 2*np.pi*list_rand_freq # angular frequency for sine waves
t_vec = np.arange(N)*T # time vector for plotting
y = np.zeros((n_signals,len(t_vec)))

# Need to fix the intervall
k = 0
y_sum = 0
for i in omega[0]:
    #y[k][:] = amp[k] * np.sin(i*t_vec)
    y[k] = np.sin(i*t_vec) #Amplitude == 1
    y_sum += y[k] 
    #plt.plot(t_vec,y[k], color = color_mix[k])
    k += 1 
    
#plt.show() 


# In the future, this will be the audio submitted
norm_max = y_sum/np.max(y_sum)
""" plt.plot(t_vec,norm_max)
plt.show() """


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
    amp_list = []

    for k in range(1,len(Pxx)-1):
        if Pxx[k-1] < Pxx[k] and Pxx[k] > Pxx[k+1]:
            amp_list.append(Pxx[k])
            freq_list.append(f[k])


    return f, Pxx, freq_list, amp_list


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




#Plot 
#----------------------------------------------------------------------------
print("Checking frequencies...")
sorted_rand_freq = np.sort(list_rand_freq)
f, Pxx, freq_list, amp_list = chaos_to_hertz(norm_max)
#np. set_printoptions(threshold=np. inf)
tol = 2
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

        
print("-----------------------------")

print("Number of elements in freq_list: ", np.shape(freq_list))
print("Number of elements in list_rand_freq: ", np.shape(list_rand_freq))

""" print(f"All the frequencies are, in ascending order, {freq_list}")
print(f"All the amplitudes are, in ascending order, {amp_list}")
 """
print("Plotting")
fig,ax = plt.subplots()
print(len(f))
print(len(Pxx))
if len(f) != len(Pxx):
    a = len(f) - len(Pxx) 
    f = f[:-a]
plt.plot(f,Pxx, marker='o', ms=5, markerfacecolor='blue')
ax.set_xscale('log')
#ax.set_yscale('log')
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
plt.savefig(f"fft' {n_signals,Fs}'.png")
#plt.show()
