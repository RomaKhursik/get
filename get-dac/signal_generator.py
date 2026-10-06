import numpy as np
import time
def get_sin_wave_amplitude(freq, time):
    x = np.sin(2*3.1415*freq*time)
    return 0.5*(1+x)
def wait_for_sampling_period(samplfreq):
    time.sleep(1/samplfreq)
    return None
