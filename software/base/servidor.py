import socket
import threading
import time
import keyboard


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
            # print(f"lista de clientes: {clientes[:][3]}")
            
        clientes.append([client_socket, client_address[0], client_address[1], client_id])
        
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
        
def actualizar_vel_keyboard():
    global vels_1
    rodillo = False
    while True:
        vel_r = 0
        vel_l = 0
        sol = 0
        if keyboard.is_pressed("w"):
            vel_r, vel_l = 50, 50
            # print("alante")
        
        elif keyboard.is_pressed("s"):
            vel_r, vel_l = -50, -50
            # print("atras")
        
        elif keyboard.is_pressed("a"):
            vel_r, vel_l = -50, 50
            # print("izq")
        
        elif keyboard.is_pressed("d"):
            vel_r, vel_l = 50, -50
            # print("derch")
            
        elif keyboard.is_pressed("SPACE"):
            sol = 1
            # print("sol")
            
        elif keyboard.is_pressed("r"):
            rodillo = not rodillo

        elif keyboard.is_pressed("e"):
            break
        
        vels_1 = str(vel_r) + ", " + str(vel_l) + ", " + str(sol) + ", " + str(int(rodillo))
        print(vels_1)
        
        time.sleep(0.15)


#-----------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    # Inicializa el Thread en el que se calculan las velocidades necesarias
    vel_thread = threading.Thread(target=actualizar_vel_keyboard)
    vel_thread.start()
    
    # Un segundo Thread (principal), se encarga de levantar el servidor y enviar las velocidades a los robots
    iniciar_servidor()