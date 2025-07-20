"""
Libreria para el control de actuadores del robot IRB.

"""
##### Librerias #####

from machine import Pin , PWM
from time import sleep, sleep_ms, ticks_us, time_ns


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
    
def flanco_subida(bit, bit_prev):
    if not bit_prev and bit:
        return True
    return False

def flanco_bajada(bit, bit_prev):
    if bit_prev and not bit:
        return True
    return False

def vel_encoders(enc1, enc2, enc1_prev, enc2_prev, time_prev):
    '''
    Esta función calculará la velocidad del motor utilizando los flancos de subida y de bajada de los encoders, luego tomará un promedio de estas.
    Para determinar la dirección de giro utilizará el desface de ambos encoders.
    '''
    dif_time = time_ns() - time_prev
    time_entre_subida_1 += dif_time
    time_entre_subida_2 += dif_time
    time_entre_bajada_1 += dif_time
    time_entre_bajada_2 += dif_time
    
    if flanco_subida(enc1, enc1_prev):
        vel_subida_1 = 1
    
    pass
    
    

##### Main #####

d1_pwma.freq(1000)      ### Averiguar sobre esta linea ###
d1_stby.value(1)        # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)        # Enable the motor driver 2

led.toggle()            # Encender el LED para indicar que el programa ha iniciado

# while True:
#     txt = input()
#     if txt == "s":
#         stop()
#         break
    
#     elif txt == "f":
#         duty_cycle = min(int(input("Ingrese el ciclo de trabajo (0-100): ")), 100)
#         forward(duty_cycle)
        
#     elif txt == "b":
#         duty_cycle = min(int(input("Ingrese el ciclo de trabajo (0-100): ")), 100)
#         backward(duty_cycle)



# Close Loop Motor 1
vel_ref = 60 # Velocidad de referencia [RPM]
vel_lectura = 0

## Parametros Controlador
Kp = 0.1 # Ganancia proporcional
Ki = 0.005 # Ganancia integral
Kd = 0 # Ganancia derivativa

error = 0
error_prev = 0
integral = 0
duty = 0

delay = 0.002

prev_enc_value = 1
encoder_count = 0

tiempo_entre_enc = delay


while True:
    print(f"vel actual: {vel_lectura}, vel ref: {vel_ref}, duty: {duty}")


    # cuenta rotaciones del encoder
    if prev_enc_value == 0 and m2_enc2.value() == 1:          # 1Rotacion = 100 Flancos de subida
        encoder_count += 1
    
    # rotaciones > 100 ->   
    if encoder_count > 100:
        vel_lectura = 60/tiempo_entre_enc                     # [RPM]
        
        # reset
        tiempo_entre_enc = delay
        encoder_count = 0

    else:
        tiempo_entre_enc += delay
        
    prev_enc_value = m2_enc2.value()
    
    # Calculo parametros ajuste
    error =  vel_ref - vel_lectura
    derivativo = (error - error_prev)/delay
    integral += error

    duty += Kp*error + Ki*integral + Kd*derivativo      # Calcula el porcentaje de PWM necesario
    duty = min(max(duty, 8), 100)                    # Se asegura de no sobrepasar el 100% de la PWM
    
    # print(duty)
    if duty >= 0:
        duty = max(duty, 10)
        RotateCCW(duty, d2_ina1, d2_ina2, d2_pwma)
    # else:
    #     duty = min(duty, -10)
    #     RotateCW(-duty, d2_ina1, d2_ina2, d2_pwma)
        
    error_prev = error
    sleep(delay)


stop()
led.toggle()            # Apagar el LED para indicar que el programa ha terminado