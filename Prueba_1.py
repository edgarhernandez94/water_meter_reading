import cv2
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import time
import numpy as np
class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")
        self.video_label = tk.Label(self.root)
        self.video_label.pack()
        self.capture_interval = 10  # Intervalo de captura en segundos
        # Ruta donde se guardarán las imágenes capturadas
        self.save_folder = r"C:\Users\ATR\Desktop\captured_images"
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        self.cap = cv2.VideoCapture(0)
        self.update_video()
        self.schedule_capture()
    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame
            # Detectar círculos en el fotograma
            circles = self.detect_circles(frame)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                # Iterar sobre cada círculo detectado
                for (x, y, r) in circles:
                    # Dibujar el círculo en el marco
                    cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    # Filtrar rectángulos dentro del círculo actual
                    rectangles = self.detect_rectangles(frame, (x, y, r))
                    if rectangles:
                        for rect in rectangles:
                            cv2.drawContours(frame, [rect], -1, (255, 0, 0), 2)
            # Mostrar la imagen procesada en la interfaz gráfica
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        # Programar la actualización del video cada 10 milisegundos (100 FPS aproximadamente)
        self.root.after(10, self.update_video)
    def detect_circles(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Aplicar un filtro de mediana para reducir el ruido antes de la detección de círculos
        gray = cv2.medianBlur(gray, 5)
        # Detección de círculos utilizando Hough Circles
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=100,
                                   param1=100, param2=45, minRadius=175, maxRadius=215)
        return circles
    def detect_rectangles(self, frame, circle_info):
        x, y, r = circle_info
        # Definir las coordenadas del círculo como una máscara
        mask = np.zeros_like(frame[:, :, 0])
        cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Aplicar un filtro de desenfoque gaussiano para reducir el ruido
        blurred = cv2.GaussianBlur(gray, (7, 7), 1)
        # Detectar bordes en la imagen usando el algoritmo Canny
        edges = cv2.Canny(blurred, 50, 150)  # Ajustar los umbrales según el contenido de la imagen
        # Aplicar la máscara del círculo a los bordes
        masked_edges = cv2.bitwise_and(edges, edges, mask=mask)
        # Encontrar los contornos de los objetos en la imagen de bordes
        contours, _ = cv2.findContours(masked_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Inicializar una lista para almacenar los rectángulos detectados
        rectangles = []
        # Iterar sobre todos los contornos encontrados
        for contour in contours:
            # Calcular el perímetro del contorno cerrado
            perimeter = cv2.arcLength(contour, True)
            # Aproximar el contorno con un polígono de pocos lados (en este caso, 4 lados)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)  # Reducir el epsilon para una aproximación más precisa
            # Verificar si el polígono aproximado tiene exactamente 4 vértices (indicativo de un rectángulo)
            if len(approx) == 4:
                # Calcular el área del contorno
                area = cv2.contourArea(approx)
                # Filtrar rectángulos basados en el área (ajustar según el tamaño esperado de los rectángulos)
                if area > 1000:  # Ajustar el área mínima según el tamaño esperado de los rectángulos
                    rectangles.append(approx.reshape(-1, 2))
        # Devolver la lista de rectángulos detectados
        return rectangles
    def capture_image(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(self.save_folder, f"image_{timestamp}.png")
        cv2.imwrite(image_path, self.frame)
        print(f"Image saved to {image_path}")
    def schedule_capture(self):
        self.capture_image()
        self.root.after(self.capture_interval * 1000, self.schedule_capture)
    def on_closing(self):
        self.cap.release()
        self.root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()