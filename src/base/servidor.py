import socket
import threading

# Aca creamos uan lista ARRAY para almacenar los sockets de los clientes conectados ya que se pueden conectar multiples
clientes = []

# en esta función  manejamos los clientes conetados de manera individual
def manejar_cliente(client_socket, client_address):
    print(f"[Conexión nueva establecida: ] Cliente {client_address} conectado.")
    clientes.append(client_socket)
    conectado = True
    while conectado: # cuando esta conectado verifica para responder mensajes
        try:
            msg = client_socket.recv(1024).decode('utf-8') # guaramosmos en la variable msg el mensaje con utf8 para todos carateres
            if msg:
                print(f"[{client_address}] {msg}")#imprmimos quien envia el mensaje para indentificar y luego el mensaje concatenado
                # Aca respndemos al cliente que envió el mensaje
                client_socket.send("Mensaje recibido por el servidor".encode('utf-8'))

                # el mensaje llega a todos los demás clientes conectados
                enviar_a_todos(msg, client_socket)
            else:
                conectado = False
        except:
            conectado = False
            clientes.remove(client_socket)
            client_socket.close()# se cierra el socket
            print(f"[Desconectado: ] Cliente {client_address} desconectado.")# al cerrrse enviamos el mesnaje de desconexion

# en esta función enviamso un mensaje a todos los clientes conectados, excepto al que lo envió
def enviar_a_todos(mensaje, cliente_actual):
    for cliente in clientes:
        if cliente != cliente_actual:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                # Si no se puede enviar el mensaje (cliente desconectado), eliminarlo
                clientes.remove(cliente)

# aca en esta función inicializamos el servidor con una ip y socket establecido la cual los clientes se conectaras
def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8080))
    server_socket.listen(5)
    print("[Incializado servidor:] escuchando nuevos sockets:")

    while True:
        client_socket, client_address = server_socket.accept()
        # se crea un hilo para manejar a cada cliente
        client_thread = threading.Thread(target=manejar_cliente, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    iniciar_servidor()