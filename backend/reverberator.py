import numpy as np 
import scipy.signal as signal
import matplotlib.pyplot as plt 

"""
Module for applying reverb to the input signal 

Main function is main_reverb, which computes the delay line, calls both comb and all-pass and goes through the algo.  

To produce a reverb effect, call main_reverb with the signal as input and an float/int delay_length > 1.

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

def is_prime(n):
    r = int(n**0.5) 
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f+2) == 0: return False
        f += 6
    return True

def mutuallyPrime(n):
    primes = [11, 17, 19, 23, 29, 31]
    m = []
    for i in range(len(n)):
        val = int(np.round(np.log(n[i])/np.log(primes[i])))
        m.append(val)

    new_list = []

    for i in range(len(n)):
        m_del = primes[i] **(m[i])
        new_list.append(m_del)    
    return new_list


def newPrime(list):
    new_list = []
    for i in list:
        k = 0
        while is_prime(i + k) is False:
            k += 1
        new_list.append(i+k)
    return new_list

def genDelays(delay_length):
    delays_early = [877, 1561, 1715, 1825, 3082, 3510] #Between  10-50ms Comb/early echos
    delays_early = [int(i*delay_length) for i in delays_early] 
    new_early_delays = mutuallyPrime(delays_early)
    delays_early = new_early_delays

    delays = [2205, 2469, 2690, 2998, 3175, 3439] # Betweem 50-80ms
    delays = [int(j*delay_length) for j in delays]
    new_delays = mutuallyPrime(delays)
    delays = new_delays
    return delays_early, delays 


def main_reverb(input, delay_length):
    Fs = 44100 
    delays_early, delays = genDelays(delay_length)
    gains_early = [1.02, 0.818, 0.635, 0.719, 0.267, 0.242]    
    g = 0.9
    allpass_g = 0.7
    rev_to_er_delay = mutuallyPrime([1800 * (delay_length)])[0] 
    if delay_length == 2:
        delay_length = 1
        delays_early, delays = genDelays(delay_length)
        rev_to_er_delay = mutuallyPrime([1800 * (delay_length)])[0] 


    rev_time = 1 / (Fs/rev_to_er_delay)
    T = rev_time
    #gain_list = [10**((-3 * (T) * Fs) / m) for m in delays_early]
    #g1_list = gain_list
    g1_list = [0.41, 0.43, 0.45, 0.47, 0.48, 0.50]
    allpass_delay = 286 

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
        early_reflections = early_reflections + delay(input, int(delays_early[i]), gains_early[i])[:len(input)]

    for j in range(6):
        combs_out = combs_out + comb_with_lp(input, delays[j], g, g1_list[j])

    reverb = allPass(combs_out, allpass_delay, allpass_g)
    early_reflections = np.concatenate((early_reflections, np.zeros(rev_to_er_delay)))
    reverb = delay(reverb, rev_to_er_delay)
    reverb_out = early_reflections + reverb 
    reverb_out = output_gain * ((reverb_out * wet1 + reverb_out * wet2) + np.concatenate((input, np.zeros(rev_to_er_delay))) * dry)
    revout = (reverb_out/ np.max(reverb_out)) 
    return revout

