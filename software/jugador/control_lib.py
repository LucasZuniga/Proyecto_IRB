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
    
def backward(duty_1, d1_ina1, d1_ina2, d1_pwma, duty_2, d2_ina1, d2_ina2, d2_pwma):
    RotateCW(duty_1, d1_ina1, d1_ina2, d1_pwma)
    RotateCCW(duty_2, d2_ina1, d2_ina2, d2_pwma)

def forward(duty_1, d1_ina1, d1_ina2, d1_pwma, duty_2, d2_ina1, d2_ina2, d2_pwma):
    RotateCCW(duty_1, d1_ina1, d1_ina2, d1_pwma)
    RotateCW(duty_2, d2_ina1, d2_ina2, d2_pwma)
    
def move(duty_1, d1_ina1, d1_ina2, d1_pwma, duty_2, d2_ina1, d2_ina2, d2_pwma):
    if duty_1 >= 0:
        RotateCCW(duty_1, d1_ina1, d1_ina2, d1_pwma)
    else:
        RotateCW(-duty_1, d1_ina1, d1_ina2, d1_pwma)
        
    if duty_2 >= 0:
        RotateCW(duty_2, d2_ina1, d2_ina2, d2_pwma)
    else:
        RotateCCW(-duty_2, d2_ina1, d2_ina2, d2_pwma)
                
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

def C_PID(duty, dt, vel_ref, vel_actual, Kp, Ki, Kd, integral, error_prev):
    error = vel_ref - vel_actual
    integral += error
    integral = min(max(integral, -200), 200)              # Unwind, ponemos un maximo al integral para evitar problemas por acumulacion
    deriv = (error-error_prev)/dt
    duty += Kp*error + Ki*integral + Kd*deriv
    duty = min(max(-100, duty), 100)
    
    return duty, error, integral