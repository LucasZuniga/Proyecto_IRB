##### Librerias #####

import sys
from machine import Pin
from utime import sleep
from machine import Pin , PWM
from time import sleep, sleep_ms, ticks_us, time_ns
from control_lib import *
import _thread


##### Definicion de pines #####

# LED
led = Pin("LED", Pin.OUT)

# Driver 1
d1_stby = Pin(3, Pin.OUT)
##  Motor 1
d1_ina1 = Pin(2,Pin.OUT)
d1_ina2 = Pin(1, Pin.OUT)
d1_pwma = PWM(Pin(0))
## Encoder 1
m1_enc1 = Pin(7, Pin.IN, Pin.PULL_UP)
m1_enc2 = Pin(8, Pin.IN, Pin.PULL_UP)

# Driver 2
d2_stby = Pin(11, Pin.OUT)
##   Motor 2
d2_ina1 = Pin(6,Pin.OUT)
d2_ina2 = Pin(5, Pin.OUT)
d2_pwma = PWM(Pin(4))
## Encoder 2
m2_enc1 = Pin(9, Pin.IN, Pin.PULL_UP)
m2_enc2 = Pin(10, Pin.IN, Pin.PULL_UP)
##   Rodillo
d2_inb1 = Pin(12,Pin.OUT)
d2_inb2 = Pin(13, Pin.OUT)
d2_pwmb = PWM(Pin(14))

# Solenoide
sol = Pin(15, Pin.OUT)
 

##### Main #####

d1_pwma.freq(1000)      ### Averiguar sobre esta linea ###
d1_stby.value(1)        # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)        # Enable the motor driver 2

led.on()            # Encender el LED para indicar que el programa ha iniciado


# Encoder read #
delay = 10
vel_lectura = 0
duty = 30


m1_enc1_prev = 1
count_pulses = 0


def thread():
    while True:
        RotateCCW(duty, d1_ina1, d1_ina2, d1_pwma)
        sleep(5)
        stop(d1_ina1, d1_ina2, d1_pwma, d2_ina1, d2_ina2, d2_pwma)
        break

        
_thread.start_new_thread(thread, ())    
 

while True:
    m1_enc1_val = m1_enc1.value()
    
    if flanco_subida(m1_enc1_val, m1_enc1_prev):
        if m1_enc2.value():
            count_pulses += 1
        else:
            count_pulses -= 1
            
        print(f"vueltas: {int(count_pulses/685)}, pulsos: {count_pulses}")
        
    if flanco_bajada(m1_enc1_val, m1_enc1_prev):
        if m1_enc2.value():
            count_pulses -= 1
        else:
            count_pulses += 1
            
        print(f"vueltas: {int(count_pulses/685)}, pulsos: {count_pulses}")

    m1_enc1_prev = m1_enc1_val
            
       
        

        