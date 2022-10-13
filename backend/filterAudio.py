from tkinter import N
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

#LOW PASS
def butter_lowpass_filter(data, cutoff, Fs, order):
    """ nyq = 0.5 * Fs
    normal_cutoff = cutoff / nyq """

    b, a = signal.butter(order, cutoff, btype='low', analog=False, fs = Fs)
    y = signal.filtfilt(b, a, data)


    w, h = signal.freqz(b, a, fs=Fs, worN=8000)

    plt.plot(w, np.abs(h), 'r--')
    plt.plot(cutoff, 0.5*np.sqrt(2), 'bo', label="LowPass")
    plt.axvline(cutoff, color='r', ls="--", lw=0.5)
    plt.xlim([0,800])
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()
    plt.legend()
    return y

def low_pass_Filter(y_sum, Fs, cutoff, order):
    data = y_sum 
    y_filtered_low = butter_lowpass_filter(data, cutoff, Fs, order)
    return y_filtered_low


# HIGH PASS
def butter_highpass_filter(data, cutoff, Fs, order):
    nyq = 0.5 * Fs
    normal_cutoff = cutoff / nyq
    print(normal_cutoff)

    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    y = signal.filtfilt(b, a, data)

    w, h = signal.freqz(b, a, fs=Fs, worN=8000)
    plt.plot(w, np.abs(h), 'r--')
    plt.plot(cutoff, 0.5*(np.sqrt(2)), 'ro', label="HighPass")
    plt.axvline(cutoff, color='r', ls="--", lw=0.5)
    plt.xlim(0, 800)
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()
    plt.legend()
    plt.tight_layout()

    return y

def high_pass_Filter(y_sum, Fs, cutoff, order):
    data = y_sum 
    y_filtered_high = butter_highpass_filter(data, cutoff, Fs, order)
    return y_filtered_high


#LFO
def Low_frequency_Oscillator_sine(freq_infrasonic, t_vec, amp):
    return 1 + amp*np.sin(2 * np.pi * freq_infrasonic * t_vec)
    

#LFO
def Low_frequency_Oscillator_saw(freq_infrasonic, t_vec, amp):
    x = np.zeros(len(t_vec))
    for i in range(1, len(t_vec)):
        ((-1)**i) * np.sin(2 * np.pi * freq_infrasonic * i * t_vec[i])/i
    return 1 + amp *(0.5 - x)

if __name__ == "__main__":
    a = 1
