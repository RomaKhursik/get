import RPi.GPIO as GPIO
import time


class R2R_ADC:
    """
    8-битный АЦП на базе параллельного R2R ЦАП и компаратора (плата get-adc, блок 8-bit ADC).

    Измерение напряжения сводится к подбору такого числа, которое надо подать
    на вход ЦАП, чтобы напряжение на его выходе стало ближе всего к напряжению
    на входе АЦП (выход потенциометра). Результат сравнения двух напряжений
    читается с выхода компаратора (GPIO 21):

        comp == 1 (светодиод COMP горит) -> напряжение на входе DAC больше,
                                            чем на входе SIG;
        comp == 0                        -> напряжение на входе DAC меньше,
                                            чем на входе SIG.

    Реализованы два алгоритма подбора числа:
        последовательный счёт   -- sequential_counting_adc();
        последовательное приближение (бинарный поиск) -- successive_approximation_adc().
    """

    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range    # динамический диапазон ЦАП, В (измеряется мультиметром)
        self.compare_time = compare_time      # пауза на то, чтобы компаратор успел сравнить напряжения
        self.verbose = verbose                # печать отладочной информации

        # GPIO-пины ЦАП по шелкографии платы get-adc:
        # int7 ... int0 (список от старшего бита к младшему)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        # GPIO-пин, подключённый к выходу компаратора
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
        GPIO.output(self.bits_gpio, 0)

    def deinit(self):
        """Погасить светодиоды ЦАП и вернуть GPIO в исходное состояние."""
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        """Подать целое число 0..255 на параллельный вход 8-битного ЦАП."""
        number = int(number)
        if not 0 <= number <= 255:
            raise ValueError("Число выходит за разрядность 8-битного ЦАП (0 - 255)")
        bits = [int(element) for element in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)
        if self.verbose:
            print(f"Число на входе ЦАП: {number:3d} ({''.join(str(b) for b in bits)})")

    def comparator_above(self):
        """
        Прочитать выход компаратора.

        Возвращает True, если напряжение на входе DAC (выход нашего ЦАП)
        больше напряжения на входе SIG (выход потенциометра), то есть
        когда горит светодиод компаратора.
        """
        comparison = GPIO.input(self.comp_gpio)
        if self.verbose:
            print(f"Выход компаратора: {comparison}")
        return comparison == 1

    def sequential_counting_adc(self):
        """АЦП последовательного счёта: перебираем числа от 0 вверх."""
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            if self.comparator_above():
                return number
        # напряжение на входе АЦП больше максимально возможного напряжения ЦАП
        return 255

    def get_sc_voltage(self):
        """Измеренное напряжение, В (АЦП последовательного счёта)."""
        return self.sequential_counting_adc() / 255 * self.dynamic_range

    def successive_approximation_adc(self):
        """АЦП последовательного приближения: определяем биты от старшего к младшему."""
        number = 0
        for bit_number in range(7, -1, -1):
            candidate = number | (1 << bit_number)
            self.number_to_dac(candidate)
            time.sleep(self.compare_time)
            if not self.comparator_above():
                # напряжение на выходе ЦАП ещё не превысило входное -- бит подходит
                number = candidate
        return number

    def get_sar_voltage(self):
        """Измеренное напряжение, В (АЦП последовательного приближения)."""
        return self.successive_approximation_adc() / 255 * self.dynamic_range


if __name__ == "__main__":
    try:
        # динамический диапазон ЦАП измерить мультиметром на тест-поинте OUT
        adc = R2R_ADC(3.293, compare_time=0.01, verbose=False)
        while True:
            print(f"Напряжение: {adc.get_sar_voltage():.3f} В")
    except KeyboardInterrupt:
        print("\nСкрипт остановлен с клавиатуры")
    finally:
        adc.deinit()
