# Rutina de demostracion de la autonomia del robot
import cv2
import math
import time
import numpy as np

# Librrias Propias
from aruco_detector2 import ArucoType
from clases import Ball, Robot, Controlable_Robot


def aruco_marker_pose_estimation(cap, aruco_dict, aruco_params): 
    robots = {}
    ret, frame = cap.read() 
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    corners, ids, _ = cv2.aruco.detectMarkers(frame_gray, aruco_dict, parameters= aruco_params)
    if ids is not None:
        for i in range(len(ids)):
            if ids[i] < 10:   # Solo se consideran los marcadores con ID menor a 10
                robots[int(ids[i])] = (corners[i])
            
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
    data = []
    
    for contour in contours:
        # Ignorar contornos muy pequeños
        if cv2.contourArea(contour) > 200:
            # Obtenemos el bounding box de cada contorno
            x, y, w, h = cv2.boundingRect(contour)
            data.append((x, y, w, h))
        
    # Retornamos el primer elemento de la lista de centros
    if len(data) >= 1:
        return data[0]
    else:
        return None

def detectar_pelota(frame):
    ball_pos = detectar_color((15, 50, 50), (30, 255, 255), frame)
    return ball_pos

def draw_ball(frame, ball_pos):
    if ball_pos is not None:
        x, y, w, h = ball_pos
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(frame, "Ball", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        cv2.circle(frame, (int(x + w/2), int(y + h/2)), 5, (0, 255, 0), -1)

        
def draw_robot(frame, corners, id):
    ally = [0]
    if id in ally:
        color = (255, 0, 0) 
    else: 
        color = (0, 0, 255)

    pts = np.array([
        [int(corners[0][0][0]), int(corners[0][0][1])],
        [int(corners[0][3][0]), int(corners[0][3][1])],
        [int(corners[0][2][0]), int(corners[0][2][1])],
        [int(corners[0][1][0]), int(corners[0][1][1])]
        ], dtype=np.int32)

    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2)
    
    # cv2.line(frame, robot.pos, robot.top_centre, color, 2)
    # cv2.putText(frame, f"ID: {robot.id}, {robot.angle} deg", (int(robot.tl[0]), int(robot.tl[1]) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, )

        


def Get_Field_Data(robots: dict, ball: Ball):
    
    cap = cv2.VideoCapture(0)
    aruco_dict = cv2.aruco.Dictionary_get(ArucoType["DICT_4X4_1000"])
    aruco_params = cv2.aruco.DetectorParameters_create()
    
    
    while True:
        # Always get the latest frame and detected markers
        frame, robots_pos = aruco_marker_pose_estimation(cap, aruco_dict, aruco_params)
        ball_pos = detectar_pelota(frame)
        
        for id in robots_pos:
            if id in robots:
                r = robots[id]
                r.update_position(robots_pos[id])
                # r.draw(frame)
                draw_robot(frame, robots_pos[id], id)
                robots[id] = r
            
        if ball_pos is not None:
            ball.update_position(ball_pos)
            draw_ball(frame, ball_pos)
            # ball.draw(frame)
        
        # cv2.putText(frame, f"STATE: {STATE}", (int(frame.shape[0]/2), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        
        if frame is not None:
            cv2.imshow('ArUco Detection',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                pass


if __name__ == "__main__":
    robots_list = {
        0 : Controlable_Robot(0, True),
        1 : Robot(1, False)
        }
    
    ball = Ball()
    
    Get_Field_Data(robots_list, ball)
    
    
    

    
    