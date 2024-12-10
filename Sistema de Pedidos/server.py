import socket
import threading
import json

class ServidorPadaria:
    
    def __init__(self, host='127.0.0.1', porta=65432):
        """
        Inicializa o servidor, configurando o socket e variáveis internas.
        """
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Criação do socket TCP/IP
        self.socket_servidor.bind((host, porta))                                  # Bind do socket ao endereço e porta fornecidos
        self.socket_servidor.listen(5)                                            # Modo de escuta, permitindo até 5 conexões simultâneas
        print(f"\nServidor online em {host}:{porta}")
        
        self.pedidos = []                                       # Lista para armazenar os pedidos recebidos
        self.clientes = {"kitchen": None, "ready_area": None}   # Dicionário de clientes registrados
        self.bloqueio = threading.Lock()                        # Lock para acesso seguro a recursos compartilhados


    def tratar_cliente(self, conn, endereco):
        """
        Trata a comunicação com cada cliente (cozinha ou área de prontos).
        """
        print(f"\nConectado à {endereco}")
        try:
            while True:
                # Recebe dados do cliente
                dados = conn.recv(1024).decode('utf-8')
                
                if not dados: 
                    break  
                
                # Converte os dados recebidos de JSON para dicionário Python
                mensagem = json.loads(dados)
                self.processar_mensagem(mensagem, conn)

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            conn.close()


    def processar_mensagem(self, mensagem, conn):
        """
        Processa a mensagem recebida do cliente e executa a ação apropriada.
        """
        tipo = mensagem['type']

        if   tipo == 'register': self.registrar_cliente(mensagem, conn)
        elif tipo == 'new_order': self.novo_pedido(mensagem)
        elif tipo == 'update_order': self.atualizar_pedido(mensagem)
        elif tipo == 'canceled_order': self.cancelar_pedido(mensagem)

    def registrar_cliente(self, mensagem, conn):
        """
        Registra um novo cliente (cozinha ou área de prontos).
        """
        self.clientes[mensagem['role']] = conn
        print(f"{mensagem['role']} registrado.")


    def novo_pedido(self, mensagem):
        """
        Processa um novo pedido e envia para a cozinha, se estiver registrada.
        """
        with self.bloqueio:
            id_pedido = len(self.pedidos) + 1
            pedido = {'id': id_pedido, 'item': mensagem['item'], 'status': 'preparando'}
            self.pedidos.append(pedido)
            print(f"\nNovo pedido recebido: {pedido}")
        
        if self.clientes["kitchen"]:
            # Mensagem de aviso de novo pedido
            notice_new_order_message = {'type': 'new_order', 'order': pedido}
            self.clientes["kitchen"].send(json.dumps(notice_new_order_message).encode('utf-8'))


    def atualizar_pedido(self, mensagem):
        """
        Atualiza o status de um pedido para "pronto" e notifica a área de prontos.
        """
        with self.bloqueio:
            for pedido in self.pedidos:
                if pedido['id'] == mensagem['order_id']:
                    pedido['status'] = 'pronto'
                    print(f"Pedido {mensagem['order_id']} marcado como pronto")
                    break

        if self.clientes["ready_area"]:
            # Mensagem de aviso de pedido pronto
            notice_ready_area_message = {'type': 'order_ready', 'order_id': mensagem['order_id']}
            self.clientes["ready_area"].send(json.dumps(notice_ready_area_message).encode('utf-8'))


    def cancelar_pedido(self, mensagem):
        """
        Marca um pedido como "cancelado".
        """
        with self.bloqueio:
            for pedido in self.pedidos:
                if pedido['id'] == mensagem['order_id']:
                    pedido['status'] = 'cancelado'
                    print(f"Pedido {mensagem['order_id']} marcado como cancelado")
                    break


    def enviar_pedidos(self, conn):
        """
        Envia a lista de pedidos para o cliente.
        """
        conn.send(json.dumps({'type': 'orders', 'orders': self.pedidos}).encode('utf-8'))


    def iniciar(self):
        """
        Inicia o servidor e espera por conexões.
        """
        print("Aguardando por conexões...")
        while True:
            conn, endereco = self.socket_servidor.accept()                               # Aceita nova conexão
            threading.Thread(target=self.tratar_cliente, args=(conn, endereco)).start()  # Cria nova thread para tratar o cliente


if __name__ == "__main__":
    servidor = ServidorPadaria()
    servidor.iniciar()
