import numpy as np
import cv2
import time
import math
import _thread
from simple_pid import PID

class Pelota():
    def __init__(self, array):
        self.pos = array


class Robot():
    def __init__(self, array):
        self.pos = array
        self.STATE = "PELOTA"
        self.control_pelota = False
        self.rodillo = False
        self.rAr = 0
        self.rAl = 0
        
        self.pid_ang = PID(1, 0.1, 0.05, setpoint=0)
        self.pid_ang.output_limits = (-250, 250)
        self.pid_ang.sample_time = 0.2
        self.delta_ang = 10
        
        self.pid_lin = PID(2, 0.5, 0.1, setpoint=20)
        self.pid_lin.output_limits = (-250, 250)
        self.pid_lin.sample_time = 0.2
        
    def atrapar_pelota(self, Pelota):
        self.control_pelota = Pelota.acquire(blocking=False)
        
    def dispara_pelota(self):
        if self.control_pelota:
            self.rodillo = False
            # activar el solenoide
            


def Juegue_1_rob(robot_1,dist, theta): 
    while True:   
        if robot_1.STATE == "IDLE":
            robot_1.STATE = "PELOTA"
            
        if robot_1.STATE == "PELOTA":
            if abs(dist) < 30:
                r1Ar = 0
                r1Al = 0
            else:
                control_R = -robot_1.pid_ang(theta)
                control_L = robot_1.pid_ang(theta)

                # Correccion linearl solo si el agulo es pequeño
                if abs(theta) < robot_1.delta_ang:
                    control_R -= robot_1.pid_lin(dist)
                    control_L -= robot_1.pid_lin(dist)
                    
                    
                r1Ar = control_R
                r1Al = control_L

        print("Angulo: " + str(theta))
        print("Distancia: " + str(dist))
        time.sleep(0.2)
            
        
    
    