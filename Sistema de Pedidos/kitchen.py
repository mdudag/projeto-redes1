import socket   
import json     

def kitchen_client():
    """
        Função referente ao totem da cozinha, onde o servidor envia as informações dos pedidos,
        e o "cliente cozinha" marca os pedidos como concluídos ou cancelados. Por fim envia a atualização 
        de leitura do pedido ao servidor.
    """

    # Endereço para se comunicar ao servidor
    host = '127.0.0.1'  
    port = 65432        

    print("\n+=============== TOTEM DA COZINHA ===============+")

    # Criando objeto socket com tipo de endereço de rede IPv4 e protocolo TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("\n Conectado ao Servidor")

        # Envio da mensagem que registra no servidor como área de preparo
        register_message = {'type': 'register', 'role': 'kitchen'}
        s.send(json.dumps(register_message).encode('utf-8'))

        while True:
            data = s.recv(1024).decode('utf-8')
            message = json.loads(data)

            # Mensagem do tipo novo pedido
            if message['type'] == 'new_order':  
                order = message['order']
                
                print("\n ------------------ Novo Pedido -----------------"
                      f"\n\n Número: {order['id']}"
                      f"\n Item: {order['item']}\n")

                while True: # Enquanto as opções de marcação do pedido não foram selecionadas
                    ready = input(f" Marcar pedido {order['id']} como concluído? (s/n): ")

                    if ready.lower() == 's':
                        print(" Pedido concluído!")

                        # Mensagem de atualização do pedido concluído
                        update_message = {'type': 'update_order', 'order_id': order['id']}
                        break
                    elif ready.lower() == 'n': 
                        print(" Pedido cancelado.")

                        # Mensagem de atualização do pedido cancelado
                        update_message = {'type': 'canceled_order', 'order_id': order['id']}
                        break

                # Envia uma mensagem de pedido atualizado ao servidor
                s.send(json.dumps(update_message).encode('utf-8'))

if __name__ == "__main__":  # Se o arquivo for executado diretamente
    kitchen_client()        # Chama função para executar o totem da cozinha
