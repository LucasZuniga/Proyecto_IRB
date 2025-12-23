import keyboard
import threading
import time

from clases import Robot, Controlable_Robot

def keyboard_process(robots):
    while True:
        r = robots[0]
        
        if keyboard.is_pressed("w"):
            r.set_velocities(50, 50)
        elif keyboard.is_pressed("s"):
            r.set_velocities(-50, -50)
        elif keyboard.is_pressed("a"):
            r.set_velocities(-50, 50)
        elif keyboard.is_pressed("d"):
            r.set_velocities(50, -50)
            
        elif keyboard.is_pressed("SPACE"):
            r.sol_on()
            
        elif keyboard.is_pressed("r"):
            r.rod_on()
        elif keyboard.is_pressed("q"):
            r.rod_off()
            
        else:
            r.set_velocities(0, 0)
            r.sol_off()
            
            
        robots[0] = r
        # print(r.get_server_data())
        
        time.sleep(0.1)
        
        
if __name__ == "__main__":
    
    robots_list = {
        0 : Controlable_Robot(0, True),
        1 : Robot(1, False)
        } 
    
    keyboard_thread = threading.Thread(keyboard_process(robots_list))
    keyboard_thread.start()