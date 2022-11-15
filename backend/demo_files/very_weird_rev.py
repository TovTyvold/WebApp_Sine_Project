
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from matplotlib.widgets import Slider, Button
from wave_to_file import wave_file
from filterAudio import low_pass_Filter, high_pass_Filter, dirac_comb_discrete,\
    singleShift, vibratoFunc, Reverb_
from coloredNoise import plot_spectrum, white_noise, brownian_noise, violet_noise, pink_noise, blue_noise
from soundGen import play
from pointsNoise import cNoise
from pointsCalculation import noteToFreq
import envelope
import bezierCurve

plt.style.use('ggplot')

def Create_Sine(amplitudes, frequencies):
    Fs = 44100
    T = 1/(Fs) 
    N = Fs
    t = 4
    t_vec = np.arange(t*N) * (T * t)
    omega = 2* np.pi 
    sine_add = 0.4*np.sin(np.linspace(-8 * np.pi,0 * np.pi,int(len(t_vec)/2)))
    sin_add = 0.3*np.sin(np.linspace(16 * np.pi,-32 * np.pi,int(len(t_vec)/2)))
    trig = np.zeros(len(t_vec))
    trig[:int(len(t_vec)/2)] = sine_add 
    trig[int(len(t_vec)/2):] = sin_add 
    omega = 2 * np.pi* trig
    y_sum = 0
    k = 0
    for i in frequencies:
        y_sum += amplitudes[k] * np.sin(omega * i * t_vec)
    
    #adsr = envelope.getSymmEnv([0.2,0.2,0.6,0.2], 0.75, 0, t)
    #y_sum = list(map(lambda a,b : a*b, bezierCurve.compositeOn(adsr, t_vec), y_sum))

    norm_y = y_sum / np.max(np.abs(y_sum))
    play(norm_y.copy())
    revout = Reverb_(norm_y.copy(), room_size=0.5, wet_level = 0.8, dry_level = 0.2, width = 0.15)
    play(revout)
    wav = list(norm_y) + list(np.zeros(int(Fs/2))) + list(revout)
    wave_file(wav, wav2=None, fname="Reverb3.wav", amp=1, sample_rate=44100)
    return None
Create_Sine([1, 1, 1], [50, 100, 150])