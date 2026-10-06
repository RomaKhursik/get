import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

leds = [22,27,17,26,25,21,20,16]
GPIO.setup(leds, GPIO.OUT)
dynamic_range = 3.3
GPIO.output(leds, 0)
def voltage_to_number(voltage):
    if not(0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} B")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage/dynamic_range * 255)
def number_to_dac(number):
    return [int(el) for el in reversed(bin(number)[2:].zfill(8))]

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            nu = number_to_dac(number)
            print(number, nu)
            GPIO.output(leds, nu)
        except ValueError:
            print("Вы не ввели число. Попробуйте еще раз")
finally:
    GPIO.output(leds, 0)
    GPIO.cleanup()