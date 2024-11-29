import socket   # Importando módulo socket para criar a comunicação de rede entre cliente e servidor
import json     # Importando módulo JSON para trabalhar com dados no formato JavaScript Object Notation

def ready_area_client():
    """
        Função referente ao totem de visualização de pedidos prontos, onde o servidor envia a mensagem com o número
        do pedido finalizado, e o "cliente totem de prontos" mostra uma mensagem informando o número do pedido.
    """

    host = '127.0.0.1'  # Endereço IP local utilizado para se conectar
    port = 65432        # Porta arbitrária para estabelecer uma conexão entre o cliente e o servidor

    print("\n+========== TOTEM DE PEDIDOS PRONTOS ==========+")

    # Criando objeto socket com dois parâmentros
        # AF_INET: define que o IPv4 é o tipo de endereço de rede utilizado
        # SOCK_STREAM: define que o TCP é o tipo de protocolo utilizado
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Método de conexão para o cliente se conectar ao servidor
        s.connect((host, port)) # Recebe uma tupla contendo o endereço do servidor
        print("\n Conectado ao Servidor")
        print("\n ------------- Pedidos Finalizados ------------\n")

        # Registra no servidor como área de pedidos prontos
        register_message = {'type': 'register', 'role': 'ready_area'}
        s.send(json.dumps(register_message).encode('utf-8'))    # Envia a mensagem codificada ao servidor

        while True:
            # 1024: especifica o tamanho máximo do dado, em bytes, que será recebido por vez
            data = s.recv(1024).decode('utf-8') # Recebendo os dados do servidor e decodificando de bytes para string
            message = json.loads(data)  # Convertendo os dados em string JSON em objeto python

            if message['type'] == 'order_ready':    # Se for uma mensagem de pedido pronto
                print(f"\t     * Pedido de número {message['order_id']} *")


if __name__ == "__main__":  # Se o arquivo for executado diretamente
    ready_area_client()     # Chama função para executar o totem dos pedidos dos clientes
