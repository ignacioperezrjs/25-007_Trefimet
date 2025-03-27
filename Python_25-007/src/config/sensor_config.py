import json
import os
from typing import Dict, Any

class SensorConfig:
    def __init__(self):
        self.base_config = {
            "device_type": "",
            "tested_JSON": "not tested",
            "modbus_settings": {
                "slave_id": 1,
                "baudrate": 9600,
                "bytesize": 8,
                "parity": "N",
                "stopbits": 1,
                "timeout": 2
            },
            "register_settings": {
                "base_address": 0,
                "register_map": {}
            }
        }

    def add_register(self, name: str, address: int, length: int = 2, type: str = "float32") -> None:
        """Add a register to the configuration"""
        self.base_config["register_settings"]["register_map"][name] = {
            "address": address,
            "length": length,
            "type": type
        }

    def set_device_info(self, device_type: str, slave_id: int, **modbus_settings: Dict[str, Any]) -> None:
        """Set basic device information"""
        self.base_config["device_type"] = device_type
        self.base_config["modbus_settings"]["slave_id"] = slave_id
        self.base_config["modbus_settings"].update(modbus_settings)

    def save_config(self, sensor_folder: str, filename: str, overwrite: bool = False) -> str:
        """Save configuration to JSON file"""
        os.makedirs(sensor_folder, exist_ok=True)
        filepath = os.path.join(sensor_folder, f"{filename}.json")
        
        if os.path.exists(filepath) and not overwrite:
            raise FileExistsError(f"Configuration file {filepath} already exists")
            
        with open(filepath, 'w') as f:
            json.dump(self.base_config, f, indent=4, sort_keys=True)  # Fixed: added file object 'f'
        
        return filepath

def create_sdm630_config(sensor_folder: str, overwrite: bool = False) -> None:
    """Create SDM630 sensor configuration"""
    config = SensorConfig()
    
    # Set basic device information
    config.set_device_info(
        device_type="SDM630-Modbus v2",
        slave_id=1
    )
    
    # Add registers
    registers = {
        "voltage_f1": 0,      # 30001
        "current_f1": 6,      # 30007
        "active_power_f1": 12,  # 30013
        "power_factor_f1": 30,  # 30031
        # Add more registers as needed
    }
    
    for name, address in registers.items():
        config.add_register(name, address)
    
    try:
        filepath = config.save_config(
            sensor_folder=sensor_folder,
            filename="SDM630-Modbus_v2",
            overwrite=overwrite
        )
        print(f"Configuration saved successfully at: {filepath}")
    except FileExistsError as e:
        print(f"Error: {e}")
        print("Use --overwrite flag to replace existing file")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create sensor configuration files')
    parser.add_argument('--folder', type=str, default='sensors',
                        help='Folder to store sensor configurations')
    parser.add_argument('--overwrite', action='store_true',
                        help='Overwrite existing configuration files')
    
    args = parser.parse_args()
    
    sensor_folder = os.path.join(os.path.dirname(__file__), args.folder)
    create_sdm630_config(sensor_folder, args.overwrite)