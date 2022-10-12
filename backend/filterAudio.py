from scipy import signal
import numpy as np

def butter_lowpass_filter(data, cutoff, Fs, order):
    b, a = signal.butter(order, cutoff, btype='low', analog=False, fs=Fs)
    y = signal.lfilter(b, a, data)
    return y

def low_pass_Filter(t, y_sum, Fs, cutoff):
    order = 5
    data = y_sum 
    y_filtered_low = butter_lowpass_filter(data, cutoff, Fs, order)
    # Call for low-pass
    # y_filtered_low = low_pass_Filter(y_sum_brage[1], Fs, 0.7*periodicFunc_list[0].frequency, 10)
    return y_filtered_low



def butter_highpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    y = signal.filtfilt(b, a, data)
    return y

def high_pass_Filter(y_sum, Fs, cutoff, order):
    data = y_sum 
    y_filtered_high = butter_highpass_filter(data, cutoff, Fs, order)
    # Call for high-pass
    # y_filtered_high = high_pass_Filter(y_sum_brage[1], Fs, 0.3*periodicFunc_list[0].frequency, 10)
    return y_filtered_high


def Low_frequency_Oscillator(freq_infra, t_vec, amp):
    LFO = 1 + amp*np.sin(2 * np.pi * freq_infra * t_vec)
    return LFO

