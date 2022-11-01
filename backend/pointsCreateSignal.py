
import time
import numpy as np 
import matplotlib.pyplot as plt
from numpy.linalg import norm
from matplotlib.widgets import Slider, Button 

from filterAudio import low_pass_Filter, high_pass_Filter, dirac_comb_discrete, weierstrassFunc,\
    semitoneFunc, singleShift, vibratoFunc, whiteChorus
from reverberator import main_reverb
from coloredNoise import plot_spectrum, white_noise, brownian_noise, violet_noise, pink_noise, blue_noise
from soundGen import play
from pointsFrequency import signal_to_hertz
from pointsNoise import coloredNoise
from plotting import plot_array
from pointsCalculation import noteToFreq

plt.style.use('ggplot')


def Create_Sine(amplitudes, frequencies):
    Fs = 44100
    T = 1/(Fs) 
    N = Fs
    t = 1
    t0 = time.time()

    # Set variables
    def slider_plot(amplitudes, frequencies, t_vec):  
        y = np.zeros(len(t_vec))

        #omega = 2 * np.pi
        sine_add = np.sin(np.linspace(-12 * np.pi,12 * np.pi,len(t_vec)))
        omega = 2 * np.pi* sine_add
        y = amplitudes * np.sin(omega * frequencies * t_vec)  
        return y

    init_amp = amplitudes[0]
    init_freq = frequencies[0]
    t_vec = np.arange(t*N)*(T*t)

    y = slider_plot(amplitudes, frequencies, t_vec)


    fig, ax = plt.subplots()
    line, = ax.plot(t_vec, slider_plot(init_amp, init_freq, t_vec), lw=2)

    fig.subplots_adjust(left= 0.25, bottom = 0.25)

    axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    freq_slider = Slider(ax=axfreq, label = 'Frequency [Hz]', valmin = 0.1, valmax = 40, valinit=init_freq)

    axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
    amp_slider = Slider(ax=axamp, label = 'Amplitude', valmin = 0, valmax = 10, valinit=init_amp, orientation='vertical')

    def update(val):
        line.set_ydata( slider_plot(amp_slider.val, freq_slider.val, t_vec))
        fig.canvas.draw_idle()

    freq_slider.on_changed(update)
    amp_slider.on_changed(update)

    resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor = '0.975')

    def reset(event):
        freq_slider.reset()
        amp_slider.reset()
    button.on_clicked(reset)
    plt.show()

    """ plt.ion()
    plt.figure()
    plt.show()
    plt.pause(4)
    plt.ioff()  """



    t1 = time.time()
    total = t1-t0
    print(f"Timing stopped, END OF FUNCTION! It took {total:0.7f}s")
    return Fs, frequencies



t0_func = time.time()
print("Timing outside func started....")

Create_Sine([1], [50])


t1_func = time.time()
total = t1_func-t0_func
print(f"Timing outside func stopped! It took {total:0.7f}s")



