import pygame
import socket
import json
import sys
import time
import math

# --- Configuración de la Red y del Robot ---
HOST = '127.0.0.1'
PORT = 65432       # Debe coincidir con el puerto del simulador
ROBOT_ID = 1       # Este controlador manejará el Robot 1 (Rojo)
CLIENT_TYPE = "MANUAL"

# --- Parámetros de Control (Asegúrate de que coincidan con los del Robot en el Simulador) ---
MAX_LINEAR_V = 150.0  # Velocidad máxima de avance
MAX_ANGULAR_V = 3.0    # Velocidad máxima de giro

# --- Función Principal de Comunicación y Control ---

def run_manual_controller():
    # Inicialización de Pygame para el manejo del teclado
    pygame.init()
    
    # Necesitas una ventana activa para que pygame detecte los eventos de teclado
    # aunque esta ventana puede ser mínima o incluso invisible.
    # Usaremos una ventana pequeña solo para asegurar el loop de eventos.
    screen_width, screen_height = 100, 100
    pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Manual Controller")
    
    clock = pygame.time.Clock()
    FPS = 60 # Sincronizar con el simulador

    # Intentar establecer la conexión socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Manual Controller conectado al simulador.")
        
        # Enviar mensaje de identificación al servidor
        id_message = json.dumps({"type": CLIENT_TYPE, "robot_id": ROBOT_ID}) + '\n'
        s.sendall(id_message.encode('utf-8'))
        
    except ConnectionRefusedError:
        print("ERROR: No se pudo conectar. Asegúrate de que el simulador esté corriendo.")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Error de conexión: {e}")
        pygame.quit()
        sys.exit()

    running = True
    while running:
        # Reiniciar comandos de velocidad en cada frame
        v_linear = 0.0
        v_angular = 0.0
        
        # 1. Manejo de Eventos y Teclado (Input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()

        # --- WASD para Robot 1 (Rojo) ---
        if keys[pygame.K_w]:  # Forward
            v_linear += MAX_LINEAR_V
        if keys[pygame.K_s]:  # Backward (más lento)
            v_linear -= MAX_LINEAR_V * 0.5
            
        if keys[pygame.K_a]:  # Turn Left
            v_angular -= MAX_ANGULAR_V
        if keys[pygame.K_d]:  # Turn Right
            v_angular += MAX_ANGULAR_V
            
        if keys[pygame.K_ESCAPE]:
            running = False

        # 2. Enviar Comandos al Simulador
        try:
            commands = {
                "robot_id": ROBOT_ID,
                "v_linear": v_linear,
                "v_angular": v_angular
            }
            command_message = json.dumps(commands) + '\n'
            s.sendall(command_message.encode('utf-8'))

        except ConnectionResetError:
            print("Conexión perdida con el simulador.")
            running = False
        except Exception as e:
            # print(f"Error enviando comandos: {e}")
            pass # Ignorar errores temporales

        # Mantener el ritmo del loop
        clock.tick(FPS)
        
    # Limpieza final
    s.close()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    run_manual_controller()