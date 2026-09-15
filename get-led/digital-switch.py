import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
button = 13
led = 26
GPIO.setup(button, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
state = 0
while True:
    if GPIO.input(button):
        state = not state
        GPIO.output(led, state)
        time.sleep(0.2)