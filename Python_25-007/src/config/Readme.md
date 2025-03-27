# Sensor Configuration System

This directory contains the configuration system for managing sensor settings and register mappings.

## Structure

```
config/
├── __init__.py
├── main.py           # Main script to create sensor configurations
├── sensor_config.py  # SensorConfig class implementation
└── Sensor_json/      # Directory for storing sensor JSON files
```

## Class Overview: SensorConfig

The `SensorConfig` class handles creation and management of sensor configuration files.

### Features
- Creates standardized JSON configuration files
- Manages Modbus settings
- Maps sensor registers
- Handles file creation and overwriting

### Configuration Structure
```json
{
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
```

## Usage

1. Create a new sensor configuration:
```powershell
cd c:\Users\ignac\projects\25-007_Trefimet\Python_25-007
python config\main.py --overwrite
```

2. Options:
   - `--folder`: Specify base folder for configurations (default: 'config')
   - `--overwrite`: Force overwrite existing configuration files

## Example: SDM630 Configuration

The system comes pre-configured for SDM630 power meter with:
- Voltage, current, and power measurements
- THD measurements
- Frequency monitoring
- Maximum values tracking

## Adding New Sensors

To add a new sensor type:
1. Create a new function in `main.py` similar to `create_sdm630_config()`
2. Define register mappings
3. Use `SensorConfig` class to generate configuration

## File Locations

Generated JSON files are stored in the `Sensor_json` directory with the format:
`{sensor_name}.json`