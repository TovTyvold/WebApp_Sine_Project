
import wave
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from plotting import plot_array 
import time

#LOW PASS

def low_pass_Filter(y_sum, Fs, cutoff, order):
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
    data = y_sum 
    sos = signal.butter(order, cutoff, btype='low', analog=False, output = 'sos', fs = Fs)
    filtered = signal.sosfilt(sos, data)

    return filtered

# HIGH PASS

def high_pass_Filter(y_sum, Fs, cutoff, order):
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
    data = y_sum 
    sos = signal.butter(order, cutoff, btype='high', analog=False, output = 'sos', fs = Fs)
    filtered = signal.sosfilt(sos, data)
    return filtered


#LFO
def Low_frequency_Oscillator_sine(freq_infrasonic, t_vec, amp):
    return 1 + amp*np.sin(2 * np.pi * freq_infrasonic * t_vec)
    

#LFO
def Low_frequency_Oscillator_saw(freq_infrasonic, t_vec, amp):
    return 2 * amp * freq_infrasonic * (t_vec % (1 / freq_infrasonic)) - 1




def reverb_filter(y, sampleRate, mixPercent):
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
    allPassFilterSamples2 - dtype ndarray: Filtered signal


    Example input:
    ----------------------------
    reverb_filter(y = normalized_y, sampleRate = Fs, mixPercent = 50)
    """

    decayFactor = -0.5
    delay = float(20)
    bufferSize = len(y)
    combFilterSamples1 = comb_for_reverb(y, bufferSize, delay, decayFactor, sampleRate)
    combFilterSamples2 = comb_for_reverb(y, bufferSize, (delay - 11), (decayFactor + 0.1313), sampleRate)
    combFilterSamples3 = comb_for_reverb(y, bufferSize, (delay + 19), (decayFactor - 0.2743), sampleRate)
    combFilterSamples4 = comb_for_reverb(y, bufferSize, (delay - 8), (decayFactor - 0.31), sampleRate)

    outputComb = np.zeros(bufferSize)
    for i in range(bufferSize):
        outputComb[i] = combFilterSamples1[i] + combFilterSamples2[i] + combFilterSamples3[i] + combFilterSamples4[i]

    mixAudio = np.zeros(bufferSize)
    for i in range(bufferSize):
        mixAudio[i] = ((100- mixPercent) * y[i]) + (mixPercent * outputComb[i])

    allPassFilterSamples1 = all_pass_reverb(mixAudio, bufferSize, sampleRate)
    allPassFilterSamples2 = all_pass_reverb(allPassFilterSamples1, bufferSize, sampleRate)

    return allPassFilterSamples2

def comb_for_reverb(samples, sampleLength, delay_in_mm, decayfactor, sampleRate):
    delaySamples = int(delay_in_mm * (sampleRate/1000))
    combFilterSamples = samples
    for i in range(0, sampleLength-delaySamples):
        combFilterSamples[i+delaySamples] += combFilterSamples[i] * decayfactor

    return combFilterSamples


def all_pass_reverb(samples, sampleLength, sampleRate):
    delaySamples = int(89.27 * (sampleRate/1000))
    allPassFilterSamples = np.zeros(sampleLength)
    decayFactor = 0.131

    for i in range(sampleLength):
        allPassFilterSamples[i] = samples[i]
        if i - delaySamples >= 0:
            allPassFilterSamples[i] += -decayFactor * allPassFilterSamples[i - delaySamples]
        elif i - delaySamples >= 1:
            allPassFilterSamples[i] += decayFactor * allPassFilterSamples[i + 20 - delaySamples]

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


if __name__ == "__main__":
    a = 1
