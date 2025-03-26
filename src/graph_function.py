import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# plt.style.use('seaborn')

def create_real_time_plot(time_data, value_data, variable_name, window_size=30):
    """
    Creates a real-time plot that updates with new data.
    
    Args:
        time_data (list): List of timestamps in seconds
        value_data (list): List of values to plot
        variable_name (str): Name of the variable for y-axis label
        window_size (int): Number of points to show in the moving window
    """
    plt.clf()  # Clear any existing plots
    
    # Only show the last window_size points
    if len(time_data) > window_size:
        time_data = time_data[-window_size:]
        value_data = value_data[-window_size:]
    
    plt.plot(time_data, value_data, 'b-')
    plt.grid(True)
    plt.xlabel('Time (seconds)')
    plt.ylabel(variable_name)
    plt.title(f'{variable_name} vs Time')
    
    # Adjust limits to create smooth movement
    if len(time_data) > 0:
        plt.xlim(max(0, time_data[-1] - 30), max(30, time_data[-1] + 2))
    
    plt.pause(0.1)  # Add small pause to allow plot to update

def create_real_time_plot_v2(timestamps, voltage_data, current_data, power_data, power_factor_data, window_size=30):
    """
    Creates a real-time plot with 4 subplots that updates with new data.
    """
    if not hasattr(create_real_time_plot_v2, "fig"):
        create_real_time_plot_v2.fig = plt.figure(figsize=(12, 8))
        plt.ion()
    else:
        plt.clf()
    
    # Only show the last window_size points
    if len(timestamps) > window_size:
        time_data = timestamps[-window_size:]
        voltage = voltage_data[-window_size:]
        current = current_data[-window_size:]
        power = power_data[-window_size:]
        pf = power_factor_data[-window_size:]
    else:
        time_data = timestamps
        voltage = voltage_data
        current = current_data
        power = power_data
        pf = power_factor_data

    # Voltage subplot (221)
    plt.subplot(221)
    plt.plot(time_data, voltage, 'b-', label='Voltage')
    plt.grid(True)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')
    plt.title('Voltage vs Time')
    if len(time_data) > 0:
        plt.xlim(max(0, time_data[-1] - 30), max(30, time_data[-1] + 2))
    plt.legend()

    # Current subplot (222)
    plt.subplot(222)
    plt.plot(time_data, current, 'r-', label='Current')
    plt.grid(True)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Current (A)')
    plt.title('Current vs Time')
    if len(time_data) > 0:
        plt.xlim(max(0, time_data[-1] - 30), max(30, time_data[-1] + 2))
    plt.legend()

    # Power subplot (223)
    plt.subplot(223)
    plt.plot(time_data, power, 'g-', label='Power')
    plt.grid(True)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Power (W)')
    plt.title('Power vs Time')
    if len(time_data) > 0:
        plt.xlim(max(0, time_data[-1] - 30), max(30, time_data[-1] + 2))
    plt.legend()

    # Power Factor subplot (224)
    plt.subplot(224)
    plt.plot(time_data, pf, 'y-', label='Power Factor')
    plt.grid(True)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Power Factor')
    plt.title('Power Factor vs Time')
    if len(time_data) > 0:
        plt.xlim(max(0, time_data[-1] - 30), max(30, time_data[-1] + 2))
        plt.ylim(-1, 1)  # Power factor range
    plt.legend()

    plt.tight_layout()
    create_real_time_plot_v2.fig.canvas.draw()
    plt.pause(0.1)