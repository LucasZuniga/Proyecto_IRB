"""
Libreria para el control de actuadores del robot IRB.

"""
##### Librerias #####

from machine import Pin , PWM
from time import sleep, sleep_ms, ticks_us, time_ns

##### Funciones ####

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
    
def backward(duty, d1_ina1, d1_ina2, d1_pwma, d2_ina1, d2_ina2, d2_pwma):
    RotateCW(duty, d1_ina1, d1_ina2, d1_pwma)
    RotateCCW(duty, d2_ina1, d2_ina2, d2_pwma)

def forward(duty, d1_ina1, d1_ina2, d1_pwma, d2_ina1, d2_ina2, d2_pwma):
    RotateCCW(duty, d1_ina1, d1_ina2, d1_pwma)
    RotateCW(duty, d2_ina1, d2_ina2, d2_pwma)
    
def stop(d1_ina1, d1_ina2, d1_pwma, d2_ina1, d2_ina2, d2_pwma):
    StopMotor(d1_ina1, d1_ina2, d1_pwma)
    StopMotor(d2_ina1, d2_ina2, d2_pwma)
    
# def rodillo_in(duty):
#     d2_inb1.value(1)
#     d2_inb2.value(0)
#     duty_16 = int((duty*65535)/100)
#     d2_pwmb.duty_u16(duty_16)

# def rodillo_out(duty):
#     d2_inb1.value(0)
#     d2_inb2.value(1)
#     duty_16 = int((duty*65535)/100)
#     d2_pwmb.duty_u16(duty_16)
    
# def rodillo_stop():
#     d2_inb1.value(0)
#     d2_inb2.value(0)
#     d2_pwmb.duty_u16(0)

# def solenoid_on():
#     sol.value(1)

# def solenoid_off():
#     sol.value(0)
    
def flanco_subida(bit, bit_prev):
    if not bit_prev and bit:
        return True
    return False

def flanco_bajada(bit, bit_prev):
    if bit_prev and not bit:
        return True
    return False

# def vel_encoders(enc1, enc2, enc1_prev, enc2_prev, time_prev):
#     '''
#     Esta función calculará la velocidad del motor utilizando los flancos de subida y de bajada de los encoders, luego tomará un promedio de estas.
#     Para determinar la dirección de giro utilizará el desface de ambos encoders.
#     '''
#     dif_time = time_ns() - time_prev
#     time_entre_subida_1 += dif_time
#     time_entre_subida_2 += dif_time
#     time_entre_bajada_1 += dif_time
#     time_entre_bajada_2 += dif_time
    
#     if flanco_subida(enc1, enc1_prev):
#         vel_subida_1 = 1
    
#         pass