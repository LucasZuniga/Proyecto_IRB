"""
Libreria para coneccion a internet
"""
import network
import rp2
import uasyncio
from machine import Pin

from time import sleep_ms

led = Pin("LED", Pin.OUT)

# Funcion que conecta a WiFi
def connect(ssid, password, wlan):
    # Connect ro WLAN
    rp2.country('CL')
    wlan.PM_PERFORMANCE
    wlan.active(True)
    wlan.connect(ssid, password)
    return wlan

# Funcion que avisa en caso de desconeccion
async def check_wifi(ssid, password, wlan, led):
    connect(ssid, password, wlan)
    while True:
        try:
            while not wlan.isconnected():
                print("Wating for connection...")
                led.toggle()
                await uasyncio.sleep_ms(500)
                
            ip = wlan.ifconfig()[0]
            print(f'Conected on {ip}')
            
            while wlan.isconnected():
                led.on()
                await uasyncio.sleep_ms(500)
                
        except KeyboardInterrupt:
            print("WiFi conecction close")
            led.off()
            break
            
        await uasyncio.sleep_ms(100)
    
### Main program to test WiFi connection ###
if __name__ == "__main__":
    # WiFi inputs
    ssid = 'Lucas'
    password = '1234567890'
    
    wlan = network.WLAN(network.STA_IF)
    
    try:
        uasyncio.run(check_wifi(ssid, password, wlan, led))
    
    finally:
        uasyncio.new_event_loop()

        