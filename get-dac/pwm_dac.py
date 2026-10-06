import RPi.GPIO as GPIO
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)
        global pwm
        pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
    def deinit(self):
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()
        pwm.stop()
    def set_voltage(self, voltage):
        if not(0.0 <= voltage <= self.dynamic_range):
            print("bruh")
        else:
            nu = voltage/self.dynamic_range * 100
            print(nu)
            pwm.start(nu)


        return None
    
if __name__ == "__main__":
    try:
        d = 0
        dac = PWM_DAC(12, 500, 3.183, True)
        while True:
            try:
                voltage = float(input("Введите напряжене в Вольтах: "))
                dac.set_voltage(voltage)
                #pwm.ChangeDutyCycle(d)
                print("ok")
            except ValueError:
                print("Вы не ввели число. Попробуйте еще раз")
    finally:
        dac.deinit()