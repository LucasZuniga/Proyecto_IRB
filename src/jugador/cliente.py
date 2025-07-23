import socket

# para recibir los mensajdes del servidor ceramos esta funcion
def recibir_mensajes(client_socket):
    while True:
        try:
            mensaje = client_socket.recv(1024).decode('utf-8') # se guarda el mensaje en la variable mensaje codificado con utf8
            if mensaje:
                print(f"{mensaje}")
        except:
            print("Conexión cerrada.")
            break

# aca iniciamos el cliente con esta función principal
def iniciar_cliente(ip, puerto, nombre_cliente):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, puerto)) # aca establecemos la conecion acuerdo la informacion suminstrada por el
        print("Conectado al servidor.")

        # Enviar nombre o ID al servidor
        client_socket.send(nombre_cliente.encode('utf-8'))
        
        recibir_mensajes(client_socket)


        client_socket.close()
    except Exception as e:
        print(f"Error al conectar: {e}")




if __name__ == "__main__":
    
    ip = input("Introduce la IP del servidor: ")
    puerto = int(input("Introduce el puerto del servidor: "))
    nombre_cliente = input("Introduce tu nombre o ID: ")       # pedimos el nombre del cliente conectado para que se pueda identificar

    iniciar_cliente(ip, puerto, nombre_cliente)