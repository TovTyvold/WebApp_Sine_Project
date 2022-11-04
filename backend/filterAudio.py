from scipy import signal
import numpy as np
from coloredNoise import white_noise, brownian_noise, pink_noise, blue_noise, violet_noise
from pedalboard import Pedalboard, Reverb


#LOW PASS
def low_pass_Filter(y_sum, cutoff):
    """
    LPF that attentuates all frequencies above the cutoff.

    Inputs 
    -----------------------------
    y_sum - dtype ndarray: Signal
    Fs - dtype int: Sample rate
    cutoff - dtype float/int: Frequency for filter processing
    order - dtype int: Order of the bisection series, higher is better, but can cause overflow. Ex: order = np.max(frequency)/2

    Returns
    ----------------------------
    filtered - dtype ndarray: Fitlered signal
    """
    order = 5
    Fs = 44100
    data = y_sum 
    sos = signal.butter(order, cutoff, btype='low', analog=False, output = 'sos', fs = Fs)
    filtered = signal.sosfilt(sos, data)
    return filtered


# HIGH PASS
def high_pass_Filter(y_sum, cutoff):
    """
    HPF that attentuates all frequencies below the cutoff.

    Inputs 
    -----------------------------
    y_sum - dtype ndarray: Signal
    Fs - dtype int: Sample rate
    cutoff - dtype float/int: Frequency for filter processing
    order - dtype int: Order of the bisection series. Higher is better, but can cause overflow. Ex: order = np.max(frequency)/2

    Returns
    ----------------------------
    filtered - dtype ndarray: Fitlered signal
    """
    order = 5
    Fs = 44100
    data = y_sum 
    sos = signal.butter(order, cutoff, btype='high', analog=False, output = 'sos', fs = Fs)
    filtered = signal.sosfilt(sos, data)
    return filtered


def Low_frequency_Oscillator_sine(input, t):
    """
    Layer input with the sine function, adds a sinusoidal effect.

    Inputs 
    -----------------------------
    input - dtype ndarray: Signal
    t - dtype float: Scalar variable that is the time domain.

    Returns
    ----------------------------
     dtype [ndarray]: Fitlered signal
    """
    t_vec = np.linspace(0, t, len(input))
    return (1 + np.sin(2 * np.pi * 20 * t_vec)) / 2
    

def Low_frequency_Oscillator_saw(input, t):
    """
    Layer input with the saw function, adds a Sawtooth effect.

    Inputs 
    -----------------------------
    input - dtype ndarray: Signal
    t - dtype float: Scalar variable that is the time domain.

    Returns
    ----------------------------
     dtype [ndarray]: Fitlered signal
    """
    t_vec = np.linspace(0, t, len(input))
    return 2 * 20 * (t_vec % (1 / 20)) - 1

def dirac_comb_discrete(y, N_, K_):
    """
    Dirac Delta Comb filter that adds a flanger effect to signal.  

    Inputs:
    -----------------------------
    y - dtype ndarray: Signal
    N_ - dtype int: Determines how well-defined the spikes in the comb should be. A low N_ = 3 gives a more depth to the sound
    and a high N_3 = 15 gives a more abrupt sound.
    K - dtype int: How often the spikes should appear in the sample length, i.e., a peak every K sample.  

    Returns:
    ----------------------------
    sigSum.real * y - dtype ndarray: Filtered signal with only the real part of sigSum


    Example input:
    ----------------------------
    dirac_comb_filt = dirac_comb_discrete(y_sum, N_ = 2, K = len(y[0])/5)
    """
    K = len(y)/K_
    n = np.arange(len(y))
    sigSum = 0
    for i in range(N_):
        part = (1/N_) *np.exp(2j * np.pi * n * i / K)
        sigSum = sigSum + part
    output = sigSum.real * y
    return output 

def hilbert(y):
    """
    Imposes the transfer function Hilbert, produses a pi/2 phase-shift.

    Inputs 
    -----------------------------
    y - dtype ndarray: Signal

    Returns
    ----------------------------
     dtype [ndarray]: Fitlered signal
    """
    return np.imag(signal.hilbert(y))


def vibratoFunc(input, Modfreq, width, W):
    """
    vibratoFunc can be used to implement an vibrato effect. The parameter "width" should be around:
    ------------ 0.001 < width < 0.003. 

    Inputs:
    -----------------------------
    input - dtype ndarray: Signal
    Modfreq - dtype float/int: The frequency the sinusoidal wave that creates vibrato. 
        0.1 < Modfreq < 5
    width - dtype float/int: Length of each vibrato-effect. 
        0.0003 < width < 0.003
    W - dtype float/int: Speed of the increase/decrease in frequency. 
        Can take any W > 0. 
        For 0 < W < 1 we have decreasing frequency
        For 1 < W we have increasing frequency.
        For W = 1 or W = 0 we have a plain vibrato.
    Returns:
    ----------------------------
    x - dtype ndarray: Array with input filtered


    EXAMPLE input for parameters:
    ----------------------------
    input = signal; Modfreq = 1.5; width = 0.003; W = 4
    """

    Fs = 44100
    Delay = width 

    # WIDTH can't be greater than DELAY.
    DELAY = int(Delay * Fs)
    WIDTH = int(width * Fs)
 
    length = len(input)
    if W == 0 or W == 1:
        MODFREQ = Modfreq/Fs + np.zeros(length)
    else:
        if  0 < W  < 1:
            MODFREQ = np.linspace(Modfreq, Modfreq * W, length) / Fs 
        elif W > 1:
            MODFREQ = np.linspace(Modfreq/(W), Modfreq, length) / Fs
    L = 1 + DELAY + WIDTH*2
    
    Delayline = np.zeros(L)
    x = np.zeros_like(input)
    for n in range(length):
        DelaylineS = []
        M = MODFREQ

        MOD = np.sin(M[n] * 2 * np.pi * n)
        TAP = 1 + DELAY + WIDTH * MOD 
        i = int(np.floor(TAP))
        frac = TAP - i 
        DelaylineS.append(input[n])
        Delayline = list(DelaylineS) +  list(Delayline[:L-1])
         
        # Linear Interpolation 
        x[n] = Delayline[i+1] * frac + Delayline[i] * (1-frac)
    return x

def singleShift(input, shift_):
    """
    singleShit can be used to change a single frequency of the signal.   

    Inputs:
    -----------------------------
    input - dtype ndarray: Signal
    shift_ - dtype float/int: The addition or subtraction on the current frequnecy.

    Returns:
    ----------------------------
    sigShifted - dtype ndarray: Array with a changed frequency


    Example input for parameters:
    ----------------------------
    input = signal
    shift_ = 40
    """
    t = np.linspace(0, 1, len(input))
    Fshift = shift_/100
    sigHil = signal.hilbert(input)
    sigHilShifted = sigHil * np.exp(1j * 2 * np.pi * Fshift * t)
    sigShifted = np.real(sigHilShifted)
    return sigShifted

def Reverb_(input, room_size = 1, wet_level = 0.5, dry_level = 0.4, width = 0.25):
    """
    Reverb_ is a module taken from the class padelboard. Can be used to generate a reverb effect.

    Inputs:
    -----------------------------
    input - dtype ndarray: Signal
    room_size - dtype float: The attack of the reverb.
    wet_level - dtype float: 
    dry_level - dtype float:
    width - dtype float: 

    Returns:
    ----------------------------
    dtype ndarray: Filtered signal, 1-d array

    Example input for parameters:
    ----------------------------
    input = signal
    room_size = 0.5
    wet_level = 0.33
    dry_level = 0.4
    width = 0.25
    """
    sample_rate = 44100
    board = Pedalboard([Reverb(room_size, wet_level, dry_level, width)])
    return board(input.copy(), sample_rate)




if __name__ == "__main__":
    abcd = 1
