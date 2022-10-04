import numpy as np
import matplotlib.pyplot as plt 


list = [1, 3, 5, 7]
A = 1
def hertz_sine(list, A):
    length = len(list) 

    # Create arrays to store points
    x_cord = np.linspace(-2*np.pi, 2*np.pi, 200)
    y_cord = np.zeros((length,len(x_cord)))
    
    row = 0
    # Run through each Hertz and the y-coordinate they give
    for hz in list:
        for i in range(len(x_cord)):
            y_cord[row][i] = A * np.sin(hz * x_cord[i])
        row = row + 1

    # Normalize through maximum
    y_sum = 0
    for i in range(length):
        y_sum += y_cord[i][:] 
    norm_max = y_sum/np.max(y_sum)

    # Normalize through signal theory
    norm_sum = 0
    for i in range(length):
        norm_sum += (y_cord[i] * y_cord[i])
    norm_signal = y_sum/(np.sqrt(norm_sum/(length**2)))

    
    return length, x_cord, y_cord, norm_max, norm_signal

        

length, x, y, norm_max, norm_signal = hertz_sine(list, A)


fig, ax = plt.subplots(1,length,figsize=(10,8),sharex=True)

for k in range(length):
    ax[k].plot(x, y[k])
    ax[k].set_title(f"Frequency is = {list[k]} Hz")  

plt.tight_layout()

plt.figure(2)
plt.plot(x,norm_max,'r--')

plt.title("Normalization through maximum")

plt.figure(3)
plt.plot(x,norm_signal,'b')

plt.title("Normalization through signal theory")
plt.show()