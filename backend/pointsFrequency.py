import numpy as np


def signal_to_hertz(normalized_signal, Fs):
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

    freq_list = []

    for k in range(1,len(Pxx)-1):
        if Pxx[k-1] < Pxx[k] and Pxx[k] > Pxx[k+1]:
            freq_list.append(f[k])

    


    return freq_list

