import numpy as np
import sys
import matplotlib.pyplot as plt
from plotting import plot_array 


def signal_to_hertz(normalized_signal, Fs, freqs, label):
    """  
        Function that outputs frequencies after taking in a signal
         with/without noise using fft. 

        Input
        ---------
        normalized_signal - dtype ndarray: An ndarray with (x,y) values 
        Fs - dtype int: The sample rate

        Returns
        --------
        freq_list - dtype ndarray: List of frequencies taken from the signal

    """
    length = len(normalized_signal)
    Y_k = np.fft.fft(normalized_signal)[0:int(length/2)]/length # FFT function from numpy
    Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
    Pxx = np.abs(Y_k) # be sure to get rid of imaginary part

    
    f = Fs*np.arange((length/2))/length; # frequency vector


    plt.figure()
    plot_array(f, Pxx,  "FFT plot", "frequency [Hz]", "Power [V]", f"Periodogram of {label} cutoff", "r", "-", "True", "FFT.pdf")
    plt.xlim([0,freqs[-1]+100 ])
    #plt.savefig(f"backend/figures/demo/Periodogram.png")

    # Test Frequencies
    """ 
    freq_list = []

    for k in range(1,len(Pxx)-1):
        if Pxx[k-1] < Pxx[k] and Pxx[k] > Pxx[k+1]:
            freq_list.append(f[k])

    
    print("Checking frequencies...")
    sorted_rand_freq = np.sort(freqs)
    #np. set_printoptions(threshold=np. inf)
    tol = 1
    for k in range(len(freqs)):
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




    print("-----------------------------")
    np.set_printoptions(threshold=sys.maxsize)
    print(f"Number of elements in freq_list: {np.shape(freq_list)[0]:.3f}")
    print(freq_list)
    print(f"Number of elements in list_rand_freq: {np.shape(freqs)[1]:.3f}")
    print(np.sort(freqs)) 
    """

    return f, Pxx#, freq_list

if __name__ == "__main__":
    a = 2
