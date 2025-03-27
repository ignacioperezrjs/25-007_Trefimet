import os
import argparse
from sensor_config import SensorConfig  # Changed import statement

def create_sdm630_config(sensor_folder: str, overwrite: bool = False) -> None:
    """Create SDM630 sensor configuration"""
    config = SensorConfig()
    
    # Set basic device information
    config.set_device_info(
        device_type="SDM630-Modbus v2",
        slave_id=1
    )
    
    # Add registers - Format: name: (register_number * 2 - 2)
    registers = {
        # Phase 1 Measurements
        "voltage_f1": 0,              # 30001: Voltage Phase 1
        "current_f1": 6,             # 30004: Current Phase 1
        "active_power_f1": 12,       # 30007: Active Power Phase 1
        "reactive_power_f1": 24,     # 30013: Reactive Power Phase 1
        "power_factor_f1": 30,       # 30016: Power Factor Phase 1
        
        # System Measurements
        "frequency": 70,             # 30036: Frequency
        
        # THD Measurements
        "thd_voltage_f1": 234,       # 30118: THD Voltage Phase 1
        "thd_current_f1": 240,       # 30121: THD Current Phase 1
        
        # Maximum Values
        "max_current_f1": 264,       # 30133: Maximum Current Phase 1
        
        # Additional registers can be added following the same pattern
        # Register calculation: (register_number * 2 - 2)
    }
    
    for name, address in registers.items():
        config.add_register(name, address)
    
    try:
        # Ensure we're saving in the Sensor_json directory
        sensor_json_path = os.path.join(sensor_folder, "Sensor_json")
        os.makedirs(sensor_json_path, exist_ok=True)
        
        filepath = config.save_config(
            sensor_folder=sensor_json_path,
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
    parser.add_argument('--folder', type=str, default='config',
                        help='Base folder for configurations')
    parser.add_argument('--overwrite', action='store_true',
                        help='Overwrite existing configuration files')
    
    args = parser.parse_args()
    
    # Base folder will be 'config'
    base_folder = os.path.join(os.path.dirname(__file__), args.folder)
    create_sdm630_config(base_folder, args.overwrite)