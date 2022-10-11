import numpy as np 
import matplotlib.pyplot as plt

def fade_in_func(y_sum, duration):
    div = int(duration)
    fade = np.linspace(0,1,div)
    fade_in = y_sum[:div] * fade 

    enveloped_y = np.zeros(len(y_sum))
    enveloped_y = y_sum
    enveloped_y[:div] = fade_in
    return enveloped_y

def decay_func(y_sum, duration, fade_duration):
    div = duration
    exp_div = int(div + fade_duration)
    decay_val = 0.5
    decay_list = np.linspace(1,decay_val,div)
    decay = y_sum[fade_duration:exp_div] * decay_list

    enveloped_y = np.zeros(len(y_sum))
    enveloped_y = y_sum
    enveloped_y[fade_duration:exp_div] = decay
    return enveloped_y, decay_val


def sustain_func(y_sum, duration, fade_in_duration, decay_duration, decay_val):
    div = duration 
    exp_div = fade_in_duration + decay_duration
    exp_div2 = exp_div + div
    sustain_val = decay_val
    sustain = y_sum[exp_div:exp_div2] * sustain_val

    enveloped_y = np.zeros(len(y_sum))
    enveloped_y = y_sum
    enveloped_y[exp_div:exp_div2] = sustain
    return enveloped_y, sustain_val


def fade_out_func(y_sum, duration, sustain_val):
    div = int(duration)
    fade = np.linspace(sustain_val,0,div)
    fade_out = y_sum[-div:] * fade
    enveloped_y = np.zeros(len(y_sum))
    enveloped_y = y_sum
    enveloped_y[-div:] = fade_out
    return enveloped_y

