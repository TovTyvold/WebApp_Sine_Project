# sampling a sine wave programmatically
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# sampling information
# Prone to be changed, might be too high
Fs = 44100 # sample rate
T = 1/Fs # sampling period
t = 0.1 # seconds of sampling
N = Fs*t # total points in signal

# signal information
freq = np.array([50, 400, 180, 2000, 140, 350]) # in hertz, the desired natural frequency
omega = 2*np.pi*freq # angular frequency for sine waves

t_vec = np.arange(N)*T # time vector for plotting
y = np.zeros((3,len(t_vec)))

amp = [1,2,5]
k = 0
y_sum = 0
for i in omega:
    y[k][:] = amp[k] * np.sin(i*t_vec)
    y_sum += y[k][:] 
    k += 1 

plt.plot(t_vec,y[0])
plt.plot(t_vec,y[1])
plt.plot(t_vec,y[2])
plt.show() 


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
    tol = np.mean(Pxx)
    k = 0
    for i in Pxx:
        k += 1
        if i > tol:
            amp_list.append(Pxx[k-1])
            freq_list.append(f[k-1])

    return f, Pxx, freq_list, amp_list



""" 
#The other way, CAN BE USED FOR COMPARISON
Y_s = np.fft.fft(norm_max)
Pxx2 = np.abs(Y_s/N)
Pxx1 = Pxx2[0:int(N/2)]
Pxx1[1:-1] = 2 * Pxx1[1:-1]
 """
#Compare the values, used when method above is also used
#----------------------------------------------------------------------------
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
f, Pxx, freq_list, amp_list = chaos_to_hertz(norm_max)

print(f"The frequencies are, in requested order, {freq_list}")
print(f"The amplitudes are, in requested order, {amp_list}")

fig,ax = plt.subplots()
plt.plot(f,Pxx, marker='*', ms=15, markerfacecolor='blue')
ax.set_xscale('log')
#ax.set_yscale('log')
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
plt.show()
