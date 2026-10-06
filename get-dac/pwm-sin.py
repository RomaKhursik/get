import pwm_dac as r2r
import time
import RPi.GPIO as GPIO
import signal_generator as sg
amplitude = 3.183
sfreq = 10
pfreq = 500
t = 0
samplfreq = 1000
GPIO.setmode(GPIO.BCM)
try:
    dac = r2r.PWM_DAC(12, pfreq, 3.183, True)
    while True:
        time.sleep(1/samplfreq)
        t += 1/samplfreq

        s = sg.get_sin_wave_amplitude(sfreq, time.time())

        s *= amplitude
        print(s)
        dac.set_voltage(s)
        #nu = int(s * 255 / 3.183)
        
        
finally:
    print('bruh')
    dac.deinit()
