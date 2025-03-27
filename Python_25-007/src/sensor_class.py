from typing import Dict, Any
import json
import os
import minimalmodbus
import serial
import time
from src.read_variables import sdm630_modbus_to_float

class BaseSensor:
    def __init__(self, config_path: str, com_port: str):
        self.com_port = com_port
        self.config = self._load_config(config_path)
        self.instrument = self._initialize_modbus()
        self.timestamps = []
        self.measurements = {}

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Config file not found at {config_path}")
            raise

    def _initialize_modbus(self) -> minimalmodbus.Instrument:
        try:
            instrument = minimalmodbus.Instrument(
                self.com_port, 
                self.config['modbus_settings']['slave_id']
            )
            
            instrument.serial.baudrate = self.config['modbus_settings']['baudrate']
            instrument.serial.bytesize = self.config['modbus_settings']['bytesize']
            instrument.serial.parity = (
                serial.PARITY_NONE if self.config['modbus_settings']['parity'] == 'N'
                else serial.PARITY_EVEN
            )
            instrument.serial.stopbits = self.config['modbus_settings']['stopbits']
            instrument.serial.timeout = self.config['modbus_settings']['timeout']
            
            return instrument
        except Exception as e:
            print(f"Error initializing Modbus: {e}")
            raise

    def read_register(self, register_name: str) -> float:
        raise NotImplementedError("Subclasses must implement read_register")

    def read_all_registers(self) -> Dict[str, float]:
        raise NotImplementedError("Subclasses must implement read_all_registers")
    

class SDM630Sensor(BaseSensor):
    def __init__(self, com_port: str):
        # Get the absolute path to the config file
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # Go to Python_25-007
            'src',
            'config',
            'Sensor_json',
            'SDM630-Modbus_v2.json'
        )
        
        # Debug print to verify path
        print(f"Looking for config at: {config_path}")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Configuration file not found at: {config_path}\n"
                "Please ensure the JSON file exists in the correct location:\n"
                "Python_25-007/src/config/Sensor_json/SDM630-Modbus_v2.json"
            )
            
        super().__init__(config_path, com_port)

        # Initialize timestamps and measurements with (0.0, 0.0)
        self.timestamps.append(0.0)  # Add 0.0 to timestamps
        for register_name in self.config['register_settings']['register_map'].keys():
            self.measurements[register_name] = [0.0]  # Add 0.0 to each measurement list

    def read_register(self, register_name: str) -> float:
        try:
            register_info = self.config['register_settings']['register_map'][register_name]
            address = register_info['address']
            
            raw_value = self.instrument.read_register(
                address, 
                number_of_decimals=0,
                functioncode=4,
                signed=False
            )
            raw_value_dec = self.instrument.read_register(
                address + 1,
                number_of_decimals=0,
                functioncode=4,
                signed=False
            )
            
            return sdm630_modbus_to_float(raw_value, raw_value_dec)
        except Exception as e:
            print(f"Error reading register {register_name}: {e}")
            raise

    def read_all_registers(self) -> Dict[str, float]:
        """Read all registers and return measurements only if all reads are successful"""
        measurements = {}
        
        try:
            # Read all registers first
            for register_name in self.config['register_settings']['register_map'].keys():
                value = self.read_register(register_name)
                measurements[register_name] = value
                
                # Store in measurements history
                if register_name not in self.measurements:
                    self.measurements[register_name] = []
                self.measurements[register_name].append(value)
                
            return measurements
            
        except Exception as e:
            print(f"Error reading registers: {e}")
            return None