# Proyecto_IRB

## Descripción general

Este repositorio documenta el trabajo realizado en un proyecto interdisciplinario de robótica, donde se desarrolló un sistema autónomo compuesto por un equipo de tres robots capaces de competir en fútbol robótico. El proyecto abarca diseño mecánico, desarrollo electrónico, construcción de placas, programación distribuida, visión por computadora y estrategias colaborativas.

El objetivo es crear un repositorio limpio, modular y reutilizable, facilitando su comprensión y extensión por parte de estudiantes, ayudantes o investigadores en el futuro.

---

## 📂 Estructura del Proyecto

### `/hardware/`
Contiene los elementos físicos del sistema, divididos en dos partes:

- **`mechanical/`**  
  Archivos CAD y STL para la impresión y construcción de los robots.  
  *(Corresponde al antiguo módulo ICM).*

- **`electrical/`**  
  Esquemáticos, planos y archivos de diseño de la PCB utilizada.  
  *(Corresponde al antiguo módulo IEE).*

---

### `/software/`
Contiene todo el código necesario para ejecutar el sistema, dividido en los siguientes submódulos:

- **`base/`**  
  Código central que corre en el servidor (por ejemplo, en un PC):
  - Visualización y procesamiento de imágenes de la cancha.
  - Dirección de cada robot en tiempo real.
  - Servidor de comunicaciones.
  - Simulador básico para pruebas sin hardware físico.

- **`player/`**  
  Código que corre en cada robot individual, implementado en MicroPython. Contiene:
  - Rutinas de control de motores y sensores.
  - Comunicación con el servidor.
  - Lógica local de toma de decisiones.

- **`extras/`**  
  Scripts adicionales, herramientas de depuración o prototipos que fueron útiles durante el desarrollo, pero que no forman parte del pipeline final.

- **`requirements.txt`**  
  Archivo con las dependencias necesarias para correr el sistema desde Python (instalación mediante `pip install -r requirements.txt`).

---

### `/docs/`
Documentación adicional, como:

- Manuales de uso
- Diagramas explicativos
- Actas de reuniones y decisiones técnicas (`/docs/actas`)

---

### `/scripts/`
Scripts automatizados para facilitar tareas como:
- Inicialización de entorno
- Carga de firmware
- Ejecutar simulaciones
- Reiniciar procesos

---

## Dependencias

- Lenguajes utilizados:
  - Python 3.x
  - MicroPython
- Editor recomendado: [Visual Studio Code](https://code.visualstudio.com/download)
- Se recomienda tener instalados:
  - `opencv-python` (para visión)
  - `pygame` o similar (si se usa simulador)
  - `numpy`, `matplotlib`, etc.

---

## Documentación complementaria

- [Documentación oficial de Python](https://docs.python.org/3/)
- [Documentación oficial de MicroPython](https://docs.micropython.org/en/latest/index.html)

---

## Créditos

Proyecto desarrollado por estudiantes de Ingeniería Mecánica, Ingeniería Eléctrica e Ingeniería en Ciencias de la Computación de la Pontificia Universidad Católica de Chile.  
Agradecimientos a los profesores y ayudantes que brindaron apoyo técnico durante el proceso.

---

## Licencia

Este proyecto se encuentra bajo la licencia MIT, salvo que se indique lo contrario en archivos específicos.
