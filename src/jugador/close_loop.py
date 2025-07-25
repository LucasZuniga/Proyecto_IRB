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



# Set vel reference [thread 1] #

vel_ref_1 = 60
vel_ref_2 = 60

def set_vel_ref():
    global vel_ref_1
    while True:
        vel_ref = int(input("set the vel ref (30 - 100)[RPM]: "))
        vel_ref_1 = vel_ref
        sleep(0.5)

        
second_thread = _thread.start_new_thread(set_vel_ref, ())


# Encoder read  [thread 0] #

# Motor 1
vel_lectura_1 = 0
duty_1 = 20
m1_enc1_prev = 1
count_pulses_1 = 0
count_pulses_1_prev = 0
Kp_1 = 1
Ki_1 = 0.4
Kd_1 = 0
integral_1 = 0

# Motor 2
vel_lectura_2 = 0
duty_2 = 20
m2_enc1_prev = 1
count_pulses_2 = 0
count_pulses_2_prev = 0
Kp_2 = 1
Ki_2 = 0.4
Kd_2 = 0
integral_2 =0

led.on()
calc_vel = 0
time_prev = time_ns()


while True:
    try:
        forward(duty_1, d1_ina1, d1_ina2, d1_pwma, duty_2, d2_ina1, d2_ina2, d2_pwma)
        m1_enc1_val = m1_enc1.value()
        m2_enc1_val = m2_enc1.value()
        
        # Pulse Counter Motor 1
        if flanco_subida(m1_enc1_val, m1_enc1_prev):
            if m1_enc2.value():
                count_pulses_1 += 1
            else:
                count_pulses_1 -= 1
                
        if flanco_bajada(m1_enc1_val, m1_enc1_prev):
            if m1_enc2.value():
                count_pulses_1 -= 1
            else:
                count_pulses_1 += 1
         
               
        # Pulse Counter Motor 2
        if flanco_subida(m2_enc1_val, m2_enc1_prev):
            if m2_enc2.value():
                count_pulses_2 -= 1
            else:
                count_pulses_2 += 1
                            
        if flanco_bajada(m2_enc1_val, m2_enc1_prev):
            if m2_enc2.value():
                count_pulses_2 += 1
            else:
                count_pulses_2 -= 1
        
        
        if calc_vel % 500 == 0:
            # Calcular velocidad
            now = time_ns()
            delta_time = now - time_prev
            # Motor 1
            delta_pulsos_1 = count_pulses_1 - count_pulses_1_prev
            vel_lectura_1 = (87591240)*(delta_pulsos_1/delta_time)         # 87591240 = (60sec = 1 min)*(10^9 nanosec = 1sec)/(685 pulsos = 1 Rev)
            
            # Motor 2
            delta_pulsos_2 = count_pulses_2 - count_pulses_2_prev
            vel_lectura_2 = (87591240)*(delta_pulsos_2/delta_time)
            
            # print(f"vel ref: {vel_ref_1} RPM, vel lectura 1: {int(vel_lectura_1)} RPM, vel lectura 2: {int(vel_lectura_2)} RPM")
            
            time_prev = now
            count_pulses_1_prev = count_pulses_1
            count_pulses_2_prev = count_pulses_2
            
            # Controlador
            error_1 = vel_ref_1 - vel_lectura_1
            integral_1 += error_1
            integral_1 = min(max(integral_1, -200), 200)              # Unwind, ponemos un maximo al integral para evitar problemas por acumulacion
            duty_1 += Kp_1*error_1 + Ki_1*integral_1
            duty_1 = min(max(0, duty_1), 70)
            
            error_2 = vel_ref_1 - vel_lectura_2
            integral_2 += error_2
            integral_2 = min(max(integral_2, -200), 200)
            duty_2 += Kp_2*error_2 + Ki_2*integral_2
            duty_2 = min(max(0, duty_2), 70)


        m1_enc1_prev = m1_enc1_val
        m2_enc1_prev = m2_enc1_val
        calc_vel += 1
        
    except KeyboardInterrupt:
        stop(d1_ina1, d1_ina2, d1_pwma, d2_ina1, d2_ina2, d2_pwma)
        led.off()
        break
            
       
        

        