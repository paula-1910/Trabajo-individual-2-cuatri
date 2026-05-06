import asyncio
import multiprocessing
import time

# Recurso compartido: La Plancha
plancha_lock = multiprocessing.Lock()

def proceso_cocinero(id_cocinero, cola):
    """Paralelismo real: Cada cocinero es un proceso"""
    while True:
        pedido = cola.get()
        if pedido == "STOP": break
        
        print(f" Cocinero {id_cocinero} preparando: {pedido}")
        time.sleep(2) # Tiempo de preparación
        
        with plancha_lock: # Exclusión mutua
            print(f" Cocinero {id_cocinero} usando PLANCHA para {pedido}")
            time.sleep(1)
        
        print(f" {pedido} LISTO (Cocinero {id_cocinero})")

async def manejar_cliente(reader, writer, cola):
    """Asincronía: Maneja múltiples clientes sin bloquearse"""
    data = await reader.read(100)
    pedido = data.decode().strip()
    addr = writer.get_extra_info('peername')
    
    print(f" Pedido recibido de {addr}: {pedido}")
    cola.put(pedido) # Enviamos el pedido a los cocineros
    
    writer.write(f"Pedido '{pedido}' recibido y en cocina.".encode())
    await writer.drain()
    writer.close()

async def main():
    cola_pedidos = multiprocessing.Queue()
    
    # Lanzar 3 procesos cocineros
    for i in range(3):
        multiprocessing.Process(target=proceso_cocinero, args=(i, cola_pedidos)).start()

    # REQUISITO: Servidor concurrente con Asyncio
    server = await asyncio.start_server(
        lambda r, w: manejar_cliente(r, w, cola_pedidos), '127.0.0.1', 8888)

    print(" Gran Cocina Distribuida abierta en 127.0.0.1:8888")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCerrando cocina...")