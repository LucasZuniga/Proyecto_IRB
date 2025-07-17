from control_lib import *
from machine import Pin , PWM
from utime import sleep

led = Pin("LED", Pin.OUT)   # Prende una led para visualizar funcionamiento de la placa

# driver 1
d1_ina1 = Pin(2,Pin.OUT)
d1_ina2 = Pin(1, Pin.OUT)
d1_stby = Pin(3, Pin.OUT)
d1_pwma = PWM(Pin(0))

# driver 2
d2_ina1 = Pin(6,Pin.OUT)
d2_ina2 = Pin(5, Pin.OUT)
d2_stby = Pin(11, Pin.OUT)
d2_pwma = PWM(Pin(4))

d1_pwma.freq(1000)
d1_stby.value(1)  # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)  # Enable the motor driver 2

led.toggle()

while True:
    duty_cycle=float(input("Enter pwm duty cycle"))
    print (duty_cycle)
    sleep(1)
    
    RotateCW(duty_cycle, d1_ina1, d1_ina2, d1_pwma)
    RotateCW(duty_cycle, d2_ina1, d2_ina2, d2_pwma)
    sleep(5)
    
    RotateCCW(duty_cycle, d1_ina1, d1_ina2, d1_pwma)
    RotateCCW(duty_cycle, d2_ina1, d2_ina2, d2_pwma)
    sleep(5)
    
    StopMotor(d1_ina1, d1_ina2, d1_pwma)
    StopMotor(d2_ina1, d2_ina2, d2_pwma)