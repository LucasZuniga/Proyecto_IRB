import socket
# import uasyncio

def iniciar_cliente(ip, puerto, nombre_cliente):
    global vel_ref_1
    global vel_ref_2
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, puerto))
    print("Conectado al servidor.")

    # Enviar nombre o ID al servidor
    client_socket.send(nombre_cliente.encode('utf-8'))
    
    while True:
        try:
            mensaje = client_socket.recv(1024).decode('utf-8')
            if mensaje:
                vel_ref_1, vel_ref_2 = mensaje.split(",")
                print(f"vel 1 r: {vel_ref_1} RPM, vel 1 r: {vel_ref_2} RPM")
        except:
            print("Conexión cerrada.")
            break



if __name__ == "__main__":
    
    ip = input("Introduce la IP del servidor: ")
    puerto = int(input("Introduce el puerto del servidor: "))
    nombre_cliente = input("Introduce tu nombre o ID: ")

    iniciar_cliente(ip, puerto, nombre_cliente)
    
        
