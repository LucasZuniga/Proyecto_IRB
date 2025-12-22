# Rutina de demostracion de la autonomia del robot
import keyboard
import cv2
import math
import os
import random
import time
import threading
from clases import Ball, Robot, Controlable_Robot


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


def StateMachine(robots: dict, ball: Ball ):
    Kp_angle = 1.0
    Kp_dist = 0.5
    STATE = 'IDLE'
    print("Press SPACE to start the state machine.")
    while True:
        
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
                    robots[0].vel_r, robots[0].vel_l = rob_ball_angle * Kp_angle, -rob_ball_angle * Kp_angle        # Proporcional al angulo entre robot y pelota
        
                print("Angle to ball:", rob_ball_angle)

            
        elif STATE == 'APPROACH_BALL':
            if robots[0].has_ball(ball) : # Function to determine if the robot has the ball
                STATE = 'AIM_TARGET'
                target_angle = round((random.random() - 0.5) * 180.0)   # Random target angle between -180 and 180 degrees
            else:
                rob_ball_dist = dist(robots[0].pos, ball.position)
                robots[0].vel_r, robots[0].vel_l = Kp_dist * rob_ball_dist, Kp_dist * rob_ball_dist   # Proporcional a la distancia entre robot y pelota
                
                print("Distance to ball:", rob_ball_dist)
        
        
        elif STATE == 'AIM_TARGET':
            dif = target_angle - robots[0].angle
            if abs(dif) < 5.0:
                STATE = 'SHOOT'
            else:
                robots[0].vel_r, robots[0].vel_l = dif * Kp_angle, -dif * Kp_angle
                    
        elif STATE == 'SHOOT':
            if robots[0].has_ball(ball):
                robots[0].shoot()
                
            else:
                STATE = 'ANGLE_BALL'    # Go back to find the ball again
        
        
        elif STATE == 'EXIT':
            break


if __name__ == "__main__":
    robot = Controlable_Robot(0, True)
    ball = Ball()
    StateMachine({0: robot}, ball) 
    

    
    