import numpy as np 
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def Create_Signal(amplitudes, frequencies,Fs):
    n = np.random.randint(3,10)
    if not amplitudes:
        """ print("-------------------------------")
        print("No amplitudes, list is empty.")
        print(f"Generating {n} random amplitudes...")
        amplitudes = 50 * np.random.rand(1,n) """
        amplitudes = np.array([6, 6, 6])

    if not Fs:
        Fs = 300
        print(f"Sampling is {Fs}")


    if not frequencies:
        max_freq_input = Fs/2
        """ print("-------------------------------")
        print("No frequencies, list is empty.")
        print(f"Generating {n} random frequencies...")
        #n Frequencies between [0,100)
        list_numbers = np.linspace(30,max_freq_input,n)
        frequencies = list_numbers * np.random.rand(1,n) """
        frequencies = np.array([100, 33, int(max_freq_input)])


    n_signals = len(frequencies)

    """ min_freq = np.min(frequencies)
    max_freq = np.max(frequencies)
    """
    # Set variables
    T = 1/Fs # sampling period
    #t = max_freq/(n_signals * (1/2) * min_freq) # seconds of sampling
    t = 0.5
    N = Fs*t # total points in signal
    omega = 2*np.pi*frequencies # angular frequency for sine waves
    t_vec = np.arange(N)*T # time vector for plotting
    y = np.zeros((n_signals,len(t_vec)))

    k = 0
    y_sum = 0
    for i in omega:
        y[k] = amplitudes[k] * np.sin(i*t_vec)
        #y[k] = np.sin(i[k]*t_vec) #Amplitude == 1
        y_sum += y[k] 
        k += 1 
    
    norm_max = y_sum/np.max(y_sum)
    return t_vec, norm_max, y_sum, Fs
