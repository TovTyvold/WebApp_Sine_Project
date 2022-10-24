
from ctypes.wintypes import PMSG
import wave
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from plotting import plot_array 



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


#LFO
def Low_frequency_Oscillator_sine(signal, t):
    t_vec = np.linspace(0, t, len(signal))
    return (1 + np.sin(2 * np.pi * 20 * t_vec)) / 2
    

#LFO
def Low_frequency_Oscillator_saw(signal, t):
    t_vec = np.linspace(0, t, len(signal))
    return 2 * 20 * (t_vec % (1 / 20)) - 1


def reverb_filter(y, t_vec, sampleRate, mixPercent, decayFactor, delay, Decay_factors, delay_factors, decayFactor_AP):
    """
    Reverb filter with layers of combs, i.e., layers that increase the delay or attack of wet/dry effect. 

    Needs functions comb_for_reverb and all_pass_reverb to function. 

    Inputs:
    -----------------------------
    y - dtype ndarray: Signal
    delay - dtype float/int: Delay in milliseconds. Determines the length of the delay effect.  --STANDARD FOR NOW
    decayfactor - dtype float: Float that determines the amplification of the delay effect.  --STANDARD FOR NOW
    sapmleRate - dtype int: Number of samples
    mixPercent - dtype float: Percentage of the wet/dry effect. Determines how much of the total should be enhanced. 

    Returns:
    ----------------------------
    allPassFilterSamples2 - dtype ndarray: Source of the signal with a reverbation after the source has 
    stopped. 
    !!!!!!!!!!Requires the time vector after call to be twice as large!!!!!!!!!!!


    Example input:
    ----------------------------
    reverb_filter(y = normalized_y, sampleRate = Fs, mixPercent = 50)
    """
    t_reverb = np.linspace(t_vec[0], t_vec[-1], len(t_vec)*2)
    y_return = np.zeros(len(t_reverb))
    y_return[:int(len(t_reverb)/2)] = y.copy()
    bufferSize = len(y)
    combFilterSamples1 = comb_for_reverb(y, bufferSize, delay, decayFactor, sampleRate)
    combFilterSamples2 = comb_for_reverb(y, bufferSize, (delay + delay_factors[0]), (decayFactor + Decay_factors[0]), sampleRate)
    combFilterSamples3 = comb_for_reverb(y, bufferSize, (delay + delay_factors[1]), (decayFactor + Decay_factors[1]), sampleRate)
    combFilterSamples4 = comb_for_reverb(y, bufferSize, (delay + delay_factors[2]), (decayFactor + Decay_factors[2]), sampleRate)

    outputComb = np.zeros(bufferSize)
    for i in range(bufferSize):
        outputComb[i] = combFilterSamples1[i] + combFilterSamples2[i] + combFilterSamples3[i] + combFilterSamples4[i]

    mixAudio = np.zeros(bufferSize)
    for i in range(bufferSize):
        mixAudio[i] = ((100 - mixPercent) * y[i]) + (mixPercent * outputComb[i])

    allPassFilterSamples1 = all_pass_reverb(mixAudio, bufferSize, sampleRate, decayFactor_AP)
    allPassFilterSamples2 = all_pass_reverb(allPassFilterSamples1, bufferSize, sampleRate, decayFactor_AP)
    y_return[-int(len(t_reverb)/2):] = allPassFilterSamples2
    return allPassFilterSamples2

def comb_for_reverb(samples, sampleLength, delay_in_mm, decayfactor, sampleRate):
    delaySamples = int(np.abs(delay_in_mm) * (sampleRate/1000))
    combFilterSamples = samples 
    for i in range(0, sampleLength-delaySamples):
        combFilterSamples[i+delaySamples] += combFilterSamples[i] * decayfactor
    return combFilterSamples


def all_pass_reverb(samples, sampleLength, sampleRate, decayFactor_AP = 0.131):
    delaySamples = int(89.27* (sampleRate/1000))
    allPassFilterSamples = np.zeros(sampleLength)
    for i in range(sampleLength):
        allPassFilterSamples[i] = samples[i]
        if i - delaySamples >= 0:
            allPassFilterSamples[i] += -decayFactor_AP * allPassFilterSamples[i - delaySamples]
        if i - delaySamples >= 1:
            allPassFilterSamples[i] += decayFactor_AP * allPassFilterSamples[i + 20 - delaySamples]

    value = allPassFilterSamples[0]
    max = 0.0

    for i in range(sampleLength):
        if np.abs(allPassFilterSamples[i]) > max:
            max = np.abs(allPassFilterSamples[i])
        
    for i in range(sampleLength):
        currentValue = allPassFilterSamples[i]
        value = ((value + (currentValue - value))/max)

        allPassFilterSamples[i] = value 
    
    return allPassFilterSamples



def Impulse_Rev(y):
    signal_clean = y # Already normalized, if not -> y / np.max(np.abs(y))
    IR = signal.unit_impulse(len(y), 'mid')
    IR = IR / np.abs(np.max(IR))
    p_max = np.argmax(np.abs(IR))
    signal_rev = signal.fftconvolve(y, IR, mode="same")
    signal_rev = signal_rev / np.max(np.abs(signal_rev))
    signal_rev = IR_shift(signal_clean, -p_max)
    signal_rev = signal_rev[0 : signal_clean.shape[0]]

    return signal_rev

def IR_shift(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n] = 0.0
        e[n:] = xs[:-n]
    else:
        e[n:] = 0.0
        e[:n] = xs[-n:]
    return e


def dirac_comb_discrete(y, N_, K):
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

    n = np.arange(len(y))
    sigSum = 0
    for i in range(N_):
        part = (1/N_) *np.exp(2j * np.pi * n * i / K)
        sigSum = sigSum + part
    return sigSum.real * y


def hilbert(y):
    # Phase shift by pi/2
    return np.imag(signal.hilbert(y))




def Rev_Conv_Filter(signal, Duration_inp, DryWet_ = 1):
    Fs = 44100
    N = Fs 
    T = 1/Fs 
    t = Duration_inp
    length = len(signal)
    DryWet_ = 100
    Duration_inp = 5
    if Duration_inp == 1:
        Duration_inp = 2
    t = Duration_inp
    Duration = Duration_inp
    total_len = int(Duration * length)
    t_vec_r = np.arange(int(N * Duration)) * T * t
    x = float(length/(total_len))
    DryWet = abs((DryWet_/100))
    #First output original sample

    length1 = int(total_len * (x)) 
    length2 = int(total_len * ((Duration_inp-1) * x/3)) + length1
    length3 = int(total_len * ((Duration_inp-1) * x/4)) + length2
    length4 = int(total_len * ((Duration_inp-1) * x/6)) + length3
    length5 = int(total_len * ((Duration_inp-1) * x/6)) + length4
    length6 = int(total_len * ((Duration_inp-1) * x/12)) + length5

    releasek = np.ones_like(t_vec_r)
    releasej = np.ones_like(t_vec_r)
    releasel = np.ones_like(t_vec_r)
    if Duration_inp >= 3:
        releaseg = np.linspace(1,0.75, length2 - length1+1)
        releaseh = np.linspace(1,0.5, length3 - length2+1)
        releasek = np.linspace(1,0.5, length4 - length3)
        releasej = np.linspace(1,0.5, length5 - length4)
        releasel = np.linspace(1,0.5, length6 - length5)

    cych = 2205
    cyc3h = 3 * cych
    cyc5h = 5 * cych
    cyc7h = 7 * cych
    cyc9h = 9 * cych
    norm_y_a = signal.copy()
    norm_y = list(norm_y_a) * int((Duration))

    conv_y = np.zeros_like(t_vec_r)
    #Release constants
    g = 0; h = 0; k = 0; j = 0; l = 0
    for n in range(len(t_vec_r)):
    
        if n >= length1 and n < length2:
            conv_y[n] = releaseg[g] * (norm_y[n]*0.4 - norm_y[n-length1+cych]*0.6 * DryWet)
            g += 1

        elif n >= length2 and n <= length3:
            conv_y[n] = releaseh[h] * (norm_y[n- length2]*0.4 - norm_y[n-length2+cych]*0.4 - norm_y[n- length2+cyc3h]*0.2)
            h += 1 

        elif n >= length3 and n <= length4:
            conv_y[n] = releasek[k] * (norm_y[n-length3]*0.3 - norm_y[n-length3+cych]*0.2\
                - norm_y[n- length3+cyc3h]*0.15 - norm_y[n- length3+cyc5h]*0.1)
            k += 1

        elif n >= length4 and n <= length5:
            conv_y[n] = releasej[j] * (norm_y[n-length4]*0.2 - norm_y[n-length4+cych]*0.2 - norm_y[n- length4+cyc3h]*0.1\
                - norm_y[n- length4+cyc5h]*0.05 - norm_y[n- length4+cyc7h]*0.05)
            j += 1
            
        elif n >= length5 and n < length6:
            dist = n - length5
            conv_y[n] =  releasel[l] * (norm_y[dist]*0.2 - norm_y[dist+cych]*0.01 - norm_y[dist+cyc3h]*0.01\
                - norm_y[dist+cyc5h]*0.01 - norm_y[dist+cyc7h]*0.01 - norm_y[dist+cyc9h]*0.01)
            l += 1

        else:
            
            conv_y[n] = norm_y[n]
    return conv_y, t_vec_r


    
if __name__ == "__main__":
    a = 1
