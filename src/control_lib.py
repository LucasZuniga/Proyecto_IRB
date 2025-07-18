"""
Libreria para el control de actuadores del robot IRB.

"""
##### Librerias #####

from machine import Pin , PWM
from utime import sleep


##### Definicion de pines #####

# LED
led = Pin("LED", Pin.OUT)

# Driver 1
d1_stby = Pin(3, Pin.OUT)
##  Motor 1
d1_ina1 = Pin(2,Pin.OUT)
d1_ina2 = Pin(1, Pin.OUT)
d1_pwma = PWM(Pin(0))

# Driver 2
d2_stby = Pin(11, Pin.OUT)
##   Motor 1
d2_ina1 = Pin(6,Pin.OUT)
d2_ina2 = Pin(5, Pin.OUT)
d2_pwma = PWM(Pin(4))
##   Rodillo
d2_inb1 = Pin(12,Pin.OUT)
d2_inb2 = Pin(13, Pin.OUT)
d2_pwmb = PWM(Pin(14))

# Solenoide
sol = Pin(15, Pin.OUT)

# Encoders
## Motor 1
m1_enc1 = Pin(7, Pin.IN)
m1_enc2 = Pin(8, Pin.IN)
## Motor 2
m2_enc1 = Pin(9, Pin.IN)
m2_enc2 = Pin(10, Pin.IN)

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
    
def backward(duty):
    RotateCW(duty, d1_ina1, d1_ina2, d1_pwma)
    RotateCCW(duty, d2_ina1, d2_ina2, d2_pwma)

def forward(duty):
    RotateCCW(duty, d1_ina1, d1_ina2, d1_pwma)
    RotateCW(duty, d2_ina1, d2_ina2, d2_pwma)
    
def stop():
    StopMotor(d1_ina1, d1_ina2, d1_pwma)
    StopMotor(d2_ina1, d2_ina2, d2_pwma)
    
def rodillo_in(duty):
    d2_inb1.value(1)
    d2_inb2.value(0)
    duty_16 = int((duty*65535)/100)
    d2_pwmb.duty_u16(duty_16)

def rodillo_out(duty):
    d2_inb1.value(0)
    d2_inb2.value(1)
    duty_16 = int((duty*65535)/100)
    d2_pwmb.duty_u16(duty_16)
    
def rodillo_stop():
    d2_inb1.value(0)
    d2_inb2.value(0)
    d2_pwmb.duty_u16(0)

def solenoid_on():
    sol.value(1)

def solenoid_off():
    sol.value(0)

##### main #####

d1_pwma.freq(1000)
d1_stby.value(1)  # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)  # Enable the motor driver 2

led.toggle()

while True:
    txt = input()
    if txt == "s":
        stop()
        break
    
    elif txt == "f":
        duty_cycle = min(int(input("Ingrese el ciclo de trabajo (0-100): ")), 100)
        forward(duty_cycle)
        
    elif txt == "b":
        duty_cycle = min(int(input("Ingrese el ciclo de trabajo (0-100): ")), 100)
        backward(duty_cycle)

stop()
led.toggle()