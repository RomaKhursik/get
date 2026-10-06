import RPi.GPIO as GPIO
leds = [22,27,17,26,25,21,20,16]

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    def set_number(self, number):
        return [int(el) for el in reversed(bin(number)[2:].zfill(8))]
    def set_voltage(self, voltage):
        if not(0.0 <= voltage <= self.dynamic_range):
            return 0

        nuu = int(voltage/self.dynamic_range * 255)
        print(self.dynamic_range)
        nu = self.set_number(nuu)
        return nu
    
if __name__ == "__main__":
    try:
        dac = R2R_DAC([16,20,21,25,26,17,27,22], 3.183, True)
        while True:
            try:
                voltage = float(input("Введите напряжене в Вольтах: "))
                nu = dac.set_voltage(voltage)
                GPIO.output(leds, nu)
                print(nu)
            except ValueError:
                
                print("Вы не ввели число. Попробуйте еще раз")
    finally:
        dac.deinit()

