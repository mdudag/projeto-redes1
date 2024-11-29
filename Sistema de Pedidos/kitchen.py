import socket   # Importando módulo socket para criar a comunicação de rede entre cliente e servidor
import json     # Importando módulo JSON para trabalhar com dados no formato JavaScript Object Notation

def kitchen_client():
    """
        Função referente ao totem da cozinha, onde o servidor envia as informações dos pedidos,
        e o "cliente cozinha" marca os pedidos como concluídos ou cancelados. Por fim envia a atualização 
        de leitura do pedido ao servidor.
    """

    # Endereço do servidor
    host = '127.0.0.1'  # Endereço IP local utilizado para se conectar
    port = 65432        # Porta arbitrária para estabelecer uma conexão entre o cliente e o servidor

    print("\n+=============== TOTEM DA COZINHA ===============+")

    # Criando objeto socket com dois parâmentros
        # AF_INET: define que o IPv4 é o tipo de endereço de rede utilizado
        # SOCK_STREAM: define que o TCP é o tipo de protocolo utilizado
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Método de conexão para o cliente se conectar ao servidor
        s.connect((host, port)) # Recebe uma tupla contendo o endereço do servidor
        print("\n Conectado ao Servidor")

        # Registra no servidor como área de preparo
        register_message = {'type': 'register', 'role': 'kitchen'}

        # Enviando ao servidor os dados convertidos a uma string JSON e depois a uma sequência de bytes
        s.send(json.dumps(register_message).encode('utf-8'))

        while True:
            # 1024: especifica o tamanho máximo do dado, em bytes, que será recebido por vez
            data = s.recv(1024).decode('utf-8') # Recebendo os dados do servidor e decodificando de bytes para string
            message = json.loads(data)  # Convertendo os dados em string JSON em objeto python

            if message['type'] == 'new_order':  # Se for uma mensagem de novo pedido
                order = message['order']        # Guardar as informações do pedido
                
                print("\n ------------------ Novo Pedido -----------------"
                      f"\n\n Número: {order['id']}"
                      f"\n Item: {order['item']}\n")

                while True: # Enquanto as opções de marcação do pedido não foram selecionadas
                    ready = input(f" Marcar pedido {order['id']} como concluído? (s/n): ")

                    if ready.lower() == 's':    # Se o pedido for marcado como concluído
                        print(" Pedido concluído!")

                        # Criando mensagem de atualização do pedido concluído
                        update_message = {'type': 'update_order', 'order_id': order['id']}
                        break
                    elif ready.lower() == 'n': 
                        print(" Pedido cancelado.")

                        # Criando mensagem de atualização do pedido cancelado
                        update_message = {'type': 'canceled_order', 'order_id': order['id']}
                        break

                # Envia uma nova mensagem ao servidor
                s.send(json.dumps(update_message).encode('utf-8'))

if __name__ == "__main__":  # Se o arquivo for executado diretamente
    kitchen_client()        # Chama função para executar o totem da cozinha
