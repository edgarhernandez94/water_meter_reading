import serial
import time
from datetime import datetime
import cv2
import numpy as np

def capture_image(serial_port, baudrate):
    try:
        # Abre la conexión serial
        ser = serial.Serial(serial_port, baudrate, timeout=10)
        time.sleep(2)  # Espera para establecer la conexión

        if not ser.is_open:
            print(f"Error: No se pudo abrir el puerto serial {serial_port}")
            return

        try:
            while True:
                # Leer datos hasta encontrar el marcador de inicio
                buffer = b""
                while True:
                    if ser.in_waiting:
                        buffer += ser.read(ser.in_waiting)
                        start_index = buffer.find(b'STARTIMG')
                        if start_index != -1:
                            buffer = buffer[start_index:]
                            break
                        elif len(buffer) > 100:
                            buffer = buffer[-10:]  # Mantén los últimos 10 bytes

                # Espera a recibir la longitud de la imagen
                length_bytes = ser.read(4)
                if len(length_bytes) != 4:
                    raise Exception("Failed to read the length of the image")
                length = int.from_bytes(length_bytes, 'little')

                # Verificar la longitud recibida
                if length <= 0:
                    raise Exception("Invalid image length received")

                # Lee los datos de la imagen
                image_data = ser.read(length)
                if len(image_data) != length:
                    raise Exception("Image data is incomplete")

                # Espera el identificador de fin
                end_marker = ser.read(6)
                if end_marker != b'ENDIMG':
                    raise Exception("End marker not found")

                # Muestra la imagen en tiempo real
                nparr = np.frombuffer(image_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow('Real-time Image', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

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
            # Cierra la conexión serial y la ventana de OpenCV
            ser.close()
            cv2.destroyAllWindows()
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")

if __name__ == "__main__":
    serial_port = 'COM10'  # Cambia esto al puerto correcto
    baudrate = 115200

    capture_image(serial_port, baudrate)
