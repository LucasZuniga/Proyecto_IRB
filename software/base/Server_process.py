import socket
import threading
import time
import keyboard
import multiprocessing
from clases import Robot, Controlable_Robot, Ball


# clientes = []
# vels_1 = 0

# ## Servidor ##
# def server_process(robots_list):
#     clientes = []
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(("0.0.0.0", 8080))
#     server_socket.listen(5)
#     print("[Incializado servidor:] escuchando nuevos sockets:")
    
#     # Envia las velocidades
#     vel_thread = threading.Thread(target=enviar_vel(robots_list))
#     vel_thread.start()

#     while True:
#         # Agrega clientes nuevos
#         client_socket, client_address = server_socket.accept()
#         new = True
#         client_id = client_socket.recv(1024).decode('utf-8')
#         for cliente in clientes:
#             if client_address[0] == cliente[1]:
#                 print("")
#                 print(f"Cliente {client_id} reconectado")
#                 new = False
#                 clientes.remove(cliente)
#         if new:
#             print("")
#             print(f"[Conexión nueva establecida] Cliente {client_id}, IP {client_address[0]} conectado")
            
#         clientes.append([client_socket, client_address[0], client_address[1], client_id])
        
# # Envia velocidades a clientes en caso de haber cambiado
# def enviar_vel(robots_list):
#     r = robots_list[0]
#     vels_1 = f"{r.vel_r}, {r.vel_l}, {r.solenoide}, {r.rodillo}"
#     vels_1_prev= vels_1
    
#     while True:
#         if vels_1 != vels_1_prev:
#             enviar_a_todos(vels_1)
#             vels_1_prev = vels_1
            
# # en esta función enviamso un mensaje a todos los clientes conectados, excepto al que lo envió
# def enviar_a_todos(mensaje):
#     for cliente in clientes:
#         try:
#             cliente[0].send(mensaje.encode('utf-8'))   
#         except:
#             # Si no se puede enviar el mensaje (cliente desconectado), eliminarlo
#             clientes.remove(cliente)

import socket
import time

def server_process(robots_list):
    # Configuración del socket servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(5)
    
    # IMPORTANTE: Hace que el socket no se quede esperando (no bloqueante)
    server_socket.setblocking(False)
    
    print("[Inicializado servidor:] Modo No Bloqueante")
    
    clientes = []  # Lista local de clientes: [socket, ip, port, id]
    vels_prev = ""

    while True:
        # --- 1. INTENTAR ACEPTAR NUEVOS CLIENTES (Sin bloquear) ---
        try:
            client_socket, client_address = server_socket.accept()
            # Una vez aceptado, el socket del cliente también puede ser no bloqueante
            client_socket.setblocking(False)
            
            # Recibir ID (con timeout pequeño para no trabar el loop)
            time.sleep(0.1) 
            client_id = client_socket.recv(1024).decode('utf-8')
            
            # Limpiar si el ID ya existía (reconexión)
            clientes = [c for c in clientes if c[3] != client_id]
            
            print(f"[Conexión nueva] Cliente {client_id}, IP {client_address[0]}")
            clientes.append([client_socket, client_address[0], client_address[1], client_id])
            
        except BlockingIOError:
            # No hay clientes nuevos intentando entrar, seguimos adelante
            pass
        except Exception as e:
            # Otros errores (como problemas al recibir el ID)
            pass

        # --- 2. PREPARAR Y ENVIAR VELOCIDADES ---
        r = robots_list[0]
        # Construimos el mensaje con el estado actual del proxy
        vels_actual = r.get_server_data()
        
        # Solo enviamos si algo cambió para no saturar la red
        if vels_actual != vels_prev:
            
            # Enviamos a todos los clientes conectados
            for cliente in clientes[:]: # Usamos copia [:] para poder remover si falla
                try:
                    cliente[0].send(vels_actual.encode('utf-8'))
                except:
                    print(f"[Desconectado] Cliente {cliente[3]}")
                    clientes.remove(cliente)
            
            vels_prev = vels_actual

        # Pequeña pausa para no consumir 100% de CPU
        time.sleep(0.01)


#-----------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    robots_list = {
        0 : Controlable_Robot(0, True),
        1 : Robot(1, False)
        } 
    
    # # Un segundo Thread (principal), se encarga de levantar el servidor y enviar las velocidades a los robots
    server_process(robots_list)