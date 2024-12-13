import socket
import json
from tkinter import Tk, Label, Button, Listbox, Frame, Scrollbar, messagebox, END, RIGHT, Y
import threading

class KitchenClientGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Totem da Cozinha")
        self.master.geometry("500x600")
        self.master.configure(bg="#ADD8E6")

        # Tamanho mínimo e máximo da tela
        self.master.minsize(width=500, height=600)
        self.master.maxsize(width=800, height=800)

        # Rótulo de título
        self.title_label = Label(self.master, text="Pedidos da Cozinha", font=("Arial", 18), bg="#ADD8E6")
        self.title_label.pack(pady=10)

        # Frame principal
        self.frame_main = Frame(self.master, bg="#ADD8E6")
        self.frame_main.place(relx=0.1, rely=0.13, relwidth=0.8, relheight=0.68)

        # Lista para exibir pedidos
        self.listbox = Listbox(self.frame_main, width=40, height=4, bg="#E0FFFF", font=("Arial", 13))
        self.listbox.pack(side="left", fill="both", expand=True)

        # Barra de rolagem para a lista
        self.scrollbar = Scrollbar(self.frame_main, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Botões de ação para marcar pedido como concluído ou cancelado
        self.frame_buttons = Frame(self.master, bd=4, bg="#ADD8E6")
        self.frame_buttons.place(relx=0.1, rely=0.83, relwidth=0.8, relheight=0.1)

        self.button_cancel = Button(self.frame_buttons, text="Cancelar Pedido", command=self.mark_cancel, bg="#4682B4", fg="white")
        self.button_cancel.place(relx=0.08, rely=0.3, relwidth=0.4, relheight=0.52)

        self.button_done = Button(self.frame_buttons, text="Concluir Pedido", command=self.mark_done, bg="#4682B4", fg="white")
        self.button_done.place(relx=0.52, rely=0.3, relwidth=0.4, relheight=0.52)

        # Iniciar a thread para o cliente socket
        self.start_client_thread()


    def start_client_thread(self):
        """
            Método para iniciar o cliente em uma thread separada para evitar travar a interface.
        """
        client_thread = threading.Thread(target=self.connect_to_server)
        client_thread.daemon = True
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

                # Envio da mensagem que registra no servidor como área de preparo
                register_message = {'type': 'register', 'role': 'kitchen'}
                s.send(json.dumps(register_message).encode('utf-8'))

                self.client_socket = s
                self.receive_orders()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            self.master.quit()


    def receive_orders(self):
        """
            Método para receber novos pedidos e os adicionar à lista de pedidos.
        """
        while True:
            data = self.client_socket.recv(1024).decode('utf-8')
            message = json.loads(data)

            # Mensagem do tipo novo pedido
            if message['type'] == 'new_order':  
                order = message['order']
                order_message = f"Pedido nº {order['id']} - Itens: {', '.join(order['item'])}"
                self.listbox.insert(END, order_message)


    def mark_done(self):
        """
            Método para marcar o pedido como concluído e enviar mensagem para
            atualizar totem de pedidos prontos.
        """
        try:
            selected_order = self.listbox.curselection()
            if not selected_order:
                messagebox.showwarning("Aviso", "Nenhum pedido selecionado.")
                return

            order_message = self.listbox.get(selected_order[0])
            order_id = order_message.split(" ")[2]              # Extrair o ID do pedido da mensagem

            # Enviar mensagem para atualizar o pedido como concluído no servidor
            update_order_message = {'type': 'update_order', 'order_id': order_id}
            self.client_socket.send(json.dumps(update_order_message).encode('utf-8'))

            # Remover pedido da lista após marcar como concluído
            self.listbox.delete(selected_order)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao marcar como concluído: {e}")


    def mark_cancel(self):
        """
            Método para marcar o pedido como cancelado.
        """
        try:
            selected_order = self.listbox.curselection()
            if not selected_order:
                messagebox.showwarning("Aviso", "Nenhum pedido selecionado.")
                return

            order_message = self.listbox.get(selected_order[0])
            order_id = order_message.split(" ")[2]              # Extrair o ID do pedido da mensagem

            # Enviar mensagem para atualizar o pedido como cancelado no servidor
            canceled_order_message = {'type': 'canceled_order', 'order_id': order_id}
            self.client_socket.send(json.dumps(canceled_order_message).encode('utf-8'))

            # Remover pedido da lista após marcar como cancelado
            self.listbox.delete(selected_order)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cancelar o pedido: {e}")


if __name__ == "__main__":
    root = Tk()
    app = KitchenClientGUI(root)
    root.mainloop()
