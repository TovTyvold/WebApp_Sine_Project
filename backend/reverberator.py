import numpy as np 
import scipy.signal as signal
import matplotlib.pyplot as plt 

"""
Module for applying reverb to the input signal 

Main function is main_reverb, which computes the delay line, calls both comb and all-pass and goes through the algo.  

To produce a reverb effect, call main_reverb with the signal as input.

Wet/dry parameter is to be added.
"""
def allPass(input, delay, gain):
    B = np.zeros(delay) 
    B[0] = gain 
    B[delay-1] = 1 
    A = np.zeros(delay)
    A[0] = 1 
    A[delay-1] = gain 

    output = np.zeros_like(input)
    output = signal.lfilter(B,A, input)
    return output

def comb(input, delay, gain):
    B = np.zeros(delay)
    B[delay - 1] = 1 
    A = np.zeros(delay)
    A[0]  = 1 
    A[delay - 1] = -gain 
    output = np.zeros_like(input)
    output = signal.lfilter(B , A, input)
    return output

def comb_with_lp(input, delay, g, g1):
    g2 = g*(1-g1)
    B = np.zeros(delay+1)
    B[delay-1] = 1
    B[delay] = -g1
    A = np.zeros(delay)
    A[0] = 1
    A[1] = -g1
    A[delay-1] = -g2
    output = np.zeros_like(input)
    output = signal.lfilter(B, A, input)
    return output

def delay(input, delay, gain = 1):
    output = np.concatenate((np.zeros(delay), input))
    output = output * gain 
    return output


def main_reverb(input):
    delays = [2205, 2469, 2690, 2998, 3175, 3439]
    delays_early = [877, 1561, 1715, 1825, 3082, 3510]
    gains_early = [1.02, 0.818, 0.635, 0.719, 0.267, 0.242]
    g1_list = [0.41, 0.43, 0.45, 0.47, 0.48, 0.50]
    g = 0.7
    rev_to_er_delay = 1800 
    allpass_delay = 286 
    allpass_g = 0.7 

    output_gain = 0.075 
    dry = 1
    wet = 1
    width = 1
    wet1 = wet * (width / 2 + 0.5)
    wet2 = wet * ((1 - width) / 2)

    early_reflections = np.zeros_like(input)
    combs_out = np.zeros_like(input)

    # Algo 
    for i in range(6):
        early_reflections = early_reflections + delay(input, delays_early[i], gains_early[i])[:len(input)]

    for j in range(6):
        combs_out = combs_out + comb_with_lp(input, delays[j], g, g1_list[j])

    reverb = allPass(combs_out, allpass_delay, allpass_g)
    early_reflections = np.concatenate((early_reflections, np.zeros(rev_to_er_delay)))
    reverb = delay(reverb, rev_to_er_delay)
    reverb_out = early_reflections + reverb 
    reverb_out = output_gain * ((reverb_out * wet1 + reverb_out * wet2) + np.concatenate((input, np.zeros(rev_to_er_delay))) * dry)

    return reverb_out


if __name__ == "__main__":
    """ Fs = 44100
    T = 1/(Fs) 
    N = Fs
    frequencies = [50]
    n_signals = len(frequencies)
    amplitudes = [1]
    t = 2
    Amp_array = 1
    N = Fs 
    t_vec = np.arange(t * N)*(T*t) 
    y = np.zeros((n_signals,len(t_vec)))
    k = 0
    y_sum = 0
    omega = 2 * np.pi
    sine_add = np.sin(np.linspace(-8 * np.pi,8 * np.pi,len(t_vec)))
    omega = 2 * np.pi* sine_add
    
    for i in range(n_signals):
        y[k] = (Amp_array * amplitudes[k]) * np.sin(omega* frequencies[i] * t_vec)
        y_sum += y[k] 
        k += 1  
    input = y_sum 
    
    rev_out = main_reverb(input)

    from soundGen import play
    Fs_n = len(rev_out)
    T = 1/Fs
    N = Fs_n 
    t_vec_r = np.arange(int(N))*(T*t)

    play(rev_out)
    plt.plot(t_vec_r, rev_out)
    plt.show() """
