"""
Libreria para el control de actuadores del robot IRB.

"""
##### Librerias #####

from machine import Pin , PWM
from time import sleep, sleep_ms, ticks_us, time_ns, time

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
    
def flanco_subida(bit, bit_prev):
    if not bit_prev and bit:
        return True
    return False

def flanco_bajada(bit, bit_prev):
    if bit_prev and not bit:
        return True
    return False

def vel_encoders(enc1, enc1_prev, time_prev, time_entre_subida_1):
    '''
    Esta función calculará la velocidad del motor utilizando los flancos de subida y de bajada de los encoders, luego tomará un promedio de estas.
    Para determinar la dirección de giro utilizará el desface de ambos encoders.
    '''
    time_now = time_ns()
    dif_time = time_now - time_prev
    
    time_entre_subida_1 += dif_time

    
    if flanco_subida(enc1, enc1_prev):
        vel_subida_1 = 1000000000/(max(time_entre_subida_1, 0.00001))
        return [True, vel_subida_1]
    
    time_prev = time_now
    return [False, time_prev, time_entre_subida_1]

##### Main #####

d1_pwma.freq(1000)
d1_stby.value(1)
d2_pwma.freq(1000)
d2_stby.value(1)

led.toggle()            # Encender el LED para indicar que el programa ha iniciado

duty = 15

enc1_prev = 1
enc2_prev = 1

vel_s1b1s2b2 = [0,0,0,0]
vel_prev = 0
time_0 = time_ns()
time_prev_s1 = time_0
time_prev_b1 = time_0
time_prev_s2 = time_0
time_prev_b2 = time_0

# Lazo cerrado

vel_ref = 180

Kp = 0.01
Ki = 0
Kd = 0


while True:
    error = vel_ref - vel_prev
    duty += Kp*error
    duty = max(15, (min(duty, 100)))
    
    RotateCCW(duty, d1_ina1, d1_ina2, d1_pwma)
    
    if flanco_subida(m1_enc1.value(), enc1_prev):
        now = time_ns()
        time_entre =  now - time_prev_s1
        vel_s1b1s2b2[0] = 600000000/time_entre
        time_prev_s1 = now
        
        
    if flanco_bajada(m1_enc1.value(), enc1_prev):
        now = time_ns()
        time_entre =  now - time_prev_b1
        vel_s1b1s2b2[1] = 600000000/time_entre
        time_prev_b1 = now
        
    if flanco_subida(m1_enc2.value(), enc2_prev):
        now = time_ns()
        time_entre =  now - time_prev_s2
        vel_s1b1s2b2[2] = 600000000/time_entre
        time_prev_s2 = now
        
        
    if flanco_bajada(m1_enc2.value(), enc2_prev):
        now = time_ns()
        time_entre =  now - time_prev_b2
        vel_s1b1s2b2[3] = 600000000/time_entre
        time_prev_b2 = now
        
    vel = (vel_s1b1s2b2[0] + vel_s1b1s2b2[1] + vel_s1b1s2b2[2] + vel_s1b1s2b2[3])/4
    if vel != vel_prev:
        print(f"vel ref: {vel_ref} RPM, vel actual: {int(vel)} RPM, duty: {int(duty)}%")
    vel_prev = vel     
    enc1_prev = m1_enc1.value()  
    enc2_prev = m1_enc2.value()  
    
    
