from machine import Pin
from utime import sleep

def pin(l,in_out):
    return Pin(l, in_out)

led = pin("LED", Pin.OUT)

print("LED starts flashing...")
while True:
    try:
        led.toggle()
        sleep(0.1) # sleep 1sec
    except KeyboardInterrupt:
        break
led.off()
print("Finished.")
