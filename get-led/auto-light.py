import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
sensor = 6
GPIO.setup(sensor, GPIO.IN)
while True:
    sensor_state = GPIO.input(sensor)
    GPIO.output(led, not sensor_state)
    time.sleep(0.2)