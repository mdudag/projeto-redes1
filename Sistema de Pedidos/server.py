import socket
import threading
import json

# Classe que implementa o servidor da padaria
class ServidorPadaria:
    
    # Construtor do servidor, inicializa a configuração da rede e variáveis internas
    def __init__(self, host='127.0.0.1', porta=65432):
        # Criação de um socket TCP/IP
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind do socket ao endereço e porta fornecidos
        self.socket_servidor.bind((host, porta))
        
        # Coloca o servidor em modo de escuta para até 5 conexões simultâneas
        self.socket_servidor.listen(5)
        
        # Exibe uma mensagem indicando que o servidor está online
        print(f"\nServidor online em {host}:{porta}")

        # Lista para armazenar os pedidos recebidos
        self.pedidos = []
        
        # Dicionário para armazenar os clientes registrados (cozinha e área de prontos)
        self.clientes = {"kitchen": None, "ready_area": None}
        
        # Lock para garantir acesso seguro a recursos compartilhados entre threads
        self.bloqueio = threading.Lock()

    # Função que trata a comunicação com cada cliente
    def tratar_cliente(self, conn, endereco):
        print(f"\nConectado à {endereco}")
        try:
            # Loop contínuo para receber dados do cliente
            while True:
                # Recebe os dados enviados pelo cliente
                dados = conn.recv(1024).decode('utf-8')
                
                # Se não houver dados, encerra a conexão
                if not dados:
                    break
                
                # Converte os dados recebidos de JSON para dicionário Python
                mensagem = json.loads(dados)

                # Processar o registro de novos clientes (cozinha ou área de prontos)
                if mensagem['type'] == 'register':
                    # Registra o cliente no dicionário
                    self.clientes[mensagem['role']] = conn
                    print(f"{mensagem['role']} registrado.")

                # Processar novos pedidos do totem
                elif mensagem['type'] == 'new_order':
                    # Uso do lock para garantir que a lista de pedidos seja acessada de forma segura
                    with self.bloqueio:
                        # Cria um novo pedido com um ID único e status "preparando"
                        id_pedido = len(self.pedidos) + 1
                        pedido = {'id': id_pedido, 'item': mensagem['item'], 'status': 'preparando'}
                        
                        # Adiciona o pedido à lista de pedidos
                        self.pedidos.append(pedido)
                        print(f"\nNovo pedido recebido: {pedido}")
                    
                    # Se a cozinha estiver registrada, notifica-a sobre o novo pedido
                    if self.clientes["kitchen"]:
                        self.clientes["kitchen"].send(json.dumps({'type': 'new_order', 'order': pedido}).encode('utf-8'))

                # Atualizar o status de um pedido na cozinha concluído
                elif mensagem['type'] == 'update_order':
                    # Uso do lock para garantir que a lista de pedidos seja acessada de forma segura
                    with self.bloqueio:
                        # Busca o pedido pelo ID e atualiza o status para "pronto"
                        for pedido in self.pedidos:
                            if pedido['id'] == mensagem['order_id']:
                                pedido['status'] = 'pronto'
                                print(f"Pedido {mensagem['order_id']} marcado como pronto")
                                break
                    
                    # Notifica a área de prontos sobre a atualização do status
                    if self.clientes["ready_area"]:
                        self.clientes["ready_area"].send(json.dumps({'type': 'order_ready', 'order_id': mensagem['order_id']}).encode('utf-8'))
                
                # Atualizar o status de um pedido na cozinha cancelado
                elif mensagem['type'] == 'canceled_order':
                    # Uso do lock para garantir que a lista de pedidos seja acessada de forma segura
                    with self.bloqueio:
                        # Busca o pedido pelo ID e atualiza o status para "pronto"
                        for pedido in self.pedidos:
                            if pedido['id'] == mensagem['order_id']:
                                pedido['status'] = 'pronto'
                                print(f"Pedido {mensagem['order_id']} marcado como cancelado")
                                break

                # Enviar a lista de pedidos para o cliente (área de prontos ou cozinha)
                elif mensagem['type'] == 'get_orders':
                    conn.send(json.dumps({'type': 'orders', 'orders': self.pedidos}).encode('utf-8'))
        except Exception as e:
            # Em caso de erro, exibe a mensagem de erro
            print(f"Erro: {e}")
        finally:
            # Fecha a conexão com o cliente
            conn.close()

    # Função para iniciar o servidor e esperar por conexões
    def iniciar(self):
        print("Aguardando por conexões...")
        # Loop contínuo para aceitar conexões de clientes
        while True:
            # Aceita uma nova conexão de um cliente
            conn, endereco = self.socket_servidor.accept()
            # Cria uma nova thread para tratar o cliente de forma independente
            threading.Thread(target=self.tratar_cliente, args=(conn, endereco)).start()


# Bloco principal que executa o servidor
if __name__ == "__main__":
    # Cria uma instância do servidor da padaria
    servidor = ServidorPadaria()
    
    # Inicia o servidor
    servidor.iniciar()
