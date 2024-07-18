from flask import Flask, request, Response
import os
from datetime import datetime
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Obtener la imagen desde el cuerpo de la solicitud
        image_data = request.data
        if not image_data:
            return "No image data received", 400
        
        # Generar el nombre del archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'captured_image_{timestamp}.jpg'
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Guardar los datos de la imagen en un archivo
        with open(filepath, 'wb') as f:
            f.write(image_data)

        print(f"Imagen guardada en {filepath}")
        return "File successfully uploaded", 200

    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
