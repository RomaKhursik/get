import time
import mcp3021_driver
import adc_plot

# динамический диапазон АЦП, В (напряжение питания блока 12-bit ADC, измеряется мультиметром)
DYNAMIC_RANGE = 5.0
# продолжительность измерений, с
DURATION = 5.0

if __name__ == "__main__":
    mcp = mcp3021_driver.MCP3021(DYNAMIC_RANGE)

    voltage_values = []
    time_values = []

    try:
        start_time = time.time()
        while time.time() - start_time < DURATION:
            voltage_values.append(mcp.get_voltage())
            time_values.append(time.time() - start_time)
        print(f"Сделано измерений: {len(voltage_values)}")

        adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
        adc_plot.plot_sampling_period_hist(time_values)
    finally:
        mcp.deinit()
