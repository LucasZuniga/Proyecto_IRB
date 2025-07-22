import network
import socket
import time
import urequests as requests
import machine
import rp2
import sys

ssid = 'Lucas'
password = '1234567890'

# LED
led = machine.Pin("LED", machine.Pin.OUT)

def connect():
    # Connect ro WLAN
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
    
    
def webpage(temp, state):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <form action="./close">
            <input type="submit" value="Stop server" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temp}</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    # Start a web server
    state = "ON"
    led.on()
    temp = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == "/lighton?":
            led.on()
            state = "ON"
        elif request == "/lightoff?":
            led.off()
            state = "OFF"
        elif request == "/close?":
            sys.exit()
        html = webpage(temp, state)
        client.send(html)
        client.close()


ip = connect()
connection = open_socket(ip)
serve(connection)
