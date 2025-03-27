import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from src.sensor_class import SDM630Sensor
from src.graph_function import create_real_time_plot_v2

def get_save_location():
    while True:
        test_or_result = input("¿Es esto un test o un resultado? (T/R): ").upper()
        if test_or_result in ['T', 'R']:
            base_folder = 'tests' if test_or_result == 'T' else 'results'
            measurement_name = input("Nombre de la medición: ")
            return base_folder, measurement_name
        print("Por favor, ingrese 'T' para test o 'R' para resultado.")

def main():
    # Initialize timestamp and create directory
    start_time = time.time()
    start_time_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        # Initialize sensor
        sensor = SDM630Sensor('COM5')
        
        # Get save location
        base_folder, measurement_name = get_save_location()
        directory = os.path.join(base_folder, measurement_name, start_time_str)
        os.makedirs(directory, exist_ok=True)
        print(f"\nGuardando datos en: {directory}\n")

        # Main measurement loop
        plt.ion()  # Turn on interactive mode
        while True:
            try:
                # Get measurements and store them
                measurements = sensor.read_all_registers()
                if measurements:  # Only store if read was successful
                    current_time = time.time() - start_time
                    sensor.timestamps.append(current_time)
                    
                    # Update real-time plot every 5 measurements
                    if len(sensor.timestamps) % 5 == 0:
                        create_real_time_plot_v2(
                            sensor.timestamps,
                            sensor.measurements['voltage_f1'],
                            sensor.measurements['current_f1'],
                            sensor.measurements['active_power_f1'],
                            sensor.measurements['power_factor_f1']
                        )
                    
                    if len(sensor.timestamps) % 50 == 0:
                        print(f"Mediciones tomadas: {len(sensor.timestamps)}")
                    
            except Exception as e:
                print(f"Error en lectura: {e}")
            
            time.sleep(0.04)  # 25Hz sampling rate

    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario. Guardando datos...")
        try:
            plt.ioff()  # Turn off interactive mode
            
            # Create DataFrame
            df = pd.DataFrame({
                'Tiempo_relativo': sensor.timestamps,
                'Voltage_F1': sensor.measurements['voltage_f1'],
                'Corriente_F1': sensor.measurements['current_f1'],
                'Potencia_Activa_F1': sensor.measurements['active_power_f1'],
                'Potencia_Reactiva_F1': sensor.measurements['reactive_power_f1'],
                'Factor_Potencia_F1': sensor.measurements['power_factor_f1'],
                'THD_Current_F1': sensor.measurements['thd_current_f1'],
                'THD_Voltage_F1': sensor.measurements['thd_voltage_f1'],
                'Corriente_Maxima_F1': sensor.measurements['max_current_f1'],
                'Frecuencia': sensor.measurements['frequency']
            })
            
            # Save Excel file
            excel_filename = os.path.join(directory, f"values_{start_time_str}.xlsx")
            df.to_excel(excel_filename, index=False, sheet_name='Mediciones')
            print(f"Datos guardados en {excel_filename}")

            # Try to save plots
            try:
                for column in df.columns[1:]:  # Skip time column
                    plt.figure(figsize=(10, 6))
                    plt.plot(df['Tiempo_relativo'], df[column])
                    plt.title(f'{column} vs Tiempo')
                    plt.xlabel('Tiempo (segundos)')
                    plt.grid(True)
                    plt.savefig(os.path.join(directory, f"{column}_{start_time_str}.png"))
                    plt.close()
            except Exception as plot_error:
                print(f"Error al guardar gráficos: {plot_error}")

        except Exception as e:
            print(f"Error al guardar datos: {e}")
        
        finally:
            plt.close('all')
            print("Programa finalizado.")

if __name__ == "__main__":
    main()