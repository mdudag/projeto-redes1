import socket   
import json
from tkinter import Tk, Label, Button, Listbox, messagebox

class TotemClientMenuGUI:
    """
        Classe do totem do cliente, que mostra 
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Totem de Pedidos - Cardápio")
        self.master.geometry("400x400")
        
        # Conectar ao servidor
        self.host = '127.0.0.1'
        self.port = 65432
        self.connect_to_server()

        # Cardápio de itens
        self.menu_items = ["Pão Francês", "Café", "Bolo de Cenoura", "Torrada", "Suco de Laranja"]
        self.selected_items = []  # Lista para armazenar itens selecionados

        # GUI Elementos
        self.title_label = Label(master, text="Cardápio", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Botões para o cardápio
        for item in self.menu_items:
            Button(master, text=item, command=lambda i=item: self.add_to_order(i), width=20).pack(pady=5)

        # Lista de pedidos
        self.order_list_label = Label(master, text="Pedidos Selecionados:", font=("Arial", 12))
        self.order_list_label.pack(pady=10)

        self.order_listbox = Listbox(master, width=40, height=10)
        self.order_listbox.pack(pady=5)

        # Botões de ação
        self.send_button = Button(master, text="Enviar Pedido", command=self.send_order)
        self.send_button.pack(pady=10)

        self.exit_button = Button(master, text="Sair", command=self.master.quit)
        self.exit_button.pack(pady=5)

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            messagebox.showinfo("Conexão", "Conectado ao servidor!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            self.master.quit()

    def add_to_order(self, item):
        """Adiciona um item à lista de pedidos"""
        self.selected_items.append(item)
        self.order_listbox.insert("end", item)

    def send_order(self):
        """Envia os itens selecionados como um pedido único"""
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado.")
            return

        try:
            # Envia cada item da lista para o servidor
            for item in self.selected_items:
                message = {'type': 'new_order', 'item': item}
                self.client_socket.send(json.dumps(message).encode('utf-8'))
            
            messagebox.showinfo("Sucesso", "Pedido enviado com sucesso!")
            self.selected_items.clear()
            self.order_listbox.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar o pedido: {e}")
            self.master.quit()

if __name__ == "__main__":
    root = Tk()
    app = TotemClientMenuGUI(root)
    root.mainloop()
