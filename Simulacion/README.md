# STOUT_SIMULATION  
Repositorio de simulaciones magneto-térmicas para el proyecto bobina-barra.  

## Descripción  
Este proyecto contiene los archivos necesarios para realizar simulaciones magneto-térmicas utilizando GetDP y GMSH. Las simulaciones modelan la interacción electromagnética entre una bobina y una barra para diferentes frecuencias y configuraciones.  Para crear el archivo .msh, ir al Readme.txt dentro de la carpeta de simulación.

## Docker (Contenedor)  
### Requisitos  
- Docker Desktop instalado en el sistema  
- Se puede ejecutar por consola o por la terminal de VSCode  

### Estructura del contenedor  
El contenedor está basado en Ubuntu 22.04 con:  
- GMSH 4.13.1  
- GetDP 3.5.0  
- Python 3  
- Dependencias necesarias (cmake, libopenblas-dev, etc.)  

### Instrucciones para ejecución  
1. **Detener contenedores previos** (opcional):  
    ```bash  
    docker stop $(docker ps -aq) 2>/dev/null  
    ```  

2. **Construir la imagen**:  
    ```bash  
    docker build -t getdp-container .  
    ```  

3. **Verificar imagen creada**:  
    ```bash  
    docker images | grep getdp-container  
    ```  

4. **Ejecutar contenedor**:  
    ```bash  
    docker run -it --rm getdp-container  
    ```  

5. **Dentro del contenedor**:  
    ```bash  
    ls  
    cd Simulacion_Stout/  
    ls  
    ```  

6. **Preparar y ejecutar simulación**:  
    ```bash  
    sed -i 's/\r$//' run_getdp.sh  
    cat -v run_getdp.sh  
    ./run_getdp.sh  
    ```  

## Estructura de archivos  
    .  
    ├── Dockerfile  
    ├── README.md  
    └── Simulacion_Stout  
        ├── extract.py  
        ├── getdp-3.5.0-Linux64c.tgz  
        ├── getdp  
        ├── magneto_thermal.geo  
        ├── magneto_thermal.msh  
        ├── magneto_thermal_1.pro  
        ├── magneto_thermal_2.pro  
        ├── magneto_thermal_3.pro  
        ├── magneto_thermal_4.pro  
        ├── readme.txt  
        └── run_getdp.sh  

## Notas  
- Ejecutar comandos con permisos de administrador cuando sea necesario  
- Los tiempos/fechas en ejemplos son ilustrativos  
- Recomendado mínimo 4GB RAM para simulaciones  
