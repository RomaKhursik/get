import r2r_dac as r2r
import time
import RPi.GPIO as GPIO
import signal_generator as sg
import triangulation as tr
amplitude = 3.183
freq = 10
t = 0
samplfreq = 1000
try:
    dac = r2r.R2R_DAC([22,27,17,26,25,21,20,16], 3.183, True)
    while True:
        time.sleep(1/samplfreq)
        s = tr.trian(freq, time.time())

        s *= amplitude
        print(s)
        nu = dac.set_voltage(s)
        #nu = int(s * 255 / 3.183)
        GPIO.output(dac.gpio_bits, nu)
        print(nu)
        
        
finally:
    print('bruh')
    dac.deinit()