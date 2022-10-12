from scipy import signal
import numpy as np

#LOW PASS
def butter_lowpass_filter(data, cutoff, Fs, order):
    """ nyq = 0.5 * Fs
    normal_cutoff = cutoff / nyq """

    b, a = signal.butter(order, cutoff, btype='low', analog=False, fs=Fs)
    y = signal.lfilter(b, a, data)
    return y

def low_pass_Filter(y_sum, Fs, cutoff, order):
    data = y_sum 
    y_filtered_low = butter_lowpass_filter(data, cutoff, Fs, order)
    return y_filtered_low


# HIGH PASS
def butter_highpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq

    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    y = signal.filtfilt(b, a, data)
    return y

def high_pass_Filter(y_sum, Fs, cutoff, order):
    data = y_sum 
    y_filtered_high = butter_highpass_filter(data, cutoff, Fs, order)
    return y_filtered_high


#LFO
def Low_frequency_Oscillator(freq_infra, t_vec, amp):
    LFO = 1 + amp*np.sin(2 * np.pi * freq_infra * t_vec)
    return LFO

