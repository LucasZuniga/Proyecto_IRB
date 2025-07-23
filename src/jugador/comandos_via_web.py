##### Librerias ####

import network
import socket
import time
import urequests as requests
import rp2
import sys
from machine import Pin, PWM
from time import sleep, sleep_ms, ticks_us, time_ns
from jugador.control_lib import *
import _thread


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

d1_pwma.freq(1000)      ### Averiguar sobre esta linea ###
d1_stby.value(1)        # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)        # Enable the motor driver 2


##### Wifi Functions #####

# Wifi
ssid = 'Lucas'
password = '1234567890'


def connect():
    # Connect ro WLAN
    rp2.country('CL')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        if rp2.bootsel_button():
            sys.exit()
        print('Wating for connection...')
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f'Conected on {ip}')
    led.on()
    return ip
    


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
    

def webpage(state):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Proyecto IRB</title>
            </head>
            <body>
            <form action="./forward">
            <input type="submit" value="Forward" />
            </form>
            <form action="./backward">
            <input type="submit" value="Backward" />
            </form>
            <form action="./stop">
            <input type="submit" value="Stop" />
            </form>
            <form action="./close">
            <input type="submit" value="Stop server" />
            </form>
            <p>Vel Referencia: {state} RPM</p>
            <p>Vel Actual: {"Soon"} RPM</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    # Start a web server
    led.on()
    duty = 30
    state = "0"
    
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == "/forward?":
            forward(duty, d1_ina1, d1_ina2, d1_pwma, duty, d2_ina1, d2_ina2, d2_pwma)
            state = "+"
        elif request == "/backward?":
            backward(duty, d1_ina1, d1_ina2, d1_pwma, duty, d2_ina1, d2_ina2, d2_pwma)
            state = "-"
        elif request == "/stop?":
            stop(d1_ina1, d1_ina2, d1_pwma, d2_ina1, d2_ina2, d2_pwma)
            state = "0"
        elif request == "/close?":
            sys.exit()

        html = webpage(state)
        client.send(html)
        client.close()


##### Main #####    

ip = connect()
connection = open_socket(ip)
serve(connection)
