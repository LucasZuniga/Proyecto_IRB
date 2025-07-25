import socket
import threading
import time

clientes = []
# serv_vel_1_r = 0
# serv_vel_1_l = 0
vels_1 = 0

def iniciar_servidor():
    # global serv_vel_1_r
    # global serv_vel_1_l
    global vels_1
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(5)
    print("[Incializado servidor:] escuchando nuevos sockets:")

    while True:
        client_socket, client_address = server_socket.accept()
        # se crea un hilo para manejar a cada cliente
        client_thread = threading.Thread(target=manejar_cliente, args=(client_socket, client_address))
        client_thread.start()
        
def manejar_cliente(client_socket, client_address):
    print(f"[Conexión nueva establecida: ] Cliente {client_address} conectado.")
    clientes.append(client_socket)
    conectado = True
    while conectado: # cuando esta conectado verifica para responder mensajes
        try:
            enviar_a_todos(vels_1)
            time.sleep(0.5)
        except:
            conectado = False
            clientes.remove(client_socket)
            client_socket.close()# se cierra el socket
            print(f"[Desconectado: ] Cliente {client_address} desconectado.")# al cerrrse enviamos el mesnaje de desconexion

# en esta función enviamso un mensaje a todos los clientes conectados, excepto al que lo envió
def enviar_a_todos(mensaje):
    for cliente in clientes:
        try:
            cliente.send(mensaje.encode('utf-8'))
        except:
            # Si no se puede enviar el mensaje (cliente desconectado), eliminarlo
            clientes.remove(cliente)
                
               
def actualizar_vel():
    # global serv_vel_1_r
    # global serv_vel_1_l
    global vels_1
    time.sleep(2)
    while True:
        vels_1 = input("Idique las velocidades en rpm separadas por una coma ")
        # serv_vel_1_r, serv_vel_1_l = vels.split(",")

if __name__ == "__main__":
    # Inicializa el Thread en el que se calculan las velocidades necesarias
    vel_thread = threading.Thread(target=actualizar_vel)
    vel_thread.start()
    
    # Un segundo Thread (principal), se encarga de levantar el servidor y enviar las velocidades a los robots
    iniciar_servidor()