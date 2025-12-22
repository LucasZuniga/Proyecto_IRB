# Librarias
import cv2
import math
import time
import multiprocessing as mp

# Librrias Propias
from clases import Robot, Controlable_Robot, Ball
from get_field_data import Get_Field_Data


if __name__ == "__main__":
    robots_list = {
        0 : Controlable_Robot(0, True),
        1 : Robot(1, False)
        }
    
    ball = Ball()
    
    # Un segundo Thread (principal), se encarga de levantar el servidor y enviar las velocidades a los robots
    field_data_process = mp.Process(target=Get_Field_Data, args=(robots_list, ball))
    field_data_process.start()