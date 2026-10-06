import pwm_dac as r2r
import time
import RPi.GPIO as GPIO
import triangulation as tr
amplitude = 3.183
sfreq = 5
pfreq = 500
t = 0
samplfreq = 100
GPIO.setmode(GPIO.BCM)
try:
    dac = r2r.PWM_DAC(12, pfreq, 3.183, True)
    while True:
        time.sleep(1/samplfreq)

        s = tr.trian(sfreq, time.time())

        s *= amplitude
        print(s)
        dac.set_voltage(s)
        #nu = int(s * 255 / 3.183)
        
        
finally:
    print('bruh')
    dac.deinit()
