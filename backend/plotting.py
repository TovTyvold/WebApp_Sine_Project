from pointsCreateSignal import Create_Sine
import numpy as np 
import matplotlib.pyplot as plt

t_vec, Array_of_various_signals, Fs, freqs = Create_Sine(np.array([10,10,10,10,10,10,10]), np.array([200, 400, 450, 500, 550, 600, 800]), 44100, list_ADSR = 0)
y_sum = Array_of_various_signals[0] 
normalzed_y = Array_of_various_signals[1]
y_filtered_low = Array_of_various_signals[2]
y_filtered_high = Array_of_various_signals[3]
y_filtered = Array_of_various_signals[4]
LFO = Array_of_various_signals[5]
y_filtered_LFO = Array_of_various_signals[6]
y_filtered_noise = Array_of_various_signals[7]
saw = Array_of_various_signals[8]
y_filtered_saw = Array_of_various_signals[9]


fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle("Frequency cutoff")
ax1.set_title("Filtered Low")
ax1.set_xlabel("t [s]")
ax1.set_ylabel("A [m]")
ax1.plot(t_vec, y_filtered_low, lw=1)
#plt.savefig(f"backend/figures/demo/Filtered_low.png")



ax2.set_title("Filtered High")
ax2.set_xlabel("t [s]")
ax2.set_ylabel("A [m]")
ax2.plot(t_vec, y_filtered_high, lw=1)
#plt.savefig(f"backend/figures/demo/Filtered_high.png")
plt.tight_layout()
#plt.show()

plt.figure(2)
plt.title("Filtered Low with y on top")
plt.xlabel("t [s]")
plt.ylabel("A [m]")
plt.plot(t_vec, normalzed_y, label= "Normalized", color ='r', ls='--')
plt.plot(t_vec, y_filtered_low, label= "y filtered_low", color= 'b', lw=1)
plt.legend()


plt.figure(3)
plt.title("Filtered High with y on top")
plt.xlabel("t [s]")
plt.ylabel("A [m]")
plt.plot(t_vec, normalzed_y, label= "Normalized", color ='r', ls='--')
plt.plot(t_vec, y_filtered_high, label= "y filtered_high", color= 'b', lw=1)
#plt.savefig(f"backend/figures/demo/Filtered_cutoff.png")
plt.legend()


plt.figure(4)
plt.title("Filtered with y on top")
plt.xlabel("t [s]")
plt.ylabel("A [m]")
plt.plot(t_vec, normalzed_y, label= "Normalized", color ='r', ls='--')
plt.plot(t_vec, y_filtered, label= "y filtered", color= 'b', lw=1)
#plt.savefig(f"backend/figures/demo/Filtered_cutoff.png")
plt.legend()
#plt.show() 

#Apply low_frequency_oscillator

plt.figure(5)
plt.title("LFO")
plt.xlabel("t [s]")
plt.ylabel("A [m]")
plt.plot(t_vec, LFO, label= "LFO", color ='r', ls='--')
plt.plot(t_vec, y_filtered, label= "y filtered", color= 'b', lw=1)
#plt.savefig(f"backend/figures/demo/Filtered_cutoff.png")
plt.legend()

plt.figure(6)
plt.title("LFO")
plt.xlabel("t [s]")
plt.ylabel("A [m]")
plt.plot(t_vec, y_filtered_LFO, label= "LFO", color ='r')
#plt.savefig(f"backend/figures/demo/Filtered_cutoff.png")
plt.legend()
#plt.show() 


plt.figure(7)
plt.title("Saw")
plt.xlabel("t [s]")
plt.ylabel("A [m]")
plt.plot(t_vec, saw, label= "Saw", color ='r')
#plt.savefig(f"backend/figures/demo/Filtered_cutoff.png")
plt.legend()

    
plt.figure(8)
plt.title("Saw and Filtered")
plt.xlabel("t [s]")
plt.plot(t_vec, y_filtered_saw, label= "Saw Filtered", color ='r')
#plt.savefig(f"backend/figures/demo/Filtered_cutoff.png")
plt.legend()
plt.show()


plt.figure(9)
plt.plot(t_vec, y_filtered_noise)
plt.figure(10)
plt.plot(t_vec, y_filtered)
plt.show()