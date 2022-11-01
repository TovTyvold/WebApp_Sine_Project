
from matplotlib.widgets import Slider, Button 
import numpy as np 
import matplotlib.pyplot as plt
from soundGen import play
from reverberator import main_reverb

def modSlide():
    t = 2
    Fs = 44100
    T = 1 / Fs 
    N = Fs 
    t_vec = np.arange(t*N)*(T*t)


    #Create simple sine wave 
    def sine(amplitudes, frequencies, t_vec):  
        y = np.zeros(len(t_vec))

        #omega = 2 * np.pi
        sine_add = np.sin(np.linspace(-12 * np.pi,12 * np.pi,len(t_vec)))
        omega = 2 * np.pi* sine_add
        y = amplitudes * np.sin(omega * frequencies * t_vec)  
        return y
    input = sine(1, 5, t_vec)
    
    # Function that is versatile/ prone to change
    def func(input, g):
        return main_reverb(input, g)

    init_g = 0.7
    t_vec_updated = np.arange(t*N + 1800)*(T*t)

    fig, ax = plt.subplots()
    # Here we want to call the function we wish to compute
    line, = ax.plot(t_vec_updated, func(input, init_g), lw=2)
    fig.subplots_adjust(left= 0.25, bottom = 0.25)

    axg = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    g_slider = Slider(ax=axg, label = 'GAIN', valmin = 0.6, valmax = 1, valinit=init_g)
    def update(val):
        play(func(input, g_slider.val))
        line.set_ydata(func(input, g_slider.val))
        fig.canvas.draw_idle()

    g_slider.on_changed(update)

    resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor = '0.975')

    def reset(event):
        g_slider.reset()
    button.on_clicked(reset)
    
    plt.show()

if __name__ == "__main__":
    modSlide()