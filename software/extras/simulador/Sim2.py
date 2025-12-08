import pygame
import math
import sys
import socket
import threading
import json
import numpy as np
import cv2
import multiprocessing.shared_memory as shm
import time

# --- 1. CONFIGURACIÓN GLOBAL Y MEMORIA COMPARTIDA ---
pygame.init()
pygame.font.init()

# Colores y Constantes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

# Dimensiones de la pantalla
WIDTH, HEIGHT, CHANNELS = 800, 600, 3
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robo-Soccer Simulator (SERVER)")

# Clock y FPS
CLOCK = pygame.time.Clock()
FPS = 60

# --- CONFIGURACIÓN DE MEMORIA COMPARTIDA (SHARED MEMORY) ---
try:
    FRAME_SIZE = HEIGHT * WIDTH * CHANNELS * np.dtype(np.uint8).itemsize
    shm_block = shm.SharedMemory(create=True, size=FRAME_SIZE)
    SHARED_MEMORY_NAME = shm_block.name

    # Arreglo NumPy para escribir el frame (RGB)
    frame_array = np.ndarray(
        (HEIGHT, WIDTH, CHANNELS), 
        dtype=np.uint8, 
        buffer=shm_block.buf
    )
    print(f"Memoria Compartida creada. Nombre para la IA: {SHARED_MEMORY_NAME}")

except Exception as e:
    print(f"ERROR: Falló la creación de Memoria Compartida: {e}")
    sys.exit()
    
# --- Carga de Imágenes de ArUco Tags ---
TAG_SIZE = 15 # Tamaño del tag en píxeles (debe ser menor que el radio del robot, que es 20)
try:
    ARUCO_TAG_1_IMAGE = pygame.image.load('simulador\ArUco_1.png').convert_alpha()
    ARUCO_TAG_2_IMAGE = pygame.image.load('simulador\ArUco_2.png').convert_alpha()
    
except pygame.error as e:
    print(f"Advertencia: No se encontraron los ArUco tags. Error: {e}")
    ARUCO_TAG_1_IMAGE = None
    ARUCO_TAG_2_IMAGE = None

# --- CONFIGURACIÓN DE RED ---
HOST = '127.0.0.1' 
PORT = 65432       
SERVER_RUNNING = True
CONNECTION_MANUAL = None
CONNECTION_AUTONOMOUS = None

# Almacenamiento de comandos recibidos
desired_speeds = {
    1: {'v_linear': 0.0, 'v_angular': 0.0}, # Robot 1 (Manual)
    2: {'v_linear': 0.0, 'v_angular': 0.0}  # Robot 2 (Autónomo)
}
score_red = 0
score_blue = 0


# --- 2. CLASES DE OBJETOS ---

class PhysicsObject:
    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.vx = 0.0
        self.vy = 0.0
        self.friction = 0.99

    def update(self):
        self.vx *= self.friction
        self.vy *= self.friction
        self.x += self.vx / FPS
        self.y += self.vy / FPS

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Ball(PhysicsObject):
    def __init__(self, x, y, radius, mass, color):
        super().__init__(x, y, radius, mass, color)
        self.restitution = 0.9

    def update(self):
        super().update()
        
        # Wall Collision Check
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx * self.restitution
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx * self.restitution
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * self.restitution
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy * self.restitution

class Robot(PhysicsObject):
    def __init__(self, x, y, radius, mass, color, robot_id):
        super().__init__(x, y, radius, mass, color)
        self.id = robot_id
        self.theta = 0.0
        self.v_linear = 0.0
        self.v_angular = 0.0
        self.max_linear_v = 150.0
        self.max_angular_v = 3.0
        
        # --- Configuración del ArUco Tag ---
        if self.id == 1:
            tag_source = ARUCO_TAG_1_IMAGE
        elif self.id == 2:
            tag_source = ARUCO_TAG_2_IMAGE
        else:
            print("Id not valid")
            
        self.use_tag = tag_source is not None
        
        if self.use_tag:
            # Escalar y almacenar la imagen original del tag
            tag_size_tuple = (TAG_SIZE * 2, TAG_SIZE * 2) # Usamos 2*TAG_SIZE para el tamaño del cuadro del tag
            self.original_tag_image = pygame.transform.scale(tag_source, tag_size_tuple)
            # Guardamos el radio del tag para centrarlo
            self.tag_radius = TAG_SIZE
        
    def apply_control(self):
        self.v_linear = desired_speeds[self.id]['v_linear']
        self.v_angular = desired_speeds[self.id]['v_angular']

    def update(self):
        self.theta += self.v_angular / FPS
        self.vx = self.v_linear * math.cos(self.theta)
        self.vy = self.v_linear * math.sin(self.theta)
        super().update()
        
        # Simple field boundaries for robots
        if self.x < self.radius or self.x > WIDTH - self.radius:
            self.x = max(self.radius, min(self.x, WIDTH - self.radius))
            self.vx = -self.vx * 0.5
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.y = max(self.radius, min(self.y, HEIGHT - self.radius))
            self.vy = -self.vy * 0.5
        
def draw(self, surface):
        # 1. DIBUJAR EL CÍRCULO BASE
        super().draw(surface)
        
        if self.use_tag:
            # 2. ROTACIÓN DEL ARUCO TAG
            # Convertir radianes a grados y ajustar el signo para Pygame
            angle_degrees = -math.degrees(self.theta) 
            
            # Rotar la imagen del tag (usando la imagen original para evitar distorsión acumulada)
            rotated_tag = pygame.transform.rotate(self.original_tag_image, angle_degrees)
            
            # 3. DIBUJAR EL TAG CENTRADO
            
            # El centro del tag es el centro del robot (x, y)
            tag_rect = rotated_tag.get_rect(center=(int(self.x), int(self.y)))
            
            surface.blit(rotated_tag, tag_rect)
            
        else:
            # Fallback: Dibujar la línea de orientación si no hay tag
            end_x = int(self.x + self.radius * math.cos(self.theta))
            end_y = int(self.y + self.radius * math.sin(self.theta))
            pygame.draw.line(surface, BLACK, (int(self.x), int(self.y)), (end_x, end_y), 3)

# Inicializar Objetos
robot1 = Robot(WIDTH/4, HEIGHT/2, 20, 10.0, RED, 1)    # Manual
robot2 = Robot(WIDTH*3/4, HEIGHT/2, 20, 10.0, BLUE, 2)  # Autónomo
ball = Ball(WIDTH/2, HEIGHT/2, 10, 1.0, YELLOW)


# --- 3. FUNCIONES DE RED (SERVIDOR) ---

def client_handler(conn, addr):
    """Maneja la recepción de comandos del cliente en un hilo separado."""
    global CONNECTION_MANUAL, CONNECTION_AUTONOMOUS
    
    buffer = ""
    
    # Paso 1: Identificar el controlador
    try:
        conn.settimeout(5.0) 
        identification_data = conn.recv(1024).decode('utf-8')
        client_info = json.loads(identification_data.strip())
        client_type = client_info.get("type")
        robot_id = client_info.get("robot_id")
        conn.settimeout(None) 
        
        if client_type == "MANUAL":
            CONNECTION_MANUAL = conn
        elif client_type == "AUTONOMOUS":
            CONNECTION_AUTONOMOUS = conn
        else:
            conn.close()
            return

    except Exception:
        conn.close()
        return

    # Paso 2: Bucle de Recepción de Comandos
    while SERVER_RUNNING:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            
            buffer += data
            
            # Procesar todos los mensajes completos en el buffer
            while '\n' in buffer:
                command_str, buffer = buffer.split('\n', 1)
                
                commands = json.loads(command_str.strip())
                target_id = commands.get("robot_id")
                
                if target_id in desired_speeds:
                    desired_speeds[target_id]['v_linear'] = commands.get("v_linear", 0.0)
                    desired_speeds[target_id]['v_angular'] = commands.get("v_angular", 0.0)
                
        except ConnectionResetError:
            break
        except json.JSONDecodeError:
            pass 
        except Exception:
            break

    if conn == CONNECTION_MANUAL: CONNECTION_MANUAL = None
    elif conn == CONNECTION_AUTONOMOUS: CONNECTION_AUTONOMOUS = None
    conn.close()


def setup_server():
    """Configura el socket principal y acepta conexiones en un hilo."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, PORT))
        s.listen(2) 
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        global SERVER_RUNNING
        SERVER_RUNNING = False
        return

    def accept_clients():
        while SERVER_RUNNING:
            try:
                conn, addr = s.accept()
                threading.Thread(target=client_handler, args=(conn, addr)).start()
            except Exception:
                break
        s.close()

    threading.Thread(target=accept_clients).start()

# --- 4. FUNCIONES DE FÍSICA Y JUEGO ---

def check_collision(obj1, obj2):
    dx = obj2.x - obj1.x
    dy = obj2.y - obj1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < obj1.radius + obj2.radius:
        nx = dx / distance
        ny = dy / distance
        overlap = obj1.radius + obj2.radius - distance
        obj1.x -= overlap / 2 * nx
        obj1.y -= overlap / 2 * ny
        obj2.x += overlap / 2 * nx
        obj2.y += overlap / 2 * ny
        dvx = obj2.vx - obj1.vx
        dvy = obj2.vy - obj1.vy
        v_normal = dvx * nx + dvy * ny
        
        if v_normal < 0:
            e = 0.8
            J = (-(1.0 + e) * v_normal) / (1.0/obj1.mass + 1.0/obj2.mass)
            obj1.vx -= J * nx / obj1.mass
            obj1.vy -= J * ny / obj1.mass
            obj2.vx += J * nx / obj2.mass
            obj2.vy += J * ny / obj2.mass

def reset_game_after_goal(ball):
    global desired_speeds
    ball.x = WIDTH / 2; ball.y = HEIGHT / 2; ball.vx = 0.0; ball.vy = 0.0
    robot1.x = WIDTH / 4; robot1.y = HEIGHT / 2; robot1.vx = 0.0; robot1.vy = 0.0; robot1.theta = 0.0
    robot2.x = WIDTH * 3 / 4; robot2.y = HEIGHT / 2; robot2.vx = 0.0; robot2.vy = 0.0; robot2.theta = math.pi
    
    desired_speeds = {1: {'v_linear': 0.0, 'v_angular': 0.0}, 2: {'v_linear': 0.0, 'v_angular': 0.0}}

def check_goal(ball):
    global score_red
    global score_blue
    goal_top = HEIGHT / 3
    goal_bottom = HEIGHT * 2 / 3
    
    if ball.y > goal_top and ball.y < goal_bottom:
        if ball.x - ball.radius < 0:
            score_blue += 1
            reset_game_after_goal(ball)
            return True
        elif ball.x + ball.radius > WIDTH:
            score_red += 1
            reset_game_after_goal(ball)
            return True
    return False

# --- 5. FUNCIONES DE DIBUJO Y PERCEPCIÓN ---

def draw_field():
    SCREEN.fill(GREEN)
    pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, HEIGHT), 5)
    pygame.draw.line(SCREEN, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT), 2)
    pygame.draw.rect(SCREEN, RED, (0, HEIGHT/3, 10, HEIGHT/3))
    pygame.draw.rect(SCREEN, BLUE, (WIDTH - 10, HEIGHT/3, 10, HEIGHT/3))

def draw_score():
    font = pygame.font.Font(None, 74)
    text_red = font.render(str(score_red), True, RED)
    SCREEN.blit(text_red, (WIDTH/2 - 100, 20))
    text_blue = font.render(str(score_blue), True, BLUE)
    SCREEN.blit(text_blue, (WIDTH/2 + 60, 20))

def write_frame_to_shared_memory():
    """Captura el frame de Pygame y lo escribe directamente en la memoria compartida."""
    pygame_surface = pygame.display.get_surface()
    image_data_rgb = pygame.image.tostring(pygame_surface, 'RGB')
    frame_np_rgb = np.frombuffer(image_data_rgb, dtype=np.uint8).reshape((HEIGHT, WIDTH, CHANNELS))

    # Escribir el array RGB directamente
    frame_array[:] = frame_np_rgb 

# --- 6. BUCLE PRINCIPAL ---

def main():
    global SERVER_RUNNING
    setup_server()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        # 1. APLICAR CONTROL
        robot1.apply_control()
        robot2.apply_control()
        
        # 2. ACTUALIZAR FÍSICA
        robot1.update()
        robot2.update()
        ball.update()
        
        # 3. COLISIONES Y REGLAS
        check_collision(robot1, ball)
        check_collision(robot2, ball)
        check_collision(robot1, robot2) 
        check_goal(ball)
        
        # 4. DIBUJO
        draw_field()
        robot1.draw(SCREEN)
        robot2.draw(SCREEN)
        ball.draw(SCREEN)
        draw_score()
        
        # 5. PERCEPCIÓN (ESCRIBIR FRAME)
        write_frame_to_shared_memory()
        
        # 6. REFRESCAR PANTALLA
        pygame.display.flip()
        CLOCK.tick(FPS)

    # Limpieza final
    SERVER_RUNNING = False
    shm_block.close()
    shm_block.unlink() 
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()