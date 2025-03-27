import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import minimalmodbus
import pandas as pd
# Replace these lines:
from src.graph_function import create_real_time_plot_v2 #, create_real_time_plot
from src.read_variables import sdm630_modbus_to_float
import matplotlib.pyplot as plt
from datetime import datetime
import time
from src.read_variables import sdm630_modbus_to_float
import os

import serial
print(serial.__version__)  # Debe mostrar "3.5"
print(serial.Serial)       # Debe mostrar <class 'serial.Serial'>)

# Configurar el puerto serie y el dispositivo Modbus
instrument = minimalmodbus.Instrument('COM5', 1)  # Puerto COM5 y esclavo Modbus 1
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 2  # Tiempo de espera en segundos
base_address = 0  # Dirección base para lectura de registros (30001 en documentación Modbus = 0 en minimalmodbus)
register_address = 0  # 30001 en documentación Modbus = 0 en minimalmodbus

def get_save_location():
    while True:
        test_or_result = input("¿Es esto un test o un resultado? (T/R): ").upper()
        if test_or_result in ['T', 'R']:
            break
        print("Por favor, ingrese 'T' para test o 'R' para resultado.")
    
    while True:
        name = input("Ingrese un nombre corto para identificar esta medición: ")
        if len(name) > 0 and len(name) <= 20 and all(c.isalnum() or c in '_-' for c in name):
            break
        print("Por favor, use un nombre corto (máximo 20 caracteres) usando solo letras, números, guiones o guiones bajos.")
    
    base_folder = "tests" if test_or_result == 'T' else "results"
    return base_folder, name

# Get save location information before starting measurements
base_folder, measurement_name = get_save_location()
print(f"\nGuardando datos en carpeta: {base_folder}/{measurement_name}\n")

# Initialize lists to store data
timestamps = []
voltages = []
currents = []
active_powers = []
reactive_powers = []
power_factors = []
thd_currents = []
max_currents = []
frequencies = []
thd_voltages = []  # Add this new list
# Start time for relative timestamps
start_time = time.time()  


try:
    # Create a timestamp string for the filename
    start_time_str = datetime.fromtimestamp(start_time).strftime('%Y%m%d_%H%M%S')
    print("Leyendo datos... Presiona CTRL + C para detener el programa.")
    
    # Create empty lists to store data for Excel
    data = {
        'Tiempo_relativo': timestamps,
        'Voltage_F1': voltages,
        'Corriente_F1': currents,
        'Potencia_Activa_F1': active_powers,
        'Potencia_Reactiva_F1': reactive_powers,
        'Factor_Potencia_F1': power_factors,  # Make sure this is included
        'THD_Current_F1': thd_currents,
        'THD_Voltage_F1': thd_voltages,
        'Corriente_Maxima_F1': max_currents,
        'Frecuencia': frequencies
    }
    while True:
        try:
            # Calculate relative timestamp
            relative_time = time.time() - start_time
            
            # Leer la tensión de fase 1
            # Direccion_V = 0*1 # Dirección de la tensión de fase 1 L-N (Input Register 30001)
            Direccion_V = 1*2-2
            raw_valueV1 = instrument.read_register(Direccion_V, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_decV1 = instrument.read_register(Direccion_V + 1, number_of_decimals=0, functioncode=4, signed=False)
            VoltageF1 = sdm630_modbus_to_float(raw_valueV1, raw_value_decV1)

            # Leer la corriente de fase 1
            direccion_I = 2*4-2  # Dirección de la corriente de fase 1 (Input Register 30004)
            raw_valueI1 = instrument.read_register(direccion_I, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_decI1 = instrument.read_register(direccion_I +1, number_of_decimals=0, functioncode=4, signed=False)
            CurrentF1 = sdm630_modbus_to_float(raw_valueI1, raw_value_decI1)

            # Leer la potencia activa de fase 1
            direcciónP1 = 2*7-2  # Dirección de la potencia de fase 1 (Input Register 30013)
            raw_valueP1 = instrument.read_register(direcciónP1, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_decP1 = instrument.read_register(direcciónP1 + 1, number_of_decimals=0, functioncode=4, signed=False)
            APowerF1 = sdm630_modbus_to_float(raw_valueP1, raw_value_decP1)

            # Leer la potencia reactiva de fase 1 (13)
            direcciónQ1 = 2*13-2  # Dirección de la potencia reactiva de linea 1 (Input Register 30025)
            raw_valueQ1 = instrument.read_register(direcciónQ1, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_decQ1 = instrument.read_register(direcciónQ1 + 1, number_of_decimals=0, functioncode=4, signed=False)
            QPowerF1 = sdm630_modbus_to_float(raw_valueQ1, raw_value_decQ1)
            # Leer el factor de potencia (16)
            Direccion_PF = 2*16-2  # Dirección del factor de potencia (Input Register 30031)
            raw_value_PF = instrument.read_register(Direccion_PF, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_PF_dec = instrument.read_register(Direccion_PF + 1, number_of_decimals=0, functioncode=4, signed=False)
            PowerFactor = sdm630_modbus_to_float(raw_value_PF, raw_value_PF_dec)

            # Add frequency reading in your main loop (after other readings)
            # Leer la frecuencia (36)
            Direccion_F = 2*36-2  # Dirección de la frecuencia (Input Register 30071)
            raw_valueF = instrument.read_register(Direccion_F, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_decF = instrument.read_register(Direccion_F + 1, number_of_decimals=0, functioncode=4, signed=False)
            Frequency = sdm630_modbus_to_float(raw_valueF, raw_value_decF)

           # Leer el THD de la corriente de fase 1
            Direccion_THD_I_F1 = 2*121-2  # Dirección del THD de la corriente de fase 1 (Input Register 30241)
            raw_value_THD_I_F1 = instrument.read_register(Direccion_THD_I_F1, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_THD_I_F1_dec = instrument.read_register(Direccion_THD_I_F1 + 1, number_of_decimals=0, functioncode=4, signed=False)
            THD_CurrentF1 = sdm630_modbus_to_float(raw_value_THD_I_F1, raw_value_THD_I_F1_dec)
            print(f"THD_CurrentF1 leído: {THD_CurrentF1:.2f} %")

            # Leer el THD del voltaje de fase 1
            Direccion_THD_V_F1 = 2*118-2  # Dirección del THD del voltaje de fase 1 (Input Register 30235)
            raw_value_THD_V_F1 = instrument.read_register(Direccion_THD_V_F1, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_THD_V_F1_dec = instrument.read_register(Direccion_THD_V_F1 + 1, number_of_decimals=0, functioncode=4, signed=False)
            THD_VoltageF1 = sdm630_modbus_to_float(raw_value_THD_V_F1, raw_value_THD_V_F1_dec)
            print(f"THD_VoltageF1 leído: {THD_VoltageF1:.2f} %")

            # Máxima corriente por la fase 1 (133)
            Direccion_maxI_F1 = 2*133-2  # Dirección de la potencia reactiva de linea 1 (Input Register 30265)
            raw_value_maxI = instrument.read_register(Direccion_maxI_F1, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_maxI_dec = instrument.read_register(Direccion_maxI_F1 + 1, number_of_decimals=0, functioncode=4, signed=False)
            max_IF1 = sdm630_modbus_to_float(raw_value_maxI, raw_value_maxI_dec)
            
            # Append values to lists
            timestamps.append(relative_time)
            voltages.append(VoltageF1)
            currents.append(CurrentF1)
            active_powers.append(APowerF1)
            reactive_powers.append(QPowerF1)
            thd_currents.append(THD_CurrentF1)
            power_factors.append(PowerFactor)
            thd_voltages.append(THD_VoltageF1)  # Add this line
            max_currents.append(max_IF1)
            frequencies.append(Frequency)
                    
            print(f"""
    ╔════════════════════════════════════════════
    ║ Tiempo relativo {relative_time:8.2f}
    ║ Fase 1 Voltage (L-N): {VoltageF1:8.2f} V         
    ║ Fase 1 Corriente instantánea: {CurrentF1:8.2f} A                             
    ║ Fase 1 Potencia Activa: {APowerF1:8.2f} W                              
    ║ Fase 1 Potencia reactiva: {QPowerF1:8.2f} VAR
    ║ Fase 1 THD Current: {THD_CurrentF1:8.2f} %
    ║ Fase 1 THD Voltage: {THD_VoltageF1:8.2f} %
    ║ Fase 1 Corriente máxima registrada: {max_IF1:8.2f} A
    ║ Frecuencia: {Frequency:8.2f} Hz
    ║ Fase 1 Factor de Potencia: {PowerFactor:8.3f}
    ╚════════════════════════════════════════════
            """)

            create_real_time_plot_v2(
                timestamps,
                voltages,
                currents,
                active_powers,
                power_factors  # Cambiado de thd_currents a power_factors
            )

            #create_real_time_plot(timestamps, currents, "Current (A)")
            #create_real_time_plot(timestamps, thd_currents, "THD Current (%)")

        except Exception as e:
            print(f"Error al leer: {e}")
        
        time.sleep(0.2)  # Espera 0.2 segundos antes de leer de nuevo

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario. Guardando datos...")
    try:
        # Primero cerramos todas las figuras de matplotlib
        plt.ioff()
        plt.close('all')

        # Create directory structure with timestamp
        directory = os.path.join(base_folder, measurement_name, start_time_str)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Crear el DataFrame con los datos recolectados
        df = pd.DataFrame({
            'Tiempo_relativo': timestamps,
            'Voltage_F1': voltages,
            'Corriente_F1': currents,
            'Potencia_Activa_F1': active_powers,
            'Potencia_Reactiva_F1': reactive_powers,
            'Factor_Potencia_F1': power_factors,
            'THD_Current_F1': thd_currents,
            'THD_Voltage_F1': thd_voltages,
            'Corriente_Maxima_F1': max_currents,
            'Frecuencia': frequencies
        })

        # Guardar Excel
        excel_filename = os.path.join(directory, f"values_{start_time_str}.xlsx")
        df.to_excel(excel_filename, index=False, sheet_name='Mediciones')
        print(f"Datos guardados en {excel_filename}")

        # Guardar gráficos uno por uno
        print("Guardando gráficos...")
        
        # Voltage plot
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, voltages, 'b-', label='Voltage')
        plt.grid(True)
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Voltaje (V)')
        plt.title('Voltaje vs Tiempo')
        plt.legend()
        plt.savefig(os.path.join(directory, f"voltage_plot_{start_time_str}.png"))
        plt.close()

        # Current plot
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, currents, 'r-', label='Current')
        plt.grid(True)
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Corriente (A)')
        plt.title('Corriente vs Tiempo')
        plt.legend()
        plt.savefig(os.path.join(directory, f"current_plot_{start_time_str}.png"))
        plt.close()

        # Power Factor plot
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, power_factors, 'm-', label='Factor de Potencia')
        plt.grid(True)
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Factor de Potencia')
        plt.title('Factor de Potencia vs Tiempo')
        plt.ylim(-1, 1)
        plt.legend()
        plt.savefig(os.path.join(directory, f"power_factor_{start_time_str}.png"))
        plt.close()

        # Combined Power plot
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, active_powers, 'g-', label='Potencia Activa (W)')
        plt.plot(timestamps, reactive_powers, 'y-', label='Potencia Reactiva (VAr)')
        plt.grid(True)
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Potencia')
        plt.title('Potencias Activa y Reactiva vs Tiempo')
        plt.legend()
        plt.savefig(os.path.join(directory, f"power_PandQ_{start_time_str}.png"))
        plt.close()

        print(f"Gráficos guardados en la carpeta {directory}")

    except Exception as e:
        print(f"Error al guardar los datos: {e}")
    
    finally:
        plt.close('all')
        print("Programa finalizado.")