import serial
import time
from datetime import datetime

def capture_image(serial_port, baudrate):
    try:
        # Abre la conexión serial
        ser = serial.Serial(serial_port, baudrate, timeout=10)
        time.sleep(2)  # Espera para establecer la conexión
        print(f"Conexión serial abierta en {serial_port} con baudrate {baudrate}")

        while True:
            # Leer datos hasta encontrar el marcador de inicio
            buffer = b""
            while True:
                if ser.in_waiting:
                    buffer += ser.read(ser.in_waiting)
                    start_index = buffer.find(b'STARTIMG')
                    if start_index != -1:
                        buffer = buffer[start_index:]
                        print("Marcador de inicio encontrado")
                        break
                    elif len(buffer) > 100:
                        buffer = buffer[-10:]  # Mantén los últimos 10 bytes

            # Espera a recibir la longitud de la imagen
            length_bytes = ser.read(4)
            if len(length_bytes) != 4:
                raise Exception("Failed to read the length of the image")
            length = int.from_bytes(length_bytes, 'little')
            print(f"Longitud de la imagen recibida: {length}")

            # Verificar la longitud recibida
            if length <= 0:
                raise Exception("Invalid image length received")

            # Lee los datos de la imagen
            image_data = ser.read(length)
            if len(image_data) != length:
                raise Exception("Image data is incomplete")
            print(f"Datos de imagen recibidos: {len(image_data)} bytes")

            # Espera el identificador de fin
            end_marker = ser.read(6)
            if end_marker != b'ENDIMG':
                raise Exception("End marker not found")
            print("Marcador de fin encontrado")

            # Genera el nombre del archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'captured_image_{timestamp}.jpg'

            # Guarda los datos en un archivo JPG
            with open(output_file, 'wb') as file:
                file.write(image_data)

            print(f"Imagen guardada en {output_file}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cierra la conexión serial
        ser.close()
        print("Conexión serial cerrada")

if __name__ == "__main__":
    serial_port = 'COM10'  # Cambia esto al puerto correcto
    baudrate = 115200

    capture_image(serial_port, baudrate)
