import pygame
import math
import sys

from Constants import *
from Objects import PhysicsObject, Robot, Ball

pygame.init()

# Screen dimensions
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robo-Soccer Simulator")

# Game clock
CLOCK = pygame.time.Clock()

# Initialize Objects
robot1 = Robot(WIDTH/4, HEIGHT/2, 20, 10.0, RED)
robot2 = Robot(WIDTH*3/4, HEIGHT/2, 20, 10.0, BLUE)
robot2.theta = math.pi
ball   = Ball(WIDTH/2, HEIGHT/2, 10, 1.0, YELLOW)     # Ball is lighter

def handle_input(robot1, robot2):
    keys = pygame.key.get_pressed()
    
    # Reset control speeds
    robot1.v_linear = 0
    robot1.v_angular = 0
    robot2.v_linear = 0
    robot2.v_angular = 0
    
    # --- Robot 1 (WASD) ---
    if keys[pygame.K_w]:  # Forward
        robot1.v_linear += robot1.max_linear_v
    if keys[pygame.K_s]:  # Backward
        robot1.v_linear -= robot1.max_linear_v * 0.5
        
    if keys[pygame.K_a]:  # Turn Left
        robot1.v_angular -= robot1.max_angular_v
    if keys[pygame.K_d]:  # Turn Right
        robot1.v_angular += robot1.max_angular_v

    # --- Robot 2 (IJKL) ---
    if keys[pygame.K_i]:  # Forward
        robot2.v_linear += robot2.max_linear_v
    if keys[pygame.K_k]:  # Backward
        robot2.v_linear -= robot2.max_linear_v * 0.5
        
    if keys[pygame.K_j]:  # Turn Left
        robot2.v_angular -= robot2.max_angular_v
    if keys[pygame.K_l]:  # Turn Right
        robot2.v_angular += robot2.max_angular_v

def check_collision(obj1, obj2):
    # Calcualte distance between centers
    dx = obj2.x - obj1.x
    dy = obj2.y - obj1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    # Check if a colision has occurred
    if distance <= (obj1.radius + obj2.radius):
        # Collision Normal Vector (unit vector pointing from obj1 to obj2)
        nx = dx / distance
        ny = dy / distance
        
        # Resolve overlap (move objects apart)
        overlap = obj1.radius + obj2.radius - distance
        obj1.x -= overlap / 2 * nx
        obj1.y -= overlap / 2 * ny
        obj2.x += overlap / 2 * nx
        obj2.y += overlap / 2 * ny
        
        # Relative Velocity
        dvx = obj2.vx - obj1.vx
        dvy = obj2.vy - obj1.vy
        
        # Velocity along the normal
        v_normal = dvx * nx + dvy * ny
        
        # Only resolve if objects are moving towards each other
        if v_normal < 0:
            e = 0.8  # Coefficient of Restitution (bounciness)
            
            # Calculate Impulse (J)
            J = (-(1.0 + e) * v_normal) / (1.0/obj1.mass + 1.0/obj2.mass)
            
            # Apply Impulse to change velocities
            obj1.vx -= J * nx / obj1.mass
            obj1.vy -= J * ny / obj1.mass
            obj2.vx += J * nx / obj2.mass
            obj2.vy += J * ny / obj2.mass

def check_goal(ball):
    global score_red
    global score_blue
    
    # Definición de la altura de la portería
    goal_top = HEIGHT / 3
    goal_bottom = HEIGHT * 2 / 3
    
    # Comprobar si la pelota está en el rango vertical (dentro de la portería)
    if ball.y > goal_top and ball.y < goal_bottom:
        
        # --- GOL PARA EL EQUIPO AZUL (Pelota cruzó la izquierda) ---
        # El límite de la izquierda es 0. Consideramos gol si el centro de la pelota está muy cerca o fuera.
        if ball.x - ball.radius <= 0:
            score_blue += 1
            print(f"¡GOL para AZUL! Marcador: {score_red} - {score_blue}")
            reset_game_after_goal(ball)
            return True # Gol detectado
            
        # --- GOL PARA EL EQUIPO ROJO (Pelota cruzó la derecha) ---
        # El límite de la derecha es WIDTH.
        elif ball.x + ball.radius >= WIDTH:
            score_red += 1
            print(f"¡GOL para ROJO! Marcador: {score_red} - {score_blue}")
            reset_game_after_goal(ball)
            return True # Gol detectado
            
    return False # No hubo gol

def reset_game_after_goal(ball):
    # Centrar la pelota y detener su movimiento
    ball.x = WIDTH / 2
    ball.y = HEIGHT / 2
    ball.vx = 0.0
    ball.vy = 0.0
    
    # Opcional: Centrar los robots para un saque de centro
    robot1.x = WIDTH / 4
    robot1.y = HEIGHT / 2
    robot1.vx = 0.0
    robot1.vy = 0.0
    
    robot2.x = WIDTH * 3 / 4
    robot2.y = HEIGHT / 2
    robot2.vx = 0.0
    robot2.vy = 0.0
           
def draw_field():
    SCREEN.fill(GREEN) # Grass
    # Draw field boundary (optional, already handled by object boundary check)
    pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, HEIGHT), 5)
    
    # Center line
    pygame.draw.line(SCREEN, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT), 2)
    
    # Goals (simple example)
    pygame.draw.rect(SCREEN, RED, (0, HEIGHT/3, 10, HEIGHT/3))
    pygame.draw.rect(SCREEN, BLUE, (WIDTH - 10, HEIGHT/3, 10, HEIGHT/3))
    
def draw_score(surface):
    font = pygame.font.Font(None, 74) # Usa una fuente predeterminada y tamaño 74
    
    # Marcador Rojo (lado izquierdo)
    text_red = font.render(str(score_red), True, RED)
    surface.blit(text_red, (WIDTH/2 - 100, 20))
    
    # Marcador Azul (lado derecho)
    text_blue = font.render(str(score_blue), True, BLUE)
    surface.blit(text_blue, (WIDTH/2 + 60, 20))

# --- Main Game Loop ---

# Variables del Marcador
score_red = 0
score_blue = 0

running = True
while running:
    # 1. Event Handling (Quit event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
    # Input
    handle_input(robot1, robot2)
    
    # Update Physics
    robot1.update()
    robot2.update()
    ball.update()
    
    # Collision Check
    check_collision(robot1, ball)
    check_collision(robot2, ball)
    check_collision(robot1, robot2)
    
    # Check Goal
    check_goal(ball)
    
    # Drawing
    draw_field()
    robot1.draw(SCREEN)
    robot2.draw(SCREEN)
    ball.draw(SCREEN)
    draw_score(SCREEN)
    
    # Refresh Screen
    pygame.display.flip()
    
    # Maintain frame rate
    CLOCK.tick(FPS)

pygame.quit()
sys.exit()