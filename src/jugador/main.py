##### Librerias ####

import network
import socket
import _thread
import rp2
import sys
import uasyncio
from machine import Pin, PWM
from time import sleep, sleep_ms, ticks_us, time_ns

# Librerias Propias #
# from cliente import *
from control_lib import *


##### Definicion de pines #####

# LEDS
led = Pin("LED", Pin.OUT)
led_verde = Pin(20, Pin.OUT)
led_amarillo = Pin(19, Pin.OUT)
led_azul = Pin(18, Pin.OUT)

led_azul.off()
led_verde.off()
led_amarillo.off()
led.off()

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

d1_pwma.freq(1000)      ### Averiguar sobre esta linea ###
d1_stby.value(1)        # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)        # Enable the motor driver 2


##### Parametros Iniciales #####

d1_pwma.freq(1000)      ### Averiguar sobre esta linea ###
d1_stby.value(1)        # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)        # Enable the motor driver 2

# velocidades de referencia iniciales
vel_ref_1 = 0
vel_ref_2 = 0

#---------------------------------------------------------------------------
##### Wifi Conection #####

# Funcion que conecta a WiFi
def connect(ssid, password):
    # Connect ro WLAN
    wlan = network.WLAN(network.STA_IF)
    rp2.country('CL')
    wlan.PM_PERFORMANCE
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Wating for connection...')
        led_verde.on()
        sleep_ms(500)
        led_verde.off()
        sleep_ms(500)
        
    led_verde.on()
    ip = wlan.ifconfig()[0]
    print(f'Conected on {ip}')

# Funcion que avisa en caso de desconeccion
async def check_wifi():
    wlan = network.WLAN(network.STA_IF)
    while wlan.isconnected():
        led_verde.on()
        await uasyncio.sleep_ms(500)
    
    led_verde.off()
    StopMotor(d1_ina1, d1_ina2, d1_pwma)
    StopMotor(d2_ina1, d2_ina2, d2_pwma)
    wlan.disconnect()


##### Server Conection #####

# Funcion encargada de crear instancia de cliente y conectarse al servidor
async def iniciar_cliente(ip, puerto, nombre_cliente):
    global vel_ref_1
    global vel_ref_2
    
    print("Iniciando coneccion al servidor...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((ip, puerto))
    led_azul.on()
    print("Conectado al servidor")

    # Enviar nombre o ID al servidor
    server_socket.send(nombre_cliente.encode('utf-8'))
    print("Identificacion enviada")
    
    while True:
        try:
            mensaje = server_socket.recv(1024).decode('utf-8')
            if mensaje:
                print(mensaje)
                vel_rec_1, vel_rec_2 = mensaje.split(",")
                vel_ref_1, vel_ref_2 = int(vel_rec_1), int(vel_rec_2)
                print(f"vel 1 r: {vel_ref_1} RPM, vel 1 r: {vel_ref_2} RPM")
        except KeyboardInterrupt:
            print("Conexión cerrada")
            led_azul.off()
            break
        await uasyncio.sleep_ms(300)
        
        
##### Close Loop #####
        
# Funcion encargada de actualizar constantemente las velocidades
def close_loop():
    global vel_ref_1
    global vel_ref_2
    
    # Motor 1
    vel_lectura_1 = 0
    duty_1 = 20
    m1_enc1_prev = 1
    count_pulses_1 = 0
    count_pulses_1_prev = 0
    Kp_1 = 0.6
    Ki_1 = 0.1
    Kd_1 = 0
    integral_1 = 0
    error_1_prev = 0

    # Motor 2
    vel_lectura_2 = 0
    duty_2 = 20
    m2_enc1_prev = 1
    count_pulses_2 = 0
    count_pulses_2_prev = 0
    Kp_2 = 0.6
    Ki_2 = 0.1
    Kd_2 = 0
    integral_2 =0
    error_2_prev = 0

    led.on()
    calc_vel = 0
    time_prev = time_ns()
    
    while True:
        move(duty_1, d1_ina1, d1_ina2, d1_pwma, duty_2, d2_ina1, d2_ina2, d2_pwma)
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
                count_pulses_2 += 1
            else:
                count_pulses_2 -= 1
                            
        if flanco_bajada(m2_enc1_val, m2_enc1_prev):
            if m2_enc2.value():
                count_pulses_2 -= 1
            else:
                count_pulses_2 += 1
        
        
        if calc_vel % 500 == 0:            
            calc_vel = 0
            # Calcular velocidad
            now = time_ns()
            delta_time = now - time_prev
            # Motor 1
            delta_pulsos_1 = count_pulses_1 - count_pulses_1_prev
            vel_lectura_1 = (87591240)*(delta_pulsos_1/delta_time)         # 87591240 = (60sec = 1 min)*(10^9 nanosec = 1sec)/(685 pulsos = 1 Rev)
            
            # Motor 2
            delta_pulsos_2 = count_pulses_2 - count_pulses_2_prev
            vel_lectura_2 = (87591240)*(delta_pulsos_2/delta_time)
            
            count_pulses_1_prev = count_pulses_1
            count_pulses_2_prev = count_pulses_2
            
            # Controladores
            duty_1, error_1_prev, integral_1 = C_PID(duty_1, delta_time, vel_ref_1, vel_lectura_1, Kp_1, Ki_1, Kd_1, integral_1, error_1_prev)
            duty_2, error_2_prev, integral_2 = C_PID(duty_2, delta_time, vel_ref_2, vel_lectura_2, Kp_2, Ki_2, Kd_2, integral_2, error_2_prev)

            time_prev = time_ns()

        m1_enc1_prev = m1_enc1_val
        m2_enc1_prev = m2_enc1_val
        calc_vel += 1


##### Main Thread Function #####

async def main(ip, puerto, nombre_cliente):
    uasyncio.create_task(check_wifi())
    uasyncio.create_task(iniciar_cliente(ip, puerto, nombre_cliente))
    
    while True:
        await uasyncio.sleep_ms(10)


#---------------------------------------------------------------------------
### Close Loop  [thread 1] ###

second_thread = _thread.start_new_thread(close_loop, ())


### Recibir Velocidades de Referencia de Base y chequear conexion a WiFi [thread 0] ###

# Parametros de la coneccion al servidor y red WiFi

# WiFi
ssid = 'Lucas'
password = '1234567890'
# Servidor
ip_server = '10.165.212.53'
port = 8080
robot_id = "FutBot_1"


connect(ssid, password)

try:
    uasyncio.run(main(ip_server, port, robot_id))
    
finally:
    uasyncio.new_event_loop()