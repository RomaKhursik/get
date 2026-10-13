import time
import adc_plot
import r2r_adc

dynamic_range = 3.293
duration = 5.0

try:
    adc = r2r_adc.R2R_ADC(dynamic_range, compare_time=0.0001)

    voltage_values = []
    time_values = []

    start_time = time.time()
    while time.time() - start_time < duration:
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.time() - start_time)
    print(f"Измерений: {len(voltage_values)}")

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
    adc_plot.plot_sampling_period_hist(time_values)
finally:
    adc.deinit()
