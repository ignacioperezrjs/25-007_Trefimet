import minimalmodbus
import serial
import time
import struct


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

