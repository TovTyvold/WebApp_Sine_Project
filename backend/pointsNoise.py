import colorednoise as cn

def coloredNoise(y, exponent, fmin = 0):
    """  
    Function that outputs signal with noise added 
    --------

    Inputs
    --------
    y - dtype ndarray: Set of (x,y) values 
    exponent - dtype int: The exponent = 1; flicker / pink noise. The exponent = 2; brown noise
    fmin - dtype float/int: Low-frequency cutff. 1 equals to white noise(regardless of exponent?)

    Returns
    --------
    y + Color_noise - dtype ndarray: Set of output values with noise effects
    """
    samples = len(y)  # number of samples to generate (time series extension)
    Color_noise = cn.powerlaw_psd_gaussian(exponent, samples, fmin)
    print(Color_noise)
    return y + Color_noise