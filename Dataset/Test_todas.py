import cv2
import pytesseract
import os
import matplotlib.pyplot as plt

# Configuración de Tesseract para enfocarse en la detección de números
custom_config_digits = r'--oem 3 --psm 6 outputbase digits'

# Directorio de las imágenes
image_directory = 'Dataset'

# Obtener todas las rutas de las imágenes en el directorio
image_paths = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(('.jpg', '.png'))]

# Coordenadas de la ROI que incluye los tres dígitos
roi_coords_full = (185, 70, 50, 25)  # Ajustar según sea necesario para incluir los tres dígitos

# Función para ajustar el brillo y el contraste
def adjust_brightness_contrast(image, brightness=0, contrast=0):
    brightness = int((brightness - 0) * (255 - 0) / (255 - 0) + 0)
    contrast = int((contrast - (-127)) * (255 - 0) / (127 - (-127)) + 0)

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)

    return image

# Procesar todas las imágenes en la lista
results = []
for image_path in sorted(image_paths):
    new_image = cv2.imread(image_path)
    
    # Extraer la ROI completa
    x, y, w, h = roi_coords_full
    roi_full = new_image[y:y+h, x:x+w]
    
    # Ajustar brillo y contraste en la ROI
    roi_bc_full = adjust_brightness_contrast(roi_full, brightness=30, contrast=50)
    
    # Convertir la ROI completa a escala de grises
    roi_gray_full = cv2.cvtColor(roi_bc_full, cv2.COLOR_BGR2GRAY)
    
    # Usar Tesseract para leer los números de la ROI completa sin preprocesamiento
    extracted_digits_full = pytesseract.image_to_string(roi_gray_full, config=custom_config_digits).strip()
    
    # Verificar si el valor extraído es un número y agregarlo a los resultados
    if extracted_digits_full.isdigit():
        results.append((os.path.basename(image_path), int(extracted_digits_full)))

# Ordenar los resultados por timestamp
results = sorted(results, key=lambda x: x[0])

# Filtrar los resultados que no cumplen con las condiciones
filtered_results = []
for i in range(len(results) - 1):
    if results[i][1] <= results[i + 1][1]:
        filtered_results.append(results[i])

# Agregar el último elemento si cumple con la condición
if len(results) > 1 and results[-2][1] <= results[-1][1]:
    filtered_results.append(results[-1])

# Separar los nombres de archivos y los valores para graficar
timestamps, values = zip(*filtered_results)

# Graficar los resultados
plt.figure(figsize=(10, 5))
plt.plot(timestamps, values, marker='o')
plt.xticks(rotation=90)
plt.xlabel('Timestamp')
plt.ylabel('Valor')
plt.title('Resultados OCR de Imágenes en Dataset')
plt.grid(True)
plt.tight_layout()
plt.show()

# Imprimir los resultados
for filename, digits in filtered_results:
    print(f"Números extraídos de {filename}: {digits}")
