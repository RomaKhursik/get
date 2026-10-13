import time
import r2r_adc
import adc_plot

# динамический диапазон ЦАП, В (измеряется мультиметром на тест-поинте OUT блока 8-bit ADC)
DYNAMIC_RANGE = 3.293
# продолжительность измерений, с
DURATION = 5.0

if __name__ == "__main__":
    adc = r2r_adc.R2R_ADC(DYNAMIC_RANGE, compare_time=0.0001)

    voltage_values = []
    time_values = []

    try:
        start_time = time.time()
        while time.time() - start_time < DURATION:
            voltage_values.append(adc.get_sar_voltage())
            time_values.append(time.time() - start_time)
        print(f"Сделано измерений: {len(voltage_values)}")

        adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
        adc_plot.plot_sampling_period_hist(time_values)
    finally:
        adc.deinit()
