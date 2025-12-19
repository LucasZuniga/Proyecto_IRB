# Rutina de demostracion de la autonomia del robot
import keyboard
import cv2
import math
import os
import random
import time

# Librrias Propias
from aruco_detector2 import ArUco_Marker

ArucoType: dict = {
    'DICT_4X4_50': cv2.aruco.DICT_4X4_50,
    'DICT_4X4_100': cv2.aruco.DICT_4X4_100,
    'DICT_4X4_250': cv2.aruco.DICT_4X4_250,
    'DICT_4X4_1000': cv2.aruco.DICT_4X4_1000,
    'DICT_5X5_50': cv2.aruco.DICT_5X5_50,
    'DICT_5X5_100': cv2.aruco.DICT_5X5_100,
    'DICT_5X5_250': cv2.aruco.DICT_5X5_250,
    'DICT_5X5_1000': cv2.aruco.DICT_5X5_1000,
    'DICT_6X6_50': cv2.aruco.DICT_6X6_50,
    'DICT_6X6_100': cv2.aruco.DICT_6X6_100,
    'DICT_6X6_250': cv2.aruco.DICT_6X6_250,
    'DICT_6X6_1000': cv2.aruco.DICT_6X6_1000,
    'DICT_7X7_50': cv2.aruco.DICT_7X7_50,
    'DICT_7X7_100': cv2.aruco.DICT_7X7_100,
    'DICT_7X7_250': cv2.aruco.DICT_7X7_250,
    'DICT_7X7_1000': cv2.aruco.DICT_7X7_1000,
    'DICT_ARUCO_ORIGINAL': cv2.aruco.DICT_ARUCO_ORIGINAL,
    'DICT_APRILTAG_16h5': cv2.aruco.DICT_APRILTAG_16h5,
    'DICT_APRILTAG_25h9': cv2.aruco.DICT_APRILTAG_25h9,
    'DICT_APRILTAG_36h10': cv2.aruco.DICT_APRILTAG_36h10,
    'DICT_APRILTAG_36h11': cv2.aruco.DICT_APRILTAG_36h11,
}

class Robot:
    def __init__(self, id: int, position: tuple, angle: float):
        self.id = id
        self.pos = position
        self.angle = angle
        self.rodillo = 0
        self.solenoide = 0
        
    def __str__(self) -> str:
        return f"Robot ID: {self.id}, Position: {self.pos}, Angle: {self.angle}"
        
    def has_ball(self, ball, frame) -> bool:
        rob_ball_pose = (self.pos[0] + 100 * math.cos(math.radians(self.angle)),     ## 15 es la distancia desde el centro del robot al frente, ajustar
                         self.pos[1] + 100 * math.sin(math.radians(self.angle)))
        
        cv2.circle(frame, (int(rob_ball_pose[0]), int(rob_ball_pose[1])), 10, (0, 255, 0), -1)
        
        if dist(rob_ball_pose, ball.position) < 10.0:   # Si la pelota est a menos de 10 unidades del frente del robot
            return True
        return False
    
    def shoot(self):
        self.solenoide = 1
        time.sleep_ms(10)
        self.solenoide = 0
    
class Ball:
    def __init__(self, position: tuple):
        self.position = position

def aruco_marker_pose_estimation(cap, aruco_dict, aruco_params, robots: dict): 
    ret, frame = cap.read() 
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    corners, ids, _ = cv2.aruco.detectMarkers(frame_gray, aruco_dict, parameters= aruco_params)
    if ids is not None:
        for i in range(len(ids)):
            if ids[i] < 10:   # Solo se consideran los marcadores con ID menor a 10
                new_marker = ArUco_Marker(corners[i], ids[i])
                robots[int(new_marker.id)] = Robot(new_marker.id, new_marker.centre, new_marker.angle)      # Actualiza la posicion y angulo del robot, y lo crea si no exise 
                new_marker.draw_marker(frame)
            
    return frame, robots


def detectar_color(low_color, high_color, img):
    # Convertimos la imagen a HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Creamos la máscara para el color
    color_mask = cv2.inRange(img_hsv, low_color, high_color)
    
    # Aplicamos la máscara a la imagen original
    img_masked = cv2.bitwise_and(img, img, mask=color_mask)
    
    # Encontramos los contornos en la máscara
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Lista para almacenar los centros de cada objeto detectado
    centros = []
    
    for contour in contours:
        # Ignorar contornos muy pequeños
        if cv2.contourArea(contour) > 200:
            # Obtenemos el bounding box de cada contorno
            x, y, w, h = cv2.boundingRect(contour)
            prom_x = int(x + w / 2)
            prom_y = int(y + h / 2)
            
            # Agregamos el centro a la lista
            centros.append((prom_x, prom_y))
            
            # Dibujamos el centro del objeto detectado en la imagen
            color_caja = (0, 0, 0)
            color_name = "Object"
            cv2.rectangle(img, (x, y), (x + w, y + h), color_caja, 2)
            cv2.putText(img, color_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_caja, 1, cv2.LINE_AA)
            cv2.circle(img, (prom_x, prom_y), 5, (0, 255, 0), -1)
    
    # Retornamos la lista de centros
    return centros

def detectar_pelota(ball, frame):
    center = detectar_color((15, 50, 50), (30, 255, 255), frame)
    ball.position = center[0] if len(center) > 0 else ball.position

def calcular_error_rob(rob, p1):
    d_y = p1[1] - rob.pos[1]
    d_x = p1[0] - rob.pos[0]
    angulo = math.degrees(math.atan2(d_y, d_x))
    delta_theta = (angulo - rob.angle)
    
    if delta_theta > 180:       # Converir a rango [-180, 180]
        delta_theta -= 360
        
    return delta_theta

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def StateMachine():
    
    cap = cv2.VideoCapture(0)
    aruco_dict = cv2.aruco.Dictionary_get(ArucoType["DICT_4X4_1000"])
    aruco_params = cv2.aruco.DetectorParameters_create()
    
    Kp_angle = 1.0
    Kp_dist = 0.5
    robots = {}
    
    ball = Ball((0, 0))
    
    STATE = 'IDLE'
    print("Press SPACE to start the state machine.")
    while True:
        print(f"Current State: {STATE}")
        # Always get the latest frame and detected markers
        frame, robots = aruco_marker_pose_estimation(cap, aruco_dict, aruco_params, robots)
        detectar_pelota(ball, frame)


                  
        # os.system('cls') # Clear console output
        
        for ids in robots:
            if dist(robots[ids].pos, ball.position) < 30.0:
                robots[ids].rodillo = 1
            else:
                robots[ids].rodillo = 0
        
        if keyboard.is_pressed("e"):
            STATE = 'EXIT'
        if keyboard.is_pressed("p"):
            STATE = 'IDLE'
        
        if STATE == 'IDLE':
            if keyboard.is_pressed("SPACE"):    # presionar espacio para iniciar
                STATE = 'ANGLE_BALL'
            
        elif STATE == 'ANGLE_BALL':
            if len(robots) >= 1:
                print(robots[0], ball.position)
                rob_ball_angle = calcular_error_rob(robots[0], ball.position)
                if rob_ball_angle < 5.0 and rob_ball_angle > -5.0:
                    STATE = 'APPROACH_BALL'
                else:
                    vel_r, vel_l = rob_ball_angle * Kp_angle, -rob_ball_angle * Kp_angle        # Proporcional al angulo entre robot y pelota
        
                print("Angle to ball:", rob_ball_angle)

            
        elif STATE == 'APPROACH_BALL':
            if robots[0].has_ball(ball, frame) : # Function to determine if the robot has the ball
                STATE = 'AIM_TARGET'
                target_angle = round((random.random() - 0.5) * 180.0)   # Random target angle between -180 and 180 degrees
            else:
                rob_ball_dist = dist(robots[0].pos, ball.position)
                vel_r, vel_l = Kp_dist * rob_ball_dist, Kp_dist * rob_ball_dist   # Proporcional a la distancia entre robot y pelota
                
                print("Distance to ball:", rob_ball_dist)
        
        
        elif STATE == 'AIM_TARGET':
            dif = target_angle - robots[0].angle
            if abs(dif) < 5.0:
                STATE = 'SHOOT'
            else:
                vel_r, vel_l = dif * Kp_angle, -dif * Kp_angle
                    
        elif STATE == 'SHOOT':
            if robots[0].has_ball(ball, frame):
                robots[0].shoot()
                
            else:
                STATE = 'ANGLE_BALL'    # Go back to find the ball again
        
        
        elif STATE == 'EXIT':
            break
        
        if frame is not None:
            cv2.imshow('ArUco Detection',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                pass


if __name__ == "__main__":
    StateMachine()
    
    

    
    