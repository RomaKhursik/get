import RPi.GPIO as GPIO
dac_bits = [22, 27, 17, 26, 25, 21, 20, 16]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_bits, GPIO.OUT)
dynamic_range = 3.3
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)
def number_to_dac(number):
    binary_string = bin(number)[2:].zfill(8)
    binary_bits = [int(bit) for bit in reversed(binary_string)]
    for i in range(8):
        GPIO.output(dac_bits[i], binary_bits[i])

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
            print(f"Число: {number}, Биты (от младшего к старшему): {[int(x) for x in reversed(bin(number)[2:].zfill(8))]}")
        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз/n")
finally:
    GPIO_output(dac_bits, 0)
    GPIO.cleanup()