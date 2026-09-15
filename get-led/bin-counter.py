import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
up_button = 9
down_button = 10
for pin in leds:
    GPIO.setup(pin, GPIO.OUT)
GPIO.output(leds, GPIO.LOW)
GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
num = 0
def dec2bin(value):
    return [int(element) for element in bin(value) [2:].zfill(8)]
sleep_time = 0.2
while True:
    if GPIO.input(up_button) == GPIO.LOW:
        num = num + 1
        if num > 255:
            num = 0
        print(num, dec2bin(num))
        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)
    elif GPIO.input(down_button) == GPIO.LOW:
        num = num - 1
        if num < 0:
            num = 255
        print(num, dec2bin(num))
        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)

