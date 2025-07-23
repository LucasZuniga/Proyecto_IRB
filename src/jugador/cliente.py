import socket
import threading

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
def iniciar_cliente():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Solicitar IP y puerto al usuario
    ip = input("Introduce la IP del servidor: ")
    puerto = int(input("Introduce el puerto del servidor: "))

    try:
        client_socket.connect((ip, puerto)) # aca establecemos la conecion acuerdo la informacion suminstrada por el
        #  usuario ip 192.168.1.1 y el puerto 2020
        print("Conectado al servidor.")

        # Recibimos y mostramos mensajes del servidor o de otros clientes
        recibir_thread = threading.Thread(target=recibir_mensajes, args=(client_socket,))
        recibir_thread.start()

        # Enviar nombre o ID al servidor
        nombre_cliente = input("Introduce tu nombre o ID: ")# pedimos el nombre del cliente conectado para que se pueda identificar
        client_socket.send(nombre_cliente.encode('utf-8'))

        # Enviar mensajes al servidor
        while True:
            msg = input("> ")
            if msg.lower() == 'salir':# al momento de desconectarmos usamos "salir"
                break
            client_socket.send(msg.encode('utf-8'))# tambien codificado en utf8 aunque aca es poco relevante pero por buenas practicas

        client_socket.close()
    except Exception as e:
        print(f"Error al conectar: {e}")

if __name__ == "__main__":
    iniciar_cliente()