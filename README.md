# Proyecto_IRB

## Descripción
Este repositorio documenta el trabajo realizado en el proyecto de un equipo de tres robots para competir en fútbol robótico autónomo. Incluye detalles sobre el diseño mecáico, componentes electrónicos, diseño de la placa, comunicación entre robots y avances del proyecto, sirviendo para evaluación y verificación por parte del profesor.

Al traatrse de un proyecto interdisiplinario, este se compone de tres módulos principales, [ICM](https://github.com/LucasZuniga/Proyecto_IRB/tree/main/ICM), [IEE](https://github.com/LucasZuniga/Proyecto_IRB/tree/main/IEE) y [DCC](https://github.com/LucasZuniga/Proyecto_IRB/tree/main/DCC), haciendo referencia a las siglas de los departamentos de Ingeniería Mecánica, Electrica y Computacional respectivamente.

En adicion a los módulos antes mencionados, se encuntra la lista de componentes necesarios para la construcción de los robots, junto con actas de distintas reuniones para el avance del proyecto.

## ICM
En este apartado se encuentran los distintos archivos STL para la impresión y construcción de cada uno de los robots.

## IEE
Respecto al módulo electrico se encuntran el esquemático y plano utilizados en el diseño y construcción de la placa.

## DCC
* Nuestro documento asume familiaridad con los lenguajes de programación Python y MicroPython, en caso contrario consultar la documentación oficial de cada lenguaje  [Documentación Python](https://docs.python.org/3/) y [Documentación MicroPython](https://docs.micropython.org/en/latest/index.html)

### Dependencias
* Recomended code editor: [Visual Studio Code](https://code.visualstudio.com/download)

### Sub-modulos
* [jugador](https://github.com/LucasZuniga/Proyecto_IRB/tree/main/DCC/jugador): Este submódulo es donde se encuentra tanto el codigo principal como las librerias propias para el correcto funcionamiento de cada robot por separado.
* [base](https://github.com/LucasZuniga/Proyecto_IRB/tree/main/DCC/base): En este submódulo se encuentra el codigo que levanta el servidor al cual se conectan los robots, el programa principal encargado visualizar la cancha meidante la camara y dirigir a cada uno de los robots de manera independiente junto con un simulador, el cual puede ser muy útil para el desarrollo de las jugadas.
* [extras](https://github.com/LucasZuniga/Proyecto_IRB/tree/main/DCC/extras): En este submodulo se encuentran codigos útilles pero que no se terminan utilizando en las rutinas finales.