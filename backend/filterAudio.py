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
    ------------ 0.001 < width < 0.03. 

    Inputs:
    -----------------------------
    input - dtype ndarray: Signal
    Modfreq - dtype float/int: The frequency the sinusoidal wave that creates vibrato should have
    width - dtype float/int: Length of the delay signal. 
 
    Returns:
    ----------------------------
    x - dtype ndarray: Array with input filtered


    Example input for parameters:
    ----------------------------
    input = signal; width = 0.003; 
    """
    # Get lowpass noise
    
    lowpass_noise = pink_noise(len(input))
    lowpass_noise = lowpass_noise / np.max(lowpass_noise)
    #lowpass_noise = low_pass_Filter(lowpass_noise,10)
    Fs = 44100
    Delay = width 

    # WIDTH can't be greater than DELAY.
    DELAY = int(Delay * Fs)
    WIDTH = int(width * Fs)
 
    length = len(input)
    MODFREQ = lowpass_noise
    L = 1 + DELAY + WIDTH*2
    L = L*2

    x = np.zeros_like(input)
    Delayline = np.zeros(L)

    FB = -0.7; BL = 0.7; FF = 1
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
    
    """ for n in range(length):
        DelaylineS = []
        # Time delay
        MOD = MODFREQ[n]
        TAP = 1 + DELAY + WIDTH * MOD 
        i = int(TAP)
        frac = TAP - i 
        # Time index-delay -> K
        # System of equations
        # -------------------
        # Delay Line and
        # Spline Comb -> Chorus equation
        g1 = (frac**(3))/6
        g2 = ((1+frac)**3 - 4*(frac)**3)/6
        g3 = ((2-frac)**3 - 4*(1 - frac)**3)/6
        g4 = ((1 - frac)**(3))/6

        DelaylineS.append(input[n]) 
        Delayline = list(DelaylineS) + list(Delayline[:L-1])

        x[n] = Delayline[i+1] * g1 + Delayline[i] * g2 \
            + Delayline[i-1] * g3 + Delayline[i-2] * g4 
     """
    # Normalize:
    g = FF + BL + FB
    #g = g1 + g2 + g3 + g4 
    x = (x) / np.max(np.abs(x))
    return x


def pitchChorus(input):
    """
    Ongoing
    """
    y1 = singleShift(input, 0.1)
    y2 = singleShift(input, 0.4)
    y3 = singleShift(input, -0.1)
    y4 = singleShift(input, -0.4)
    chor = input + y1 + y2 + y3 + y4
    return chor
#z^-[M(n) + frac(n)] ---->>> x[M(n) + frac(n)]

if __name__ == "__main__":
    abcd = 1
