import socket
import json
import sys
import time
import math
import cv2
import numpy as np
import multiprocessing.shared_memory as shm

# El nombre de la memoria COMPARTIDA debe ser copiado de la salida del Simulator.py
SHARED_MEMORY_NAME = 'wnsm_5106c1ae' 

HOST = '127.0.0.1'
PORT = 65432       
ROBOT_ID = 2       # Este controlador manejará el Robot 2 (Azul)
CLIENT_TYPE = "AUTONOMOUS"

HEIGHT, WIDTH, CHANNELS = 600, 800, 3
FPS = 60

# --- Funciones de Visión (OpenCV) ---

def detect_objects_and_orientation(frame_bgr):
    """
    Procesa el frame BGR para encontrar la posición de los objetos clave.
    Aquí se usa un filtro de color HSV básico para detección.
    """
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    
    ball_pos = None
    robot_auto_pos = None
    
    # Detección de la Pelota (Amarillo)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    contours_ball, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_ball:
        largest_contour = max(contours_ball, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 50:
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                ball_pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame_bgr, ball_pos, 5, (0, 255, 255), -1)

    # Detección del Robot Autónomo (Azul)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    contours_robot, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_robot:
        largest_contour = max(contours_robot, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 200:
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                robot_auto_pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame_bgr, robot_auto_pos, 5, (255, 0, 0), -1)
                
    # NOTA: Para obtener la orientación (theta), necesitarías un marcador adicional.
    # Por ahora, se asume orientación cero para la lógica simple de persecución.
    robot_theta = 0.0 

    return ball_pos, robot_auto_pos, robot_theta, frame_bgr

# --- Lógica de Control ---

def calculate_commands(robot_pos, ball_pos, robot_theta):
    """
    Controlador simple P (Proporcional) para ir hacia la pelota.
    """
    v_linear = 0.0
    v_angular = 0.0
    
    if robot_pos is None or ball_pos is None:
        return v_linear, v_angular

    robot_x, robot_y = robot_pos
    ball_x, ball_y = ball_pos

    # 1. Calcular el ángulo deseado (ángulo hacia la pelota)
    dx = ball_x - robot_x
    dy = ball_y - robot_y
    angle_to_target = math.atan2(dy, dx)
    
    # 2. Calcular el error angular (cuánto tiene que girar)
    angle_error = angle_to_target - robot_theta
    angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi # Normalizar
    
    # Constantes Kp
    K_angular = 2.5 
    K_linear = 100.0

    # 3. Comando Angular (Giro): Proporcional al error angular
    v_angular = K_angular * angle_error
    
    # 4. Comando Lineal (Avance): Avanza si está razonablemente alineado
    if abs(angle_error) < 0.2 or abs(angle_error) > (math.pi - 0.2): # Dentro de un cono de 11 grados
        v_linear = K_linear
    else:
        v_linear = 0.0

    return v_linear, v_angular


# --- Función Principal ---

def run_autonomous_controller():
    # 1. CONEXIÓN A MEMORIA COMPARTIDA
    try:
        shm_block = shm.SharedMemory(name=SHARED_MEMORY_NAME)
        frame_shared = np.ndarray(
            (HEIGHT, WIDTH, CHANNELS), 
            dtype=np.uint8, 
            buffer=shm_block.buf
        )
    except FileNotFoundError:
        print("ERROR: Memoria Compartida NO ENCONTRADA. Asegúrate que el SIMULADOR esté corriendo y copia el nombre correcto.")
        return

    # 2. CONEXIÓN SOCKET (para enviar comandos)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Autocontroller conectado al simulador vía Socket.")
        
        id_message = json.dumps({"type": CLIENT_TYPE, "robot_id": ROBOT_ID}) + '\n'
        s.sendall(id_message.encode('utf-8'))
        
    except ConnectionRefusedError:
        print("ERROR: Socket no conectado. Asegúrate que el simulador esté corriendo.")
        shm_block.close()
        return

    # Bucle Principal de Control
    while True:
        try:
            # 3. LEER el frame de la Memoria Compartida
            frame_np_rgb = frame_shared.copy()

            # 4. Convertir y Procesar Frame (OpenCV)
            # El frame compartido es RGB, OpenCV usa BGR
            frame_cv_bgr = cv2.cvtColor(frame_np_rgb, cv2.COLOR_RGB2BGR)
            
            ball_pos, robot_pos, robot_theta, debug_frame = detect_objects_and_orientation(frame_cv_bgr)

            # Mostrar la vista de la IA para depuración
            cv2.imshow(f"IA View (Robot {ROBOT_ID}) - SHM Name: {SHARED_MEMORY_NAME}", debug_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # 5. CALCULAR Comandos de Control
            v_linear, v_angular = calculate_commands(robot_pos, ball_pos, robot_theta)
            
            # 6. ENVIAR Comandos al Simulador vía Socket
            commands = {
                "robot_id": ROBOT_ID,
                "v_linear": v_linear,
                "v_angular": v_angular
            }
            command_message = json.dumps(commands) + '\n'
            s.sendall(command_message.encode('utf-8'))
            
            time.sleep(1/FPS) # Controlar la tasa de actualización

        except ConnectionResetError:
            print("Conexión Socket cerrada por el simulador.")
            break
        except Exception as e:
            # print(f"Error en el bucle de la IA: {e}")
            pass
            
    # Limpieza final
    cv2.destroyAllWindows()
    shm_block.close()
    s.close()

if __name__ == '__main__':
    run_autonomous_controller()