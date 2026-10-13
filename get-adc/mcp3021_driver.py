import smbus
import time


class MCP3021:
    """
    Драйвер 10-битного АЦП MCP3021 (шина I2C) в блоке 12-bit ADC платы get-adc.

    Микросхема передаёт результат преобразования двумя байтами:
    младшие 2 бита -- в первым пришедшем байте (upper), остальные 8 бит --
    во втором байте (lower). Итоговое число собирается из этих частей.

    Перед запуском, после каждой перезагрузки Raspberry Pi, нужно выставить
    на GPIO2 и GPIO3 альтернативную функцию линий i2c1:

        raspi-gpio set 2 a0
        raspi-gpio set 3 a0
    """

    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range    # динамический диапазон АЦП, В (напряжение VCC)
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        """Освободить шину I2C."""
        self.bus.close()

    def get_number(self):
        """Прочитать из микросхемы число 0..1023, пропорциональное входному напряжению."""
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: {upper_data_byte:x}, "
                  f"Младший байт: {lower_data_byte:x}, Число: {number}")
        return number

    def get_voltage(self):
        """Измеренное напряжение, В."""
        return self.get_number() / 1023 * self.dynamic_range


if __name__ == "__main__":
    try:
        # динамический диапазон измерить мультиметром на контакте PWR блока 12-bit ADC
        mcp = MCP3021(5.0, verbose=False)
        while True:
            print(f"Напряжение: {mcp.get_voltage():.3f} В")
            time.sleep(1)
    finally:
        mcp.deinit()
