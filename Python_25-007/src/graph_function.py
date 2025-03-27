import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from typing import List
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

def create_real_time_plot_v2(timestamps, voltage, current, power, power_factor):
    """Real-time plotting of sensor measurements"""
    # Initialize the plot on first call
    if not hasattr(create_real_time_plot_v2, 'initialized'):
        create_real_time_plot_v2.initialized = True
        create_real_time_plot_v2.fig, create_real_time_plot_v2.axs = plt.subplots(2, 2, figsize=(12, 8))
        plt.ion()
    
    # Clear all subplots
    for ax in create_real_time_plot_v2.axs.flat:
        ax.clear()
    
    # Get axes references
    ((ax1, ax2), (ax3, ax4)) = create_real_time_plot_v2.axs
    
    # Plot data
    ax1.plot(timestamps, voltage, 'b-')
    ax1.set_title('Voltaje vs Tiempo')
    ax1.set_ylabel('Voltaje (V)')
    ax1.grid(True)
    
    ax2.plot(timestamps, current, 'r-')
    ax2.set_title('Corriente vs Tiempo')
    ax2.set_ylabel('Corriente (A)')
    ax2.grid(True)
    
    ax3.plot(timestamps, power, 'g-')
    ax3.set_title('Potencia vs Tiempo')
    ax3.set_ylabel('Potencia (W)')
    ax3.grid(True)
    
    ax4.plot(timestamps, power_factor, 'm-')
    ax4.set_title('Factor de Potencia vs Tiempo')
    ax4.set_ylabel('Factor de Potencia')
    ax4.set_ylim(-1.1, 1.1)
    ax4.grid(True)
    
    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)

def save_measurement_plots(directory: str, timestamps: list, measurements: dict, start_time_str: str):
    """Save measurement plots to files"""
    plt.ioff()  # Turn off interactive mode
    
    plot_configs = [
        ('voltage', measurements['voltage_f1'], 'Voltaje vs Tiempo', 'Voltaje (V)', 'b'),
        ('current', measurements['current_f1'], 'Corriente vs Tiempo', 'Corriente (A)', 'r'),
        ('power_factor', measurements['power_factor_f1'], 'Factor de Potencia vs Tiempo', 'Factor de Potencia', 'm'),
    ]

    for name, data, title, ylabel, color in plot_configs:
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, data, f'{color}-')
            plt.grid(True)
            plt.xlabel('Tiempo (segundos)')
            plt.ylabel(ylabel)
            plt.title(title)
            if name == 'power_factor':
                plt.ylim(-1.1, 1.1)
            plt.savefig(os.path.join(directory, f"{name}_plot_{start_time_str}.png"))
            plt.close()
        except Exception as e:
            print(f"No se pudo guardar el gráfico {name}: {e}")
            plt.close()

    # Try to save power plot separately
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, measurements['active_power_f1'], 'g-', label='Potencia Activa (W)')
        plt.plot(timestamps, measurements['reactive_power_f1'], 'y-', label='Potencia Reactiva (VAr)')
        plt.grid(True)
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Potencia')
        plt.title('Potencias Activa y Reactiva vs Tiempo')
        plt.legend()
        plt.savefig(os.path.join(directory, f"power_PandQ_{start_time_str}.png"))
        plt.close()
    except Exception as e:
        print(f"No se pudo guardar el gráfico de potencias: {e}")
        plt.close()