import socket   
import json
from tkinter import Tk, Label, Button, Listbox, Scrollbar, Frame, messagebox, RIGHT, LEFT, Y, BOTH, END

class TotemClientMenuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Totem de Pedidos - Cardápio")
        self.master.geometry("400x600")  # Ajustado para comportar mais itens

        # Alterar a cor de fundo para azul claro
        self.master.configure(bg="#ADD8E6")  # Cor em hexadecimal para azul claro

        # Conectar ao servidor
        self.host = '127.0.0.1'
        self.port = 65432
        self.connect_to_server()

        # Cardápio de itens
        self.menu_items = [
            "Pão Francês", "Bolo de Cenoura", "Torrada",
            "Pão de Queijo", "Misto Quente", "Café", "Suco de Laranja", "Café com leite"
        ]
        self.selected_items = []  # Lista para armazenar itens selecionados

        # GUI Elementos
        self.title_label = Label(master, text="Cardápio", font=("Arial", 16), bg="#ADD8E6")
        self.title_label.pack(pady=10)

        # Botões para o cardápio
        for item in self.menu_items:
            Button(master, text=item, command=lambda i=item: self.add_to_order(i), width=20, bg="#87CEEB", fg="white").pack(pady=5)

        # Lista de pedidos com barra de rolagem
        self.order_list_label = Label(master, text="Pedidos Selecionados:", font=("Arial", 12), bg="#ADD8E6")
        self.order_list_label.pack(pady=10)

        # Frame para a lista e barra de rolagem (centralizado)
        list_frame = Frame(master, bg="#ADD8E6")
        list_frame.pack(pady=10)

        self.order_listbox = Listbox(list_frame, width=30, height=6, bg="#E0FFFF", yscrollcommand=lambda *args: self.scrollbar.set(*args))
        self.order_listbox.pack(side=LEFT)

        self.scrollbar = Scrollbar(list_frame, orient="vertical", command=self.order_listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Botões de ação
        self.send_button = Button(master, text="Enviar Pedido", command=self.send_order, bg="#4682B4", fg="white")
        self.send_button.pack(pady=10)

        self.exit_button = Button(master, text="Sair", command=self.master.quit, bg="#4682B4", fg="white")
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
        self.order_listbox.insert(END, item)

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
            self.order_listbox.delete(0, END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar o pedido: {e}")
            self.master.quit()

if __name__ == "__main__":
    root = Tk()
    app = TotemClientMenuGUI(root)
    root.mainloop()
