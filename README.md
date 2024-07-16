# Proyecto de Detección y Captura de Imágenes

Este repositorio contiene dos scripts principales que se utilizan para capturar imágenes a través de una conexión serial y procesarlas para detectar números utilizando OCR.

## Estructura del Proyecto

- `image_processing.py`: Script para procesar imágenes y detectar números utilizando OCR.
- `image_capture.py`: Script para capturar imágenes desde un dispositivo serial y guardarlas con un timestamp.

## Requisitos

Para ejecutar los scripts, necesitas tener instaladas las siguientes dependencias:

- `opencv-python`
- `pytesseract`
- `matplotlib`
- `pyserial`

Puedes instalar todas las dependencias utilizando el archivo `requirements.txt`.

## Uso

### Procesamiento de Imágenes

1. Asegúrate de que las imágenes que deseas procesar se encuentren en el directorio `Dataset`.
2. Ejecuta el script `image_processing.py` para procesar las imágenes y extraer los números.
3. Los resultados se mostrarán en una gráfica y se imprimirán en la consola.

### Captura de Imágenes

1. Conecta tu dispositivo serial al puerto correcto.
2. Cambia el valor de `serial_port` en el script `image_capture.py` al puerto correcto (por ejemplo, 'COM10').
3. Ejecuta el script `image_capture.py` para capturar imágenes y guardarlas con un timestamp.

## Ejemplos de Ejecución

### Procesamiento de Imágenes

```bash
python image_processing.py
Captura de Imágenes
bash
Copiar código
python image_capture.py
Notas
Asegúrate de ajustar las coordenadas de la ROI en el script image_processing.py según sea necesario para tu caso específico.
Verifica que el puerto serial y la tasa de baudios sean correctos para tu dispositivo antes de ejecutar image_capture.py.
Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para cualquier mejora o corrección.

Licencia
Este proyecto está bajo la licencia MIT.

arduino
Copiar código

### requirements.txt

```text
opencv-python
pytesseract
matplotlib
pyserial