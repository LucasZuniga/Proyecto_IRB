"""
Libreria para el control de actuadores del robot IRB.

"""
##### Librerias #####

from machine import Pin , PWM
from time import sleep, sleep_ms, ticks_us


##### Definicion de pines #####

# LED
led = Pin("LED", Pin.OUT)

# Driver 1
d2_stby = Pin(11, Pin.OUT)
##   Motor 2
d2_ina1 = Pin(6,Pin.OUT)
d2_ina2 = Pin(5, Pin.OUT)
d2_pwma = PWM(Pin(4))
## Encoder 1
m1_enc1 = Pin(10, Pin.IN, Pin.PULL_UP)
m1_enc2 = Pin(8, Pin.IN, Pin.PULL_UP)


##### Definicion de funciones ####

def RotateCW(duty, m1, m2, pwm):
    m1.value(1)
    m2.value(0)
    duty_16 = int((duty*65536)/100)
    pwm.duty_u16(duty_16)

def RotateCCW(duty, m1, m2, pwm):
    m1.value(0)
    m2.value(1)
    duty_16 = int((duty*65536)/100)
    pwm.duty_u16(duty_16)
    
def StopMotor(m1, m2, pwm):
    m1.value(0)
    m2.value(0)
    pwm.duty_u16(0)

##### Main #####

d2_pwma.freq(1000)      ### Averiguar sobre esta linea ###
d2_stby.value(1)        # Enable the motor driver 1

led.toggle()            # Encender el LED para indicar que el programa ha iniciado

duty = 60
delay = 0.2

while True:
    
    RotateCW(duty, d2_ina1, d2_ina2, d2_pwma)
    print(f"enc1: {m1_enc1.value()}, enc2: {m1_enc2.value()}")
        
    sleep(delay)


stop()
led.toggle()            # Apagar el LED para indicar que el programa ha terminado