import tkinter as tk
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Variables para el seguimiento del dedo índice
drawing = False
last_x, last_y = 0, 0
eraser = False

# Lista para almacenar las líneas dibujadas
lines = []

# Colores disponibles para escribir
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Negro, Rojo, Verde, Azul
current_color = 0  # Color actual (comienza con negro)

# Color verde para el punto de la punta del dedo
color_verde = (0, 255, 0)
# Color blanco para el fondo
color_blanco = (255, 255, 255)

def limpiar_pizarra():
    lines.clear()

def change_color():
    global current_color
    current_color = (current_color + 1) % len(colors)

# Agregar texto para mostrar las teclas y su función
def add_text(frame):
    text = "C: Limpiar   S: Cambiar Color   (Presiona 'Esc' para salir)"
    label = tk.Label(root, text=text)
    label.pack(side="bottom", pady=10, anchor="center")  # Centrar el texto horizontalmente y ajustar el relleno vertical

    
# Crear una ventana de tkinter
root = tk.Tk()
root.title("Pizarra Digital")

# Centrar la ventana en la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 640  # Ancho deseado de la ventana
window_height = 500  # Alto deseado de la ventana
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Crear un lienzo para la pizarra
canvas = tk.Canvas(root, width=window_width, height=460, bg="white")
canvas.pack()

def update_frame():
    global lines
    ret, frame = cap.read()

    height, width, _ = frame.shape
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    frame[:,:,:] = color_blanco  # Establecer el fondo en blanco

    if results.multi_hand_landmarks is not None:
        hand_landmarks = results.multi_hand_landmarks[0]

        x_punta = int(hand_landmarks.landmark[8].x * width)
        y_punta = int(hand_landmarks.landmark[8].y * height)

        if hand_landmarks.landmark[8].z < 0:
            yema_orientada_hacia_camara = True
        else:
            yema_orientada_hacia_camara = False

        if yema_orientada_hacia_camara:
            cv2.circle(frame, (x_punta, y_punta), 10, color_verde, -1)

        if yema_orientada_hacia_camara:
            drawing = True
        else:
            drawing = False

        if drawing:
            current_line = lines[-1] if lines else []
            current_line.append((x_punta, y_punta))
            lines.append(current_line)

    for line in lines:
        if len(line) > 1:
            for i in range(1, len(line)):
                x1, y1 = line[i - 1]
                x2, y2 = line[i]
                cv2.line(frame, (x1, y1), (x2, y2), colors[current_color], 5)

    add_text(frame)  # Agregar texto

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.image = photo

    canvas.after(10, update_frame)

# Iniciar el proceso de detección de manos
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

def on_key(event):
    if event.keysym == 'c' or event.keysym == 'C':
        limpiar_pizarra()
    elif event.keysym == 'e' or event.keysym == 'E':
        eraser = not eraser
    elif event.keysym == 's' or event.keysym == 'S':
        change_color()
    elif event.keysym == 'Escape':
        root.quit()  # Para salir la aplicación

root.bind('<Key>', on_key)  # Capturar eventos de teclado

update_frame()
root.mainloop()
cap.release()
cv2.destroyAllWindows()









