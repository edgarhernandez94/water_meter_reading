import os
import cv2
from PIL import Image
import matplotlib.pyplot as plt

# Ruta a la carpeta de imágenes
data_dir = 'Dataset'

# Obtener todas las imágenes en la carpeta
image_files = [f for f in os.listdir(data_dir) if f.endswith('.jpg') or f.endswith('.png')]

# Ordenar las imágenes por nombre (asumimos que el nombre contiene un timestamp)
image_files.sort()

# Función para preprocesar la imagen y extraer la ROI
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    
    # Verificar si la imagen se cargó correctamente
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {image_path}")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Definir la región de interés (ROI)
    x_start, x_end = 280, 380
    y_start, y_end = 250, 320
    roi = gray[y_start:y_end, x_start:x_end]

    # Aplicar umbralización adaptativa
    blurred = cv2.GaussianBlur(roi, (5, 5), 0)
    adaptive_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    return adaptive_thresh

# Preprocesar la primera imagen para verificar el preprocesamiento
first_image_path = os.path.join(data_dir, image_files[0])
preprocessed_first_image = preprocess_image(first_image_path)

# Mostrar la imagen preprocesada
plt.imshow(preprocessed_first_image, cmap='gray')
plt.title('Primera Imagen Preprocesada')
plt.show()
