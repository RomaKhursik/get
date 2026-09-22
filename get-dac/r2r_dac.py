import RPi.GPIO as GPIO
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        for i in range(8):
            bit_value = (number >> i) & 1
            GPIO.output(self.gpio_bits[i], bit_value)
        if self.verbose:
            debug_bits = [(number >> i) & 1 for i in range(8)]
            print(f"Число на входе ЦАП: {number}, биты: {debug_bits}")
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            return
        number = int(round((voltage / self.dynamic_range) * 255))
        self.set_number(number)
if __name__ == "__main__":
    try:
        dac = R2R_DAC([22, 27, 17, 26, 25, 21, 20, 16], 3.183, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()