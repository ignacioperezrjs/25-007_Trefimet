# Usamos Ubuntu 22.04 como base
FROM ubuntu:22.04

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    libglu1-mesa \
    freeglut3-dev \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Instalar GMSH
RUN wget https://gmsh.info/bin/Linux/gmsh-4.13.1-Linux64.tgz -O /tmp/gmsh.tgz && \
    tar -xzf /tmp/gmsh.tgz -C /usr/local/ && \
    ln -s /usr/local/gmsh-4.13.1-Linux64/bin/gmsh /usr/local/bin/gmsh

# Copiar e instalar GetDP desde el archivo .tgz local
COPY Simulacion_Stout/getdp-3.5.0-Linux64c.tgz /tmp/getdp.tgz
RUN tar -xzf /tmp/getdp.tgz -C /usr/local/ && \
    ln -s /usr/local/getdp-3.5.0-Linux64/bin/getdp /usr/local/bin/getdp && \
    rm /tmp/getdp.tgz

# Verificar instalaciones
RUN gmsh --version && getdp --version || echo "Continuando..."

# Copiar todos los archivos de simulación al directorio /app
COPY . /app
WORKDIR /app

# Dar permisos de ejecución
RUN chmod +x Simulacion_Stout/run_getdp.sh Simulacion_Stout/extract.py

# Comando por defecto
CMD ["./run_getdp.sh"]