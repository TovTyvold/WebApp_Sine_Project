import numpy as np
from pyparsing import line 
from scipy import signal
import matplotlib.pyplot as plt
from pointsFrequency import signal_to_hertz
from pointsCreateSignal import Create_Signal
plt.style.use('ggplot')


# t, system, y_sum, Fs = Create_Signal([],[],[])
""" plt.plot(t,system)
plt.show() """

def butter_lowpass(cutoff, Fs, order):
        return signal.butter(order, cutoff, btype='low', analog=False, fs=Fs)
def butter_lowpass_filter(data, cutoff, Fs, order):
    b, a = butter_lowpass(cutoff, Fs, order = order)
    y = signal.lfilter(b, a, data)
    return y

def low_pass_Filter(t, y_sum, Fs):

    cutoff_lower = 15
    order = 5
    b, a = butter_lowpass(cutoff_lower, Fs, order)
    w, h = signal.freqz(b, a, worN=8000, fs=Fs)
    noise = 1.5*np.cos(9*2*np.pi*t)
    data = y_sum + noise
    y_filtered = butter_lowpass_filter(data, cutoff_lower, Fs, order)

    """ plt.subplot(2, 1, 1)
    plt.plot(w, np.abs(h), 'b')
    plt.plot(cutoff_lower, 0.5*np.sqrt(2), 'ko')
    plt.axvline(cutoff_lower, color='k')
    plt.xlim(0, 0.5*Fs)
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(t, data, 'b-', label='data', linewidth = 2)
    plt.plot(t, y_filtered, 'r--', linewidth=2, label='filtered data')
    plt.xlabel('Time [sec]')
    plt.grid()
    plt.legend()

    plt.subplots_adjust(hspace=0.35)
    plt.savefig(f"filter_{cutoff_lower}.png")
    plt.show() """
    return y_filtered

