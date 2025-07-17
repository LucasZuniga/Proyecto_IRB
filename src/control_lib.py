"""
Libreria de control de motores para el robot IRB.

"""
from machine import Pin , PWM
from utime import sleep

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

led = Pin("LED", Pin.OUT)

d1_pwma.freq(1000)
d1_stby.value(1)  # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)  # Enable the motor driver 2

led.toggle()

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

while True:
    duty_cycle=float(input("Enter pwm duty cycle"))
    print (duty_cycle)
    sleep(1)
    
    forward(duty_cycle)
    sleep(3)

    backward(duty_cycle)
    sleep(3)

    stop()