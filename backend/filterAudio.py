
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from plotting import plot_array 

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
    


# Add type of impulse response as "type" variable
def reverb_filter(y, mode, amp):

    n = int(len(y))
    #descend = 1 / step**2
    #sig = np.repeat([0, -5, 0, -5, 0], n/5)
    #sig = np.repeat([0., , 0.], int(n/3))

    win = signal.windows.hann(n, sym=True)

    filtered = signal.convolve(y, win,  mode, method='direct')
    #
    return filtered, n, win



def reverb_filter2(y, delay, decayFactor, sampleRate, mixPercent):
    bufferSize = len(y)
    combFilterSamples1 = comb_for_reverb(y, bufferSize, delay, decayFactor, sampleRate)
    combFilterSamples2 = comb_for_reverb(y, bufferSize, (delay - 11.73), (decayFactor - 0.1313), sampleRate)
    combFilterSamples3 = comb_for_reverb(y, bufferSize, (delay + 19.31), (decayFactor - 0.2743), sampleRate)
    combFilterSamples4 = comb_for_reverb(y, bufferSize, (delay - 7.97), (decayFactor - 0.31), sampleRate)

    outputComb = np.zeros(bufferSize)

    for i in range(bufferSize):
        outputComb[i] = combFilterSamples1[i] + combFilterSamples2[i] + combFilterSamples3[i] + combFilterSamples4[i]


    mixAudio = np.zeros(bufferSize)

    for i in range(bufferSize):
        mixAudio[i] = ((100- mixPercent) * y[i]) + (mixPercent * outputComb[i])


    allPassFilterSamples1 = all_pass_reverb(y, bufferSize, sampleRate)

    # Final array
    allPassFilterSamples2 = all_pass_reverb(allPassFilterSamples1, bufferSize, sampleRate)

    return allPassFilterSamples2

def comb_for_reverb(samples, sampleLength, delay_in_mm, defacyFactor, sampleRate):

    delaySamples = int(delay_in_mm * (sampleRate/1000))

    combFilterSamples = samples

    for i in range(0, sampleLength-delaySamples):
        combFilterSamples[i+delaySamples] += combFilterSamples[i] * defacyFactor

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


def delay(y, delay_len, sampleRate):
    N = len(y)
    k = int(delay_len*sampleRate)
    #Delay gain
    b = 0.5 

    x = np.zeros(N + k)

    
    for n in range(0, N + k):
        if n > k and n - k < N:
            xd =  b * y[n-k]
        else:
            xd = [0]

        if n < N:
            xn = y[n]

        else:
            xn = [0]

        x[n] = xn + xd 
    return x, len(x)


def Delay_Comb(y, delay_gain, delay_amount, sampleRate):
    return np.sqrt(1 + 2 * delay_gain * np.cos(2 * np.pi * y * delay_amount / sampleRate) + delay_gain **2)



if __name__ == "__main__":
    a = 1
