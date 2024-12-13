import socket
import json
from tkinter import Tk, Label, Listbox, Frame, Scrollbar, messagebox, END, RIGHT, Y
import threading

class ReadyAreaGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Totem de Pedidos Prontos")
        self.master.geometry("350x400")
        self.master.configure(bg="#ADD8E6")

        # Tamanho mínimo e máximo da tela
        self.master.minsize(width=350, height=400)
        self.master.maxsize(width=350, height=400)

        # Rótulo de título
        self.title_label = Label(self.master, text="Pedidos Prontos", font=("Arial", 18), bg="#ADD8E6")
        self.title_label.pack(pady=10)

        # Frame principal
        self.frame_main = Frame(self.master, bg="#ADD8E6")
        self.frame_main.pack(pady=10, padx=10, fill='both', expand=True)

        # Lista para exibir pedidos prontos
        self.listbox = Listbox(self.frame_main, width=60, height=15, bg="#E0FFFF", font=("Arial", 13))
        self.listbox.pack(side="top", fill="both", expand=True)

        # Definir limite de itens na Listbox
        self.max_items = 15

        # Iniciar a thread para o cliente socket
        self.start_client_thread()


    def start_client_thread(self):
        """
            Método para iniciar o cliente em uma thread separada para evitar travar a interface.
        """
        
        # Conexão com o servidor é processada em paralelo, sem bloquear a interface gráfica.
        client_thread = threading.Thread(target=self.connect_to_server)
        # A conexão encerra com o fechamento da interface
        client_thread.daemon = True
        # Inicia execução da linha de execução independente
        client_thread.start()


    def connect_to_server(self):
        """
            Método para gerenciar a conexão com o servidor.
        """
        # Configuração do servidor para conexão
        host = '127.0.0.1'
        port = 65432

        try:
            # Criando objeto socket com tipo de endereço de rede IPv4 e protocolo TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port)) 
                messagebox.showinfo("Conexão", "Conectado ao servidor!")

                # Envio da mensagem que registra no servidor como área de pedidos prontos
                register_message = {'type': 'register', 'role': 'ready_area'}
                s.send(json.dumps(register_message).encode('utf-8'))

                while True:
                    data = s.recv(1024).decode('utf-8')
                    message = json.loads(data)

                    # Mensagem do tipo pedido pronto
                    if message['type'] == 'order_ready':
                        order_message = f"Pedido nº {message['order_id']}"
                        self.add_message(order_message)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            self.master.quit()

    
    def add_message(self, message):
        """
            Método para adicionar uma mensagem centralizada à Listbox 
            e remover mensagens antigas, se ultrapassar o limite.
        """

        # Remove o item mais antigo, se tiver passado do limite
        if self.listbox.size() >= self.max_items:
            self.listbox.delete(0)

        # Centraliza o texto
        width = self.listbox.cget("width")          # Largura do Listbox
        centered_message = message.center(width)    # Centraliza o texto com base na largura
        self.listbox.insert(END, centered_message)



if __name__ == "__main__":
    root = Tk()
    app = ReadyAreaGUI(root)
    root.mainloop()
