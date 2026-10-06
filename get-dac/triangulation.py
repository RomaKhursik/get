def trian(freq, time):
    nu = 1/freq
    nu-= 2*(time%(1/freq))
    nu = abs(nu)
    #return freq*(1/freq-2*time%(1/freq))
    return nu