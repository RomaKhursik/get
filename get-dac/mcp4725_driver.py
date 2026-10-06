import smbus
import RPi.GPIO as GPIO
class MCP4725:
    def __init__(self, dr, address=0x61, verbose = True):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        self.dr = dr
    def deinit(self):
        self.bus.close()
    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
        if not(0<= number <= 4095):
            print("Число выходит за разрядность MCP4752 (12 бит)")
        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address <<1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")
    def set_voltage(self, voltage):
        print(self.dr)
        if not(0.0 <= voltage <= self.dr):
            nu = 0
            return 0

        nuu = int(voltage/self.dr * 4095)
        print(self.dr)
        nu = self.set_number(nuu)
        GPIO.output(2, nu)
        return nu
1



if __name__ == "__main__":
    try:
        dac = MCP4725(5, True)
        while True:
            try:
                voltage = float(input("Введите напряжене в Вольтах: "))
                nu = dac.set_voltage(voltage)
                
                print(nu)
            except ValueError:
                print("Вы не ввели число. Попробуйте еще раз")
    finally:
        dac.deinit()