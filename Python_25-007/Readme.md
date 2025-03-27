# Power Meter Data Logger

## Estructura del Proyecto
```
25-007 Trefimet/
├── config/
│   └── sensors/
│       └── sdm630_power_meter.json
├── src/
│   ├── __init__.py
│   ├── sensor_reader.py
│   ├── data_logger.py
│   └── plotter.py
├── tests/
│   ├── __init__.py
│   ├── test_sensor_reader.py
│   ├── test_data_logger.py
│   └── test_plotter.py
├── results/
│   ├── measurements/
│   │   └── {timestamp}/
│   │       ├── data.xlsx
│   │       └── plots/
│   └── tests/
│       └── {timestamp}/
│           ├── test_results.html
│           └── test_data.json
├── main.py
└── README.md
```

## Pruebas
Para ejecutar las pruebas, use:
```bash
python -m pytest tests/ --html=results/tests/$(date +%Y%m%d_%H%M%S)/test_results.html
```

## Estructura de Resultados
- `/results/measurements/`: Contiene las mediciones organizadas por timestamp
- `/results/tests/`: Contiene los resultados de las pruebas unitarias