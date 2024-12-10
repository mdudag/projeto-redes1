import socket   
import json     

def ready_area_client():
    """
        Função referente ao totem de visualização de pedidos prontos, onde o servidor envia a mensagem com o número
        do pedido finalizado, e o "cliente totem de prontos" mostra uma mensagem informando o número do pedido.
    """

    # Endereço para se comunicar ao servidor
    host = '127.0.0.1'  
    port = 65432        

    print("\n+========== TOTEM DE PEDIDOS PRONTOS ==========+")

    # Criando objeto socket com tipo de endereço de rede IPv4 e protocolo TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Método de conexão para o cliente se conectar ao servidor
        s.connect((host, port)) # Recebe uma tupla contendo o endereço do servidor
        print("\n Conectado ao Servidor")
        print("\n ------------- Pedidos Finalizados ------------\n")

        # Envio da mensagem que registra no servidor como área de pedidos prontos
        register_message = {'type': 'register', 'role': 'ready_area'}
        s.send(json.dumps(register_message).encode('utf-8'))

        while True:
            data = s.recv(1024).decode('utf-8')
            message = json.loads(data)

            # Mensagem do tipo pedido pronto
            if message['type'] == 'order_ready':
                print(f"\t     * Pedido de número {message['order_id']} *")


if __name__ == "__main__":
    ready_area_client()
