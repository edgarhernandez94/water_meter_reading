import cv2
import easyocr
from matplotlib import pyplot as plt

def detect_water_meter_value(image_path):
    # Leer la imagen
    image = cv2.imread(image_path)
    
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Recortar la región de interés (ROI) que contiene los números
    x_start, x_end = 280, 390
    y_start, y_end = 250, 320
    roi = gray[y_start:y_end, x_start:x_end]
    
    # Aplicar un filtro Gaussiano para reducir el ruido
    roi = cv2.GaussianBlur(roi, (5, 5), 0)
    
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
image_path = 'C:/Users/edgar/OneDrive/Escritorio/water_meter_reading/images.jpg'  # Ajusta la ruta de la imagen

# Detectar el valor del medidor de agua
resultado = detect_water_meter_value(image_path)
print(resultado)

# Mostrar la imagen procesada (opcional)
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
roi = gray[250:320, 280:380]  # Ajusta estos valores según sea necesario
thresh = cv2.adaptiveThreshold(
    roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
plt.imshow(thresh, cmap='gray')
plt.title('ROI del Medidor de Agua Procesado')
plt.show()



##########################################################################################
# Se necesita crear dataset de imagenes para probar
# Se necesita homogenizar y generar el dispositivo para poder estar tomando fotos constantemente y visualizarlas en plataforma web.
