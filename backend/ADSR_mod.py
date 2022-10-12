
import numpy as np

def ADSR(list_ADSR, N, t):
    Amp_array = np.zeros(N)
    A_time = int((N*list_ADSR[0])/t)
    D_time = int((N*list_ADSR[1])/t)
    S_time = int((N*list_ADSR[2])/t)
    R_time = int((N*list_ADSR[3])/t)
    A = np.zeros(A_time)
    D = np.zeros(D_time)
    S = np.zeros(S_time)
    R = np.zeros(R_time)

    A_lin = np.linspace(0,4,A_time)
    D_lin = np.linspace(4,0.5,D_time)
    R_lin = np.linspace(0.5,0,R_time)
    Attack = A + A_lin
    Decay = D + D_lin
    Sustain = S + 0.5
    Release = R + R_lin

    Prog_1 = A_time + D_time
    Prog_2 = A_time + D_time + S_time


    Amp_array[:A_time] = Attack
    Amp_array[A_time:Prog_1] = Decay
    Amp_array[Prog_1:Prog_2] = Sustain
    Amp_array[Prog_2:Prog_2 + R_time] = Release
    return Amp_array
