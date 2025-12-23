import socket
import threading
import time
import keyboard
import multiprocessing
from clases import Robot, Controlable_Robot, Ball


clientes = []
vels_1 = 0

## Servidor ##
def server_process(robots_list):
    clientes = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(5)
    print("[Incializado servidor:] escuchando nuevos sockets:")
    
    # Envia las velocidades
    vel_thread = threading.Thread(target=enviar_vel, args=(robots_list,))
    vel_thread.start()

    while True:
        # Agrega clientes nuevos
        client_socket, client_address = server_socket.accept()
        new = True
        client_id = client_socket.recv(1024).decode('utf-8')
        for cliente in clientes:
            if client_address[0] == cliente[1]:
                print("")
                print(f"Cliente {client_id} reconectado")
                new = False
                clientes.remove(cliente)
        if new:
            print("")
            print(f"[Conexión nueva establecida] Cliente {client_id}, IP {client_address[0]} conectado")
            
        clientes.append([client_socket, client_address[0], client_address[1], client_id])
        
# Envia velocidades a clientes en caso de haber cambiado
def enviar_vel(robots_list):
    vels_1_prev= "0, 0, 0, 0"
    
    while True:
        r = robots_list[0]
        vels_1 = r.get_server_data()
        
        if vels_1 != vels_1_prev:
            enviar_a_todos(vels_1)
            vels_1_prev = vels_1
            
# en esta función enviamso un mensaje a todos los clientes conectados, excepto al que lo envió
def enviar_a_todos(mensaje):
    print(f"[Enviando a clientes:] {mensaje}")
    for cliente in clientes:
        try:
            cliente[0].send(mensaje.encode('utf-8'))   
        except:
            # Si no se puede enviar el mensaje (cliente desconectado), eliminarlo
            clientes.remove(cliente)


#-----------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    robots_list = {
        0 : Controlable_Robot(0, True),
        1 : Robot(1, False)
        } 
    
    # # Un segundo Thread (principal), se encarga de levantar el servidor y enviar las velocidades a los robots
    server_process(robots_list)