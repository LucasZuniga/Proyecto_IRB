import socket
import threading
import time

clientes = []
vels_1 = 0

## Servidor ##
def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(5)
    print("[Incializado servidor:] escuchando nuevos sockets:")
    
    # Envia las velocidades
    vel_thread = threading.Thread(target=enviar_vel)
    vel_thread.start()

    while True:
        # Agrega clientes nuevos
        client_socket, client_address = server_socket.accept()
        new = True
        for cliente in clientes:
            if client_address[0] == cliente[1]:
                print(f"Cliente {client_address[0]} reconectado")
                new = False
                clientes.remove(cliente)
        if new:
            print(f"[Conexión nueva establecida: ] Cliente {client_address} conectado")
            print(f"lista de clientes: {clientes}")
            
        clientes.append([client_socket, client_address[0], client_address[1]])
        
# Envia velocidades a clientes en caso de haber cambiado
def enviar_vel():
    global vels_1
    vels_1_prev= vels_1
    
    while True:
        if vels_1 != vels_1_prev:
            enviar_a_todos(vels_1)
            vels_1_prev = vels_1
            
# en esta función enviamso un mensaje a todos los clientes conectados, excepto al que lo envió
def enviar_a_todos(mensaje):
    for cliente in clientes:
        try:
            cliente[0].send(mensaje.encode('utf-8'))
        except:
            # Si no se puede enviar el mensaje (cliente desconectado), eliminarlo
            clientes.remove(cliente)


## Velocidades ##

# Funcion en la que se calculan las nuevas velocidades              
def actualizar_vel():
    # global serv_vel_1_r
    # global serv_vel_1_l
    global vels_1
    time.sleep(2)
    while True:
        print("")
        vels_1 = input("Idique las velocidades en rpm separadas por una coma ")
        # serv_vel_1_r, serv_vel_1_l = vels.split(",")


#-----------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    # Inicializa el Thread en el que se calculan las velocidades necesarias
    vel_thread = threading.Thread(target=actualizar_vel)
    vel_thread.start()
    
    # Un segundo Thread (principal), se encarga de levantar el servidor y enviar las velocidades a los robots
    iniciar_servidor()