import socket

def enviar_pedido(plato):
    # REQUISITO: Comunicación por Sockets
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 8888))
    cliente.send(plato.encode())
    
    respuesta = cliente.recv(1024).decode()
    print(f"Respuesta del servidor: {respuesta}")
    cliente.close()

if __name__ == "__main__":
    menu = ["Burger XL", "Pizza BBQ", "Tacos", "Ensalada"]
    for plato in menu:
        enviar_pedido(plato)