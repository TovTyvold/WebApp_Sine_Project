from scipy import signal
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
from pointsFrequency import signal_to_hertz
from plotting import plot_array 
from pointsNoise import cNoise
from coloredNoise import white_noise, brownian_noise, pink_noise, blue_noise, violet_noise



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
    

#LFO
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

def weierstrassFunc(input, a):
    """
    Layer input with the Weierstrass function, adds a metallic effect.

    Inputs 
    -----------------------------
    input - dtype ndarray: Signal
    a - dtype float: Scalar variable, must be 0 < a < 1. Sets the 
    precision of the weier function

    Returns
    ----------------------------
    weier - dtype ndarray: Fitlered signal
    """

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

# To do: Be able to pitch signals that have semirandom frequencies
def semitoneFunc(input, shift_):
    """
    Currently can only take in a single frequency.
    Parameter "n" for semitones is yet to be implemented.
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
    shift_ - dtype float/int: The addition or subtraction on the current frequnecy.

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



def whiteChorus(input, width):
    """
    vibratoFunc can be used to implement an vibrato effect. The parameter "width" should be around:
    ------------ 0.001 < width < 0.003. 

    Inputs:
    -----------------------------
    input - dtype ndarray: Signal
    Modfreq - dtype float/int: The frequency the sinusoidal wave that creates vibrato should have
    width - dtype float/int: Length of the delay signal. 
    W - dtype float/int: Speed of the increase in frequency. High W results in a larger low-frequency variance domain.
    Returns:
    ----------------------------
    x - dtype ndarray: Array with input filtered


    Example input for parameters:
    ----------------------------
    input = signal; width = 0.003; 
    """
    # Get lowpass noise
    
    lp_noise = brownian_noise(len(input))
    lowpass_noise = low_pass_Filter(lp_noise, 1)
    Fs = 44100
    Delay = width 

    # WIDTH can't be greater than DELAY.
    DELAY = int(Delay * Fs)
    WIDTH = int(width * Fs)
 
    length = len(input)
    MODFREQ = lowpass_noise / Fs
    L = 1 + DELAY + WIDTH*2
    print(MODFREQ)
    BL = 0.7
    FF = 1
    FB = -0.7
    x = np.zeros_like(input)
    Delayline = np.zeros(L)
    for n in range(length):
        
        DelaylineS = []
        # Time delay
        MOD = MODFREQ[n]
        TAP = 1 + DELAY + WIDTH * MOD 
        i = int(np.floor(TAP))
        frac = TAP - i 
        # Time index-delay -> K
        K = MOD + frac
        # System of equations
        # -------------------
        # Delay Line and
        # All-Pass Comb -> Chorus equation 
        DelaylineS_ = input[n] + FB * input[int(n-K)]
        DelaylineS.append(DelaylineS_)
        Delayline = list(DelaylineS) + list(Delayline[:L-1])
        x[n] =  BL * Delayline[i] + FF * (DelaylineS_) + input[n]


    # Normalize:
    g = BL + FF + FB
    x = (x * g)/ np.max(np.abs(x))
    return x


def reverberatorFunc_unused(input, DryWet):
    Fs = 44100
    output = np.zeros_like(input)
    DelayLine = np.zeros(int(Fs/20))

    A_delay = 40 
    DryWet = 0.7 

    for i in range(1,len(input)):
        tmp = DelayLine[A_delay] + input[i] * (-DryWet)
        DelayLine = list(tmp * DryWet + input[i]) + list(DelayLine[len(DelayLine)-1])
        output[i] = tmp

    return output

#z^-[M(n) + frac(n)] ---->>> x[M(n) + frac(n)]

if __name__ == "__main__":
    abcd = 1
