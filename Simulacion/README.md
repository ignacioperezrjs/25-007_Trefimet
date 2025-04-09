# Autor: Ignacio Pérez

## Entendiendo Contenedores de Docker usando la imagen de Ubuntu 22.04
https://medium.com/@andrewdass/make-your-own-dockerfile-to-run-an-ubuntu-container-015c58beb869

Crear la imagen en la terminal con cd en: Simulacion_Stout_Wolke. **Leer el artículo de medium para entende rmás sobre imágenes.**.

1. ╰─ docker build -t img_lanza
A continuación, se crea el contenedor a partir de la imagen.
2. docker run -it --name=cont_sim_lanza img_lanza /bin/bash
Se debería ver algo como: root@43d8aa05caba:/app# 

## Simulacion_Stout_Wolke
Repositorio con los archivos necesarios para genera una simulación en GETDP de un acoplamiento bobina-lanza
