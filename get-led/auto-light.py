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
 
        print("\nОстановлено пользователем.")

import pandas as pd
import matplotlib.pyplot as plt
 
# 1. Загрузка данных (разделитель , или ; определяется автоматически)
data = pd.read_csv('data.csv', sep=None, engine='python')
print(data.head())  # посмотреть названия столбцов
 
t = data.iloc[:, 0]   # первый столбец — время
u = data.iloc[:, 1]   # второй столбец — напряжение на конденсаторе
 
# 2. Постоянная времени τ
u0, u_end = u.iloc[0], u.iloc[-1]
if u_end > u0:   # заряд: 63 % от установившегося значения
    u_tau = u0 + 0.632 * (u_end - u0)
    i_tau = (u >= u_tau).idxmax()
else:            # разряд: 37 % от начального значения
    u_tau = u_end + 0.368 * (u0 - u_end)
    i_tau = (u <= u_tau).idxmax()
tau = t[i_tau]
print(f'τ ≈ {tau:.4g} с')
 
# 3. График
plt.figure(figsize=(8, 5))
plt.plot(t, u, label='Напряжение на конденсаторе')
plt.axvline(tau, color='gray', linestyle='--')
plt.axhline(u_tau, color='gray', linestyle='--')
plt.plot(tau, u_tau, 'ro', label=f'τ ≈ {tau:.3g} с')
 
plt.title('Зависимость напряжения на конденсаторе от времени')
plt.xlabel('Время, с')
plt.ylabel('Напряжение, В')
plt.grid(True)
plt.legend()
 
# 4. Сохранение вместо plt.show()
plt.savefig('rc-plot.png', dpi=300)
 
