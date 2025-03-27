import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import minimalmodbus
import pandas as pd
from tests.graph_function import create_real_time_plot
import matplotlib.pyplot as plt
from datetime import datetime
import time
from tests.read_variables import sdm630_modbus_to_float

import serial
print(serial.__version__)  # Debe mostrar "3.5"
print(serial.Serial)       # Debe mostrar <class 'serial.Serial'>
print("intento 18:57")

# Configurar el puerto serie y el dispositivo Modbus
instrument = minimalmodbus.Instrument('COM5', 1)  # Puerto COM5 y esclavo Modbus 1
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 2  # Tiempo de espera en segundos
base_address = 0  # Dirección base para lectura de registros (30001 en documentación Modbus = 0 en minimalmodbus)
register_address = 0  # 30001 en documentación Modbus = 0 en minimalmodbus


# Initialize lists to store data
timestamps = []
voltages = []
currents = []
active_powers = []
reactive_powers = []
thd_currents = []
max_currents = []
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
        'THD_Current_F1': thd_currents,
        'Corriente_Maxima_F1': max_currents
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

           # Leer el THD de la corriente de fase 1
            Direccion_THD_I_F1 = 2*121-2  # Dirección del THD de la corriente de fase 1 (Input Register 30241)
            raw_value_THD_I_F1 = instrument.read_register(Direccion_THD_I_F1, number_of_decimals=0, functioncode=4, signed=False)
            raw_value_THD_I_F1_dec = instrument.read_register(Direccion_THD_I_F1 + 1, number_of_decimals=0, functioncode=4, signed=False)
            THD_CurrentF1 = sdm630_modbus_to_float(raw_value_THD_I_F1, raw_value_THD_I_F1_dec)
            print(f"THD_CurrentF1 leído: {THD_CurrentF1:.2f} %")


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
            
            max_currents.append(max_IF1)
            # Imprimir los resultados
            print(f"""
╔════════════════════════════════════════════
║ Tiempo relativo {relative_time:8.2f}
║ Fase 1 Voltage (L-N): {VoltageF1:8.2f} V         
║ Fase 1 Corriente instantánea: {CurrentF1:8.2f} A                             
║ Fase 1 Potencia Activa: {APowerF1:8.2f} W                              
║ Fase 1 Potencia reactiva: {QPowerF1:8.2f} VAR
║ Fase 1 THD Current: {THD_CurrentF1:8.2f} %
║ Fase 1 Corriente máxima registrada: {max_IF1:8.2f} A
╚════════════════════════════════════════════
            """)

            # Add these plotting calls after appending values
            create_real_time_plot(timestamps, voltages, "Voltage (V)")
            #create_real_time_plot(timestamps, currents, "Current (A)")
            #create_real_time_plot(timestamps, thd_currents, "THD Current (%)")

        except Exception as e:
            print(f"Error al leer: {e}")
        
        time.sleep(0.8)  # Espera 1 segundo antes de leer de nuevo

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario. Guardando datos...")
    
    # Create DataFrame and save to Excel
    df = pd.DataFrame(data)
    excel_filename = f"values_{start_time_str}.xlsx"
    df.to_excel(excel_filename, index=False, sheet_name='Mediciones')
    print(f"Datos guardados en {excel_filename}")
    
    plt.ioff()
    plt.close('all')