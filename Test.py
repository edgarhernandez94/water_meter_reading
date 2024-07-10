import cv2
import easyocr
from matplotlib import pyplot as plt

def detect_water_meter_value(image_path):
    # Leer la imagen
    image = cv2.imread(image_path)
    
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Recortar la región de interés (ROI) que contiene los números en la parte roja
    x_start, x_end = 150, 230
    y_start, y_end = 90, 110
    roi = gray[y_start:y_end, x_start:x_end]
    
    # Aplicar un filtro Gaussiano para reducir el ruido
    roi = cv2.GaussianBlur(roi, (9, 9), 0)
    
    # Aplicar umbralización adaptativa para mejorar el contraste
    thresh = cv2.adaptiveThreshold(
        roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Aplicar morfología para limpiar la imagen
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Crear un lector de EasyOCR
    reader = easyocr.Reader(['en'])
    
    # Usar EasyOCR para realizar OCR en la imagen
    result = reader.readtext(thresh, detail=0)
    
    # Extraer y limpiar el texto detectado
    text = ''.join(result)
    value = ''.join(filter(str.isdigit, text))
    
    if value:
        if len(value) > 2:
            return f"El valor del medidor de agua es: {value[:2]}.{value[2:]} m³"
        elif len(value) == 2:
            return f"El valor del medidor de agua es: {value[0]}.{value[1]} m³"
        else:
            return f"El valor del medidor de agua es: {value} m³"
    else:
        return "No se pudo detectar el valor del medidor de agua."

# Ruta a la imagen del medidor de agua
image_path = 'C:/Users/ATR/Desktop/Water_meter/Dataset/captured_image_20240710_165955.jpg'  # Ajusta la ruta de la imagen

# Detectar el valor del medidor de agua
resultado = detect_water_meter_value(image_path)
print(resultado)

# Mostrar la imagen procesada
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
roi = gray[75:95, 165:215]
thresh = cv2.adaptiveThreshold(
    roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
plt.imshow(thresh, cmap='gray')
plt.title('ROI del Medidor de Agua Procesado (Parte Roja Ajustada)')
plt.show()
