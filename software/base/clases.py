import time
import math
import cv2
import numpy as np

# Funciones
def dist(p1: tuple, p2: tuple) -> float:
    """Calcula la distancia euclidiana entre dos puntos 2D."""
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def calcular_error_rob(rob, p1):
    d_y = p1[1] - rob.pos[1]
    d_x = p1[0] - rob.pos[0]
    angulo = math.degrees(math.atan2(d_y, d_x))
    delta_theta = (angulo - rob.angle)
    
    if delta_theta > 180:       # Converir a rango [-180, 180]
        delta_theta -= 360
        
    return delta_theta

# Clases
class Robot():
    def __init__(self, id: int, is_ally: bool):
        self.id = id
        self.pos = (-1, -1)
        self.angle = 0.0
        self.is_ally = is_ally
        self.corners = None

    def __str__(self) -> str:
        if self.is_ally:
            return f"Ally Robot ID: {self.id}, Position: {self.pos}, Angle: {self.angle}"
        else:
            return f"Enemy Robot ID: {self.id}, Position: {self.pos}, Angle: {self.angle}"
        
    def update_position(self, corners):
        self.tl = corners[0]
        self.tr = corners[1]
        self.bl = corners[2]
        self.br = corners[3]
        
        self.get_centre()
        self.calc_angle()
        
    def get_centre(self):
        top_centre_x = int((self.tl[0] + self.tr[0])/2)
        top_centre_y = int((self.tl[1] + self.tr[1])/2)
        self.top_centre = (top_centre_x, top_centre_y)
        
        bot_centre_x = int((self.bl[0] + self.br[0])/2)
        bot_centre_y = int((self.bl[1] + self.br[1])/2)
        self.bot_centre = (bot_centre_x, bot_centre_y)
        
        self.rigth_centre = (int((self.tr[0] + self.br[0])/2), int((self.tr[1] + self.br[1])/2))
        
        self.pos = (int((top_centre_x + bot_centre_x)/2), int((top_centre_y + bot_centre_y)/2))
        
    def calc_angle(self):
        dx = self.top_centre[0] - self.pos[0]
        dy = self.top_centre[1] - self.pos[1]

        theta_rad = round((math.atan2(dy, dx)/2), 3)
        theta_deg = int((theta_rad/math.pi)*360)

        self.angle = theta_deg
        
    def has_ball(self, ball) -> bool:
        rob_ball_pose = (self.pos[0] + 15 * math.cos(math.radians(self.angle)),     ## 15 es la distancia desde el centro del robot al frente, ajustar
                         self.pos[1] + 15 * math.sin(math.radians(self.angle)))
        
        if dist(rob_ball_pose, ball.position) < 10.0:   # Si la pelota est a menos de 10 unidades del frente del robot
            return True
        return False
    
    def get_draw_info(self):
        if self.is_ally: 
            color = (255, 0, 0) 
        else: 
            color = (0, 0, 255)
            
        pts = np.array([
            [int(self.tl[0]), int(self.tl[1])],
            [int(self.br[0]), int(self.br[1])],
            [int(self.bl[0]), int(self.bl[1])],
            [int(self.tr[0]), int(self.tr[1])]
            ], dtype=np.int32)

        return pts, color, self.pos, self.top_centre, self.id, self.angle, self.tl
        
    def get_pos(self): return self.pos
    def get_angle(self): return self.angle


class Controlable_Robot(Robot):
    def __init__(self, id: int, is_ally: bool):
        super().__init__(id, is_ally)
        self.state = "IDLE"
        self.vel_r = 0
        self.vel_l = 0
        self.rodillo = 0
        self.solenoide = 0
        
    def get_server_data(self):
        return f"{self.vel_r}, {self.vel_l}, {self.solenoide}, {self.rodillo}"
    
    def set_velocities(self, r, l):
        self.vel_r = r
        self.vel_l = l
    
    def sol_on(self):
        self.solenoide = 1
    
    def sol_off(self):
        self.solenoide = 0
        
    def rod_on(self):
        self.rodillo = 1
    
    def rod_off(self):
        self.rodillo = 0



class Ball():
    def __init__(self):
        self.position = (-1, -1)
        
    def update_position(self, data: tuple):
        self.x = data[0]
        self.y = data[1]
        self.w = data[2]
        self.h = data[3]
        self.position = (int(self.x + self.w/2), int(self.y + self.h/2))
        
    def get_draw_info(self):
        return self.x, self.y, self.w, self.h

    def get_position(self): return self.position