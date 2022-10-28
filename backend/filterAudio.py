
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
def Low_frequency_Oscillator_sine(input, t):
    t_vec = np.linspace(0, t, len(input))
    return (1 + np.sin(2 * np.pi * 20 * t_vec)) / 2
    

#LFO
def Low_frequency_Oscillator_saw(input, t):
    t_vec = np.linspace(0, t, len(input))
    return 2 * 20 * (t_vec % (1 / 20)) - 1

def weierstrassFunc(input, a):
    t_vec = np.linspace(-2 * np.pi, 2 * np.pi, len(input))
    a = 0.5
    tol = 0.1
    b = 1/a + (3 / (2 * a)) * np.pi + tol
    
    weier = np.zeros_like(input)
    for i in range(100):
        weier  += a **i * np.cos((b**(i) * np.pi * t_vec))
    return weier


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
    # Phase shift by pi/2
    return np.imag(signal.hilbert(y))


def Rev_Conv_Filter(input, Duration_inp, DryWet_):
    Fs = 44100
    N = Fs 
    T = 1/Fs 
    t = Duration_inp
    length = len(input)
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
    norm_y_a = input.copy()
    norm_y = list(norm_y_a) * int((Duration))

    conv_y = np.zeros_like(t_vec_r)

    # Determine the Dry/Wet factor with the reverb 
    if DryWet == 0.0:
        D1 = 1; D2 = 1; D3 = 1; D4 = 1; D5 = 1

    elif DryWet == 1:
        a = 1
        D1 = 1 - 0.9 * DryWet*a; D2 = 1 - 0.8 * DryWet*a; D3 = 1 - 0.7 * DryWet*a
        D4 = 1 - 0.7 * DryWet*a; D5 = 1 - 0.6 * DryWet*a


    elif 0.75 <= DryWet < 1:
        a = 1.2 + (1 - DryWet)*2.75
        D1 = 1 - 0.9 * DryWet*a; D2 = 1 - 0.8 * DryWet*a; D3 = 1 - 0.7 * DryWet*a
        D4 = 1 - 0.7 * DryWet*a; D5 = 1 - 0.6 * DryWet*a

    elif 0.5 <= DryWet < 0.75:
        a = 2 + (1 - DryWet - 0.3) * 3.5
        D1 = 1 - 0.9 * DryWet*a; D2 = 1 - 0.8 * DryWet*a; D3 = 1 - 0.7 * DryWet*a
        D4 = 1 - 0.7 * DryWet*a; D5 = 1 - 0.6 * DryWet*a


    elif 0.25 <= DryWet < 0.5:
        b = 8 - abs(1 - DryWet*4)*8
        D1 = 1 - 0.9 * DryWet*b; D2 = 1 - 0.8 * DryWet*b; D3 = 1 - 0.7 * DryWet*b
        D4 = 1 - 0.7 * DryWet*b; D5 = 1 - 0.6 * DryWet*b

    elif 0 < DryWet < 0.25:
        b = 0.1
        D1 = 1 - 0.9 * DryWet*b; D2 = 1 - 0.8 * DryWet*b; D3 = 1 - 0.7 * DryWet*b
        D4 = 1 - 0.7 * DryWet*b; D5 = 1 - 0.6 * DryWet*b
    #Release constants
    g = 0; h = 0; k = 0; j = 0; l = 0


    #Release constants
    g = 0; h = 0; k = 0; j = 0; l = 0
    for n in range(len(t_vec_r)):
    
        if n >= length1 and n < length2:
            conv_y[n] = releaseg[g] * (norm_y[n] * D1 - norm_y[n-length1+cych]*0.9 * DryWet)
            g += 1

        elif n >= length2 and n <= length3:
            conv_y[n] = releaseh[h] * (norm_y[n- length2] * D2 - norm_y[n-length2+cych]*0.3 * DryWet - norm_y[n- length2+cyc3h]*0.3  * DryWet\
                - norm_y[n- length2+cyc5h]*0.1 * DryWet - norm_y[n- length2+cyc7h]*0.15 * DryWet)
            h += 1 

        elif n >= length3 and n <= length4:
            conv_y[n] = releasek[k] * (norm_y[n-length3] * D3 - norm_y[n-length3+cych]*0.3 * DryWet\
                - norm_y[n- length3+cyc3h]*0.2 * DryWet - norm_y[n- length3+cyc5h]*0.1 * DryWet - norm_y[n- length3+cyc7h]*0.1 * DryWet)
            k += 1

        elif n >= length4 and n <= length5:
            conv_y[n] = releasej[j] * (norm_y[n-length4] * D4 - norm_y[n-length4+cych]*0.2 * DryWet - norm_y[n- length4+cyc3h]*0.2 * DryWet\
                - norm_y[n- length4+cyc5h]*0.1 * DryWet - norm_y[n - length4+cyc7h]*0.05 * DryWet - norm_y[n - length4+cyc9h]*0.05 * DryWet)
            j += 1
            
        elif n >= length5 and n < length6:
            dist = n - length5
            conv_y[n] =  releasel[l] * (norm_y[dist] * D5 - norm_y[dist+cych]*0.2 * DryWet - norm_y[dist+cyc3h]*0.15 * DryWet\
                - norm_y[dist+cyc5h]*0.05 * DryWet - norm_y[dist+cyc7h]*0.05 * DryWet - norm_y[dist+cyc9h]*0.05 * DryWet)
            l += 1

        else:
        
            conv_y[n] = norm_y[n]
    return conv_y


def semitoneFunc(input, n, shift_):
    """
    Currently can only take in a single frequency.
    """
    Fs = 44100
    tol = 0.01
    minSigLen = Fs / tol

    # Add 1 if minSigLen is a odd number
    if np.mod(minSigLen,2) !=0 :
        minSigLen = minSigLen + 1

    #length = len(input)
    #new_f = f * np.exp(n/12)
    freq_shift = shift_/10

    if len(input) < minSigLen:
        input = list(input) + list(np.zeros(int(minSigLen - len(input))))

    df = Fs/len(input) 
    n_samp_shift = int(freq_shift / df)

    Y_k = np.fft.fft(input)

    mag = np.abs(Y_k) 
    phase = np.unwrap(np.angle(Y_k), np.pi)

    # Shift the frequency
    shift = n_samp_shift
    N_ = len(Y_k)

    # First half
    mag1 = mag[1:int(N_/2)]
    phase1 = phase[1:int(N_/2)]

    # Second half
    mag2 = mag[int(N_/(2)):]
    phase2 = phase[int(N_/(2)):]

    # Lets pad the arrays to the right
    mag1s = list(np.zeros(shift)) + list(mag1[:-shift])
    phase1s = list(np.zeros(shift)) + list(phase1[:-shift])

    # Then pad the arrays to the left
    mag2s = list(mag2[shift:]) + list(np.zeros(shift))
    phase2s = list(phase2[shift:]) + list(np.zeros(shift))
    # And concatenate
    magS = []
    magS.append(mag[0])
    magS = magS + list(mag1s) + list(mag2s)

    phaseS = []
    phaseS.append(phase[0])
    phaseS = phaseS + list(phase1s) + list(phase2s)

    x = magS*np.cos(phaseS)               # change from polar to rectangular
    y = magS*np.sin(phaseS)
    new_fft2 = x + 1j*y                     #store signal as complex numbers
    new_ifft2 = np.real(np.fft.ifft(new_fft2))
    return new_ifft2


def singleShift(input, shift_):
    """
    singleShit can be used to change a single frequency of the signal.   

    Inputs:
    -----------------------------
    input - dtype ndarray: Signal
    shift_ - dtype float/int: The addition or subtraction on the previous frequnecy, depending on the
    sign of the value.

    Returns:
    ----------------------------
    sigShifted - dtype ndarray: Array with a changed frequency


    Example input for parameters:
    ----------------------------
    input = signal
    shift_ = 40
    """
    t = np.linspace(0,1,len(input))
    Fshift = shift_/10
    sigHil = signal.hilbert(input)
    sigHilShifted = sigHil * np.exp(1j * 2 * np.pi * Fshift * t)
    sigShifted = np.real(sigHilShifted)
    return sigShifted

if __name__ == "__main__":
    abcd = 1
