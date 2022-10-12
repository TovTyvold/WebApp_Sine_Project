from envelope import fade_in_func, sustain_func, decay_func, fade_out_func




def envelope_slice_func(y_sum, duration, boolean_env):

        """  
        Function that outputs frequencies after taking in a signal with/without noise/chaos using fft. 
        ---------
        y_sum - dtype ndarray: Set of output values 
        duration - dtype int: Number of samples

        Returns
        --------
        y_sum - dtype ndarray: Set of output values with env effects
        """

        
        dur_scale = boolean_env.count(True)
        if dur_scale == 0:
            dur_scale = 1
        n_dur = int(duration / dur_scale)
        dur_list = [0, 0, 0, 0]



        counter = 0
        for i in boolean_env:
            if i == True:
                dur_list[counter] = n_dur
            counter += 1

        fade_in_duration = dur_list[0]
        decay_duration = dur_list[1]
        sustain_duration = dur_list[2]
        fade_out_duration = dur_list[3]

        #Fade In
        if boolean_env[0] == True:
            y_sum = fade_in_func(y_sum, fade_in_duration)
        
        #Decay
        if boolean_env[1] == True:
            if boolean_env[0] == True:
                y_sum, decay_val = decay_func(y_sum, decay_duration, fade_in_duration)
                
            else:
                y_sum, decay_val = decay_func(y_sum, decay_duration, fade_duration = 0)

        #Sustain
        if boolean_env[2] == True:
            if boolean_env[1] == True:
                y_sum, sustain_val = sustain_func(y_sum, sustain_duration, fade_in_duration, decay_duration, decay_val)

            elif boolean_env[1] == False:
                y_sum, sustain_val = sustain_func(y_sum, sustain_duration, fade_in_duration, decay_duration, decay_val = 1)


        #Fade Out
        if boolean_env[2] == True: 
            y_sum = fade_out_func(y_sum, fade_out_duration, sustain_val)
        y_env = y_sum
        return y_env, boolean_env