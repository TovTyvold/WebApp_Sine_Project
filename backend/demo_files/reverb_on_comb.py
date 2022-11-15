
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
    t = 3
    t_vec = np.arange(t*N) * (T * t)
    omega = 2* np.pi 
    #sine_add = 0.4*np.sin(np.linspace(-8 * np.pi,0 * np.pi,int(len(t_vec))))
    #omega = 2 * np.pi* sine_add
    y_sum = 0
    k = 0
    for i in frequencies:
        y_sum += amplitudes[k] * np.sin(omega * i * t_vec)
    
    adsr = envelope.getSymmEnv([0.3,0.2,1,0.2], 0.75, 0, t)
    y_sum = list(map(lambda a,b : a*b, bezierCurve.compositeOn(adsr, t_vec), y_sum))

    norm_y = y_sum / np.max(np.abs(y_sum))
    #play(norm_y.copy())
    combed = dirac_comb_discrete(norm_y.copy(), 5, 10)
    play(combed)
    revout = Reverb_(combed.copy(), room_size=1, wet_level = 0.6, dry_level = 0.4, width = 1)
    play(revout)
    wav = list(norm_y) + list(np.zeros(int(Fs/2))) + list(revout)
    wave_file(wav, wav2=None, fname="Reverb3.wav", amp=1, sample_rate=44100)
    return None
Create_Sine([1, 1, 1], [50, 100, 150])


