"""
Libreria para el control de actuadores del robot IRB.

"""
##### Librerias #####

from machine import Pin , PWM
from time import sleep, sleep_ms, ticks_us
import network


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


##### Definicion de funciones ####
    
def StopMotor(m1, m2, pwm):
    m1.value(0)
    m2.value(0)
    pwm.duty_u16(0)


def stop():
    StopMotor(d1_ina1, d1_ina2, d1_pwma)
    StopMotor(d2_ina1, d2_ina2, d2_pwma)

##### Main #####

d1_pwma.freq(1000)      ### Averiguar sobre esta linea ###
d1_stby.value(1)        # Enable the motor driver 1
d2_pwma.freq(1000)
d2_stby.value(1)        # Enable the motor driver 2

led.off()            # Encender el LED para indicar que el programa ha iniciado

stop()
wlan = network.WLAN(network.STA_IF)
wlan.disconnect()