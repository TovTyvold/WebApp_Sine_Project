from scipy import signal
#
# 
# 
# 
""" 
from pointsCalculation import getPoints, parseDict
periodicFunc_list = [parseDict({"shape" : "sin","frequency" : 440,"amplitude": 1})]
sampleRate = 44100
y_sum_brage = getPoints(periodicFunc_list, 44100) 
"""


def butter_lowpass_filter(data, cutoff, Fs, order):
    b, a = signal.butter(order, cutoff, btype='low', analog=False, fs=Fs)
    y = signal.lfilter(b, a, data)
    return y

def low_pass_Filter(y_sum, Fs, cutoff, order):
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

