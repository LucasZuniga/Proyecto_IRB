# Rutina de demostracion de la autonomia del robot
import keyboard
import cv2
import math
import os
import random
import time
import threading
from clases import Ball, Robot, Controlable_Robot

def has_ball(rob_pos, rob_angle, ball_pos) -> bool:
    rob_ball_pose = (rob_pos[0] + 15 * math.cos(math.radians(rob_angle)),     ## 15 es la distancia desde el centro del robot al frente, ajustar
                        rob_pos[1] + 15 * math.sin(math.radians(rob_angle)))
    
    if dist(rob_ball_pose, ball_pos) < 10.0:   # Si la pelota est a menos de 10 unidades del frente del robot
        return True
    return False

def calcular_error_rob(rob_pos, rob_angle, p1):
    d_y = p1[1] - rob_pos[1]
    d_x = p1[0] - rob_pos[0]
    angulo = math.degrees(math.atan2(d_y, d_x))
    delta_theta = (angulo - rob_angle)
    
    if delta_theta > 180:       # Converir a rango [-180, 180]
        delta_theta -= 360
        
    return delta_theta

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def StateMachine(robots: dict, ball: Ball ):
    Kp_angle = 1.0
    Kp_dist = 0.5
    STATE = 'IDLE'
    print("Press SPACE to start the state machine.")
    while True:
        # Make sure that we use the same pose and angle during the loop
        r = robots[0]
        b = ball
        rob_pos = r.get_pos()
        rob_angle = r.get_angle()
        ball_pos = b.get_pos()
        
        if dist(rob_pos, ball_pos) < 30.0:
            r.rod_on()
        else:
            r.rod_off()
        
        if keyboard.is_pressed("e"):
            STATE = 'EXIT'
        if keyboard.is_pressed("p"):
            STATE = 'IDLE'
        
        ### State Machine ###
        if STATE == 'IDLE':
            if keyboard.is_pressed("SPACE"):    # presionar espacio para iniciar
                STATE = 'ANGLE_BALL'
            
        elif STATE == 'ANGLE_BALL':
            if len(robots) >= 1:
                # print(r, ball.get_pos())
                rob_ball_angle = calcular_error_rob(rob_pos, rob_angle, ball_pos)
                if rob_ball_angle < 5.0 and rob_ball_angle > -5.0:
                    STATE = 'APPROACH_BALL'
                else:
                    vel_r, vel_l = rob_ball_angle * Kp_angle, -rob_ball_angle * Kp_angle        # Proporcional al angulo entre robot y pelota
                    r.set_velocities(vel_r, vel_l)
        
                # print("Angle to ball:", rob_ball_angle)

        elif STATE == 'APPROACH_BALL':
            if has_ball(rob_pos, rob_angle, ball_pos) : # Function to determine if the robot has the ball
                STATE = 'AIM_TARGET'
                target_angle = round((random.random() - 0.5) * 180.0)   # Random target angle between -180 and 180 degrees
            else:
                rob_ball_dist = dist(rob_pos, ball_pos)
                vel_r, vel_l = Kp_dist * rob_ball_dist, Kp_dist * rob_ball_dist   # Proporcional a la distancia entre robot y pelota
                r.set_velocities(vel_r, vel_l)
                
                # print("Distance to ball:", rob_ball_dist)
        
        elif STATE == 'AIM_TARGET':
            dif = target_angle - rob_angle
            if abs(dif) < 5.0:
                STATE = 'SHOOT'
            else:
                vel_r, vel_l = dif * Kp_angle, -dif * Kp_angle
                r.set_velocities(vel_r, vel_l)
                    
        elif STATE == 'SHOOT':
            if has_ball(rob_pos, rob_angle, ball_pos):
                r.sol_on()
                STATE = 'SHOOTING'
            else:
                STATE = 'ANGLE_BALL'    # Go back to find the ball again
                
        elif STATE == 'SHOOTING':
            time.sleep_ms(100)
            r.sol_off()
            STATE = 'ANGLE_BALL'
        
        elif STATE == 'EXIT':
            break
        
        robots[0] = r


if __name__ == "__main__":
    robot = Controlable_Robot(0, True)
    ball = Ball()
    StateMachine({0: robot}, ball) 
    

    
    