"""
Libreria para el control de actuadores del robot IRB.

"""
##### Librerias #####


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