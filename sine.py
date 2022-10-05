  
import numpy as np
import matplotlib.pyplot as plt 


list = [1, 3, 5, 7]
interval = [-2*np.pi, 2*np.pi]
sample_rate = 200
A = 1
def hertz_sine(list, A, interval, sample_rate):
    """  
        Function that outputs a normalized graph corresponding to several frquencies using sine functions
        Arguments
        ---------
        list - dtype list/touple: A list of the submitted frequencies
        A - dtype int: The submitted amplitude
        interval - dtype list/touple: The given interval for our x-cooridnates
        sample_rate - dtype int: The sample rate

        Returns
        --------
        length (int): Number of submitted frequencies
        x_cord (ndarray): Array containing x-values for intervall
        y_cord (ndarray): n-dimensional matrix containing all y-values from different hertz
        norm_max (ndarray): Array containing y-values that are normalized

    """
    length = len(list) 


    # Create arrays to store points
    x_cord = np.linspace(interval[0], interval[1], sample_rate)
    y_cord = np.zeros((length,len(x_cord)))
    
    row = 0
    # Run through each Hertz and the y-coordinate they give
    for hz in list:
        for i in range(len(x_cord)):
            y_cord[row][i] = A * np.sin(2 * np.pi * hz * x_cord[i])
        row = row + 1

    # Normalize through maximum
    y_sum = 0
    for i in range(length):
        y_sum += y_cord[i][:] 
    norm_max = y_sum/np.max(y_sum)
    return length, x_cord, y_cord, norm_max, 

    


def hertz_sine_simple(list):
    """  
        Function that outputs a normalized graph corresponding to several frquencies using sine functions
        Arguments
        ---------
        list - dtype list/touple: A list of the submitted frequencies

        Returns
        --------
        length (int): Number of submitted frequencies
        x_cord (ndarray): Array containing x-values for intervall
        y_cord (ndarray): n-dimensional matrix containing all y-values from different hertz
        norm_max (ndarray): Array containing y-values that are normalized

    """
    length = len(list) 


    # Create arrays to store points
    x_cord = np.linspace(-2*np.pi, 2*np.pi, 200)
    y_cord = np.zeros((length,len(x_cord)))
    
    row = 0
    # Run through each Hertz and the y-coordinate they give
    for hz in list:
        for i in range(len(x_cord)):
            y_cord[row][i] = np.sin(2 * np.pi * hz * x_cord[i])
        row = row + 1

    # Normalize through maximum
    y_sum = 0
    for i in range(length):
        y_sum += y_cord[i][:] 
    norm_max = y_sum/np.max(y_sum)
    return length, x_cord, y_cord, norm_max, 
