import minimalmodbus
import serial
import time
import struct

from typing import Dict, List
import numpy as np

def validate_measurements(timestamps: List[float], measurements: Dict[str, List[float]]) -> bool:
    """
    Validate measurement data and print diagnostics
    Returns True if data is valid, False otherwise
    """
    print("\n=== Data Validation Report ===")
    
    # Check if we have any data
    if not timestamps:
        print("Error: No timestamp data collected")
        return False
    
    timestamp_len = len(timestamps)
    print(f"Number of timestamps: {timestamp_len}")
    
    # Check each measurement array
    valid = True
    for name, values in measurements.items():
        if not values:
            print(f"Error: No data for {name}")
            valid = False
            continue
            

def sdm630_modbus_to_float(register_high, register_low):
    """
    Conversión directa para SDM630 (Modbus RTU) - ¡Probado y funcionando!
    Parámetros:
    - register_high: Primer registro recibido (ej. 17256)
    - register_low: Segundo registro recibido (ej. -29756)
    Retorna:
    - Valor flotante interpretado correctamente
    """
    # SDM630 usa formato: High Word + Low Word (big endian)
    # Convertimos cada registro a 2 bytes (big endian)
    bytes_high = (register_high & 0xFFFF).to_bytes(2, 'big')
    bytes_low = (register_low & 0xFFFF).to_bytes(2, 'big')

    # Combinamos los bytes (High Word primero)
    combined_bytes = bytes_high + bytes_low

    # Interpretamos como float de 32 bits (big endian)
    [float_value] = struct.unpack('>f', combined_bytes)

    return float_value

