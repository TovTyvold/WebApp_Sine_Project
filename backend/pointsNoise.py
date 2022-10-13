import colorednoise as cn

def coloredNoise(exponent, y, fmin, noise_intensity):
    """  
    Function that outputs signal with noise added 
    --------

    Inputs
    --------
    y - dtype ndarray: Set of (x,y) values 
    exponent - dtype int: The exponent = 1; flicker / pink noise. The exponent = 2; brown noise
    fmin - dtype float/int: Low-frequency cutff. 1 equals to white noise(regardless of exponent?) Must be 0 < fmin < 0.5
    noise_intensity - dtype float: Noise amplifier

    Returns
    --------
    y + Color_noise * noise_intensity - dtype ndarray: Set of output values with noise effects sacled with noise_intensity
    """
    samples = len(y)  # number of samples to generate (time series extension)
    Color_noise = cn.powerlaw_psd_gaussian(int(exponent), int(samples), fmin)
    return y + Color_noise * noise_intensity