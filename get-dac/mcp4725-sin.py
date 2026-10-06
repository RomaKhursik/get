import mcp4725_driver as mcp
import time
import RPi.GPIO as GPIO
import signal_generator as sg

amplitude = 3
sfreq = 10
samplfreq = 1000
dynamic_range = 3.183

try:
    dac = mcp.MCP4725(dynamic_range)
    while True:
        try:
            s = sg.get_sin_wave_amplitude(sfreq, time.time())
            time.sleep(1/samplfreq)
            nu = dac.set_voltage(s)
            print(nu)
        except ValueError:
            print('')
finally:
    dac.deinit()
    print("")