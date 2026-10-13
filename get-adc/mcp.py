import time
import adc_plot
import mcp3021_driver

dynamic_range = 5.0
duration = 5.0

try:
    mcp = mcp3021_driver.MCP3021(dynamic_range)

    voltage_values = []
    time_values = []

    start_time = time.time()
    while time.time() - start_time < duration:
        voltage_values.append(mcp.get_voltage())
        time_values.append(time.time() - start_time)
    print(f"Измерений: {len(voltage_values)}")

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
    adc_plot.plot_sampling_period_hist(time_values)
finally:
    mcp.deinit()
