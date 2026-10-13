import time
import RPi.GPIO as GPIO


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose

        # bit7 ... bit0 блока 8-bit ADC платы get-adc
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        bits = [int(element) for element in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)
        if self.verbose:
            print(f"Число на входе ЦАП: {number}, биты: {bits}")

    def comparator_above(self):
        # 1, когда напряжение на входе DAC больше, чем на входе SIG
        comparison = GPIO.input(self.comp_gpio)
        if self.verbose:
            print(f"Выход компаратора: {comparison}")
        return comparison == 1

    def sequential_counting_adc(self):
        # АЦП последовательного счёта: перебираем числа от 0 вверх
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            if self.comparator_above():
                return number
        return 255

    def get_sc_voltage(self):
        return self.sequential_counting_adc() / 255 * self.dynamic_range

    def successive_approximation_adc(self):
        # АЦП последовательного приближения: биты от старшего к младшему
        number = 0
        for bit_number in range(7, -1, -1):
            candidate = number | (1 << bit_number)
            self.number_to_dac(candidate)
            time.sleep(self.compare_time)
            if not self.comparator_above():
                number = candidate
        return number

    def get_sar_voltage(self):
        return self.successive_approximation_adc() / 255 * self.dynamic_range


if __name__ == "__main__":
    try:
        # динамический диапазон ЦАП измерить мультиметром на тест-поинте OUT
        adc = R2R_ADC(3.293)
        while True:
            print(f"Напряжение: {adc.get_sar_voltage():.3f} В")
    finally:
        adc.deinit()
