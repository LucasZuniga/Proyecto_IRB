from machine import Pin
from time import sleep_ms, sleep
import _thread

# Example 1

# boton = Pin(20, Pin.IN, Pin.PULL_DOWN)
# azul = Pin(19, Pin.OUT)

# rojo = Pin(18, Pin.OUT)
# amarillo = Pin(17, Pin.OUT)
# verde = Pin(16, Pin.OUT)

# leds = (rojo, amarillo, verde)

# def estado_pulsador_thread():
#     while True:
#         if boton.value() == 1:
#             azul.value(1)
#         else:
#             azul.value(0)
        
#         sleep_ms(10)
        
# _thread.start_new_thread(estado_pulsador_thread, ())

# while True:
#     for led in leds:
#         led.value(1)
#         sleep_ms(500)
#         led.value(0)
#         sleep_ms(500)


# Example2

# def thread_function(param1, param2, param3 = 3):
#     # this will run on core 1
#     pass

# param1 = 1
# param2 = 2

# # start a new thread on core 1
# new_trhead = _thread.start_new_thread(thread_function, (param1, param2), {"param3": 3})

# # this will run on core 0


# Example 3

# def core0_thread():
#     counter = 0
#     while True:
#         print(counter)
#         counter += 2
#         sleep(1)
        
# def core1_thread():
#     counter = 1
#     while True:
#         print(counter)
#         counter += 2
#         sleep(2)
        
        
# second_thread = _thread.start_new_thread(core1_thread, ())

# core0_thread()


# Example 4

def core0_thread():
    global run_core_1
    counter = 0
    while True:
        # print next 5 even numbers
        for loop in range(5):
            print(counter)
            counter += 2
            sleep(1)
            
        # signal core 1 to run
        run_core_1 = True
        
        # wait for core 1 to finish
        print("core 0 waiting")
        while run_core_1:
            pass
        
def core1_thread():
    global run_core_1
    counter = 1
    while True:
        # wait for core 0 to signal start
        print("core 1 waiting")
        while not run_core_1:
            pass
        
        for loop in range(3):
            print(counter)
            counter += 2
            sleep(0.5)
            
        # signal core 0 code finished
        run_core_1 = False
        
# Global variable to send signals between threads
run_core_1 = False
        
second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()