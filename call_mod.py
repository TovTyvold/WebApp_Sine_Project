from sine import hertz_sine, hertz_sine_simple
import numpy as np
import matplotlib.pyplot as plt

list = [1, 3, 5, 7]
""" interval = [-2*np.pi, 2*np.pi]
sample_rate = 200
A = 1
length, x, y, norm_max = hertz_sine(list, A, interval, sample_rate)

fig, ax = plt.subplots(1,length,figsize=(10,8),sharex=True)

for k in range(length):
    ax[k].plot(x, y[k])
    ax[k].set_title(f"Frequency is = {list[k]} Hz")  

plt.tight_layout()

plt.figure(2)
plt.plot(x,norm_max,'r--')
plt.title("Normalization through maximum")


plt.show()  """

print("Running simple converter")
length, x, y, norm_max = hertz_sine_simple(list)

fig, ax = plt.subplots(1,length,figsize=(10,8),sharex=True)

for k in range(length):
    ax[k].plot(x, y[k])
    ax[k].set_title(f"Frequency is = {list[k]} Hz")  

plt.tight_layout()

plt.figure(2)
plt.plot(x,norm_max,'r--')
plt.title("Normalization through maximum")

print("Finished running, plotting!")
plt.show() 