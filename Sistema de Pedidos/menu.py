import socket
import json
from tkinter import Tk, Label, Button, Listbox, Scrollbar, Frame, messagebox, RIGHT, LEFT, Y, END
import time

class TotemClientMenuGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Totem de Pedidos - Cardápio")    # Título da janela principal
        self.master.geometry("500x600")                     # Tamanho da janela
        self.master.configure(bg="#ADD8E6")                 # Cor de fundo azul claro

        # Tamanho mínimo e máximo da tela
        self.master.minsize(width=500, height=600)
        self.master.maxsize(width=800, height=650)

        # Configuração do servidor para conexão
        self.host = '127.0.0.1'
        self.port = 65432
        self.connect_to_server()

        self.selected_items = []  # Lista para armazenar itens selecionados do menu

        # Inicialização dos componentes da GUI
        self.create_main_layout()       
        self.create_food_section()
        self.create_drink_section()
        self.create_order_section()
        self.create_action_buttons()


    def connect_to_server(self):
        """
            Método para conectar ao servidor especificado
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            messagebox.showinfo("Conexão", "Conectado ao servidor!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            self.master.quit()


    def create_main_layout(self):
        """
            Método para criar o layout principal da interface.
        """
        # Cria o título principal
        self.title_label = Label(self.master, text="Cardápio", font=("Arial", 18), bg="#ADD8E6")
        self.title_label.pack(pady=10)  # Espaçamento superior

        # Frame principal para os componentes
        self.frame_main = Frame(self.master, bd=4, bg="#ADD8E6")
        self.frame_main.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)


    def create_food_section(self):
        """
            Método para criar a seção de comidas.
        """
        # Cria o frame para a seção de comidas
        self.frame_comidas = self.create_section(self.frame_main, 0.1, 0.02, "Comidas")

        # Frame interno para os botões de comidas
        self.frame_1 = Frame(self.frame_main, bd=4, bg="#ADD8E6", highlightbackground="black", highlightthickness=1)
        self.frame_1.place(relx=0.1, rely=0.08, relwidth=0.35, relheight=0.41)

        # Lista de itens de comida e suas posições relativas
        food_items = [
            ("Biscoito", 0),
            ("Bolo de Cenoura", 0.175),
            ("Misto Quente", 0.345),
            ("Pão Francês", 0.518),
            ("Torrada", 0.69),
            ("Torta de Frango", 0.86)
        ]
        self.create_buttons(self.frame_1, food_items)  # Cria os botões dinamicamente


    def create_drink_section(self):
        """
            Método para criar a seção de bebidas.
        """
        # Cria o frame para a seção de bebidas
        self.frame_bebidas = self.create_section(self.frame_main, 0.55, 0.02, "Bebidas")

        # Frame interno para os botões de bebidas
        self.frame_2 = Frame(self.frame_main, bd=4, bg="#ADD8E6", highlightbackground="black", highlightthickness=1)
        self.frame_2.place(relx=0.55, rely=0.08, relwidth=0.35, relheight=0.41)

        # Lista de itens de bebidas e suas posições relativas
        drink_items = [
            ("Café", 0),
            ("Café com leite", 0.175),
            ("Capuccino", 0.345),
            ("Chocolate Quente", 0.518),
            ("Leite Gelado", 0.69),
            ("Suco de Fruta", 0.86)
        ]
        self.create_buttons(self.frame_2, drink_items)  # Cria os botões dinamicamente


    def create_section(self, parent, relx, rely, title):
        """
            Método para criar seções.
        """
        # Cria uma seção com título
        frame = Frame(parent, bd=4, bg="#ADD8E6")
        frame.place(relx=relx, rely=rely, relwidth=0.35, relheight=0.06)
        Label(frame, text=title, font=("Arial", 12), bg="#ADD8E6").place(relx=0.5, rely=0.5, anchor="center")

        return frame


    def create_buttons(self, parent, items):
        """
            Método para criar botões.
        """
        # Cria botões para os itens fornecidos
        for text, rel_y in items:
            Button(parent, text=text, bg="#444554", fg="white", command=lambda t=text: self.add_to_order(t)).place(
                relx=0, rely=rel_y, relwidth=1, relheight=0.14)
            

    def add_to_order(self, item):
        """
            Método para adicionar um item à lista de pedidos selecionados.
        """
        self.selected_items.append(item)
        self.order_listbox.insert(END, item)


    def create_order_section(self):
        """
            Método para criar a seção de pedidos.
        """
        # Frame para a lista de pedidos com barra de rolagem
        self.frame_barra_rolagem = Frame(self.frame_main, bd=4, bg="#ADD8E6")
        self.frame_barra_rolagem.place(relx=0.25, rely=0.55, relwidth=0.5, relheight=0.35)

        # Rótulo para o título da lista de pedidos
        self.order_list_label = Label(self.frame_barra_rolagem, text="Pedidos Selecionados:", font=("Arial", 12), bg="#ADD8E6")
        self.order_list_label.pack(pady=5)

        # Frame interno para a lista e barra de rolagem
        list_frame = Frame(self.frame_barra_rolagem, bg="#ADD8E6")
        list_frame.pack(pady=10)

        # Lista para exibir os itens selecionados
        self.order_listbox = Listbox(list_frame, width=30, height=6, bg="#E0FFFF")
        self.order_listbox.pack(side=LEFT)

        # Barra de rolagem vertical
        self.scrollbar = Scrollbar(list_frame, orient="vertical", command=self.order_listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.order_listbox.config(yscrollcommand=self.scrollbar.set)  # Conecta a barra de rolagem à lista


    def create_action_buttons(self):
        """
            Método para criar a seção de botões de ação de enviar pedido e 
            sair, para fechar a interface.
        """
        # Frame para os botões "Enviar Pedido" e "Sair"
        self.frame_button_send_exit = Frame(self.frame_main, bd=4, bg="#ADD8E6")
        self.frame_button_send_exit.place(relx=0.1, rely=0.92, relwidth=0.8, relheight=0.1)

        # Botão "Sair"
        self.exit_button = Button(self.frame_button_send_exit, text="Sair", command=self.master.quit, bg="#4682B4", fg="white")
        self.exit_button.place(relx=0.18, rely=0.3, relwidth=0.2, relheight=0.7)

        # Botão "Enviar Pedido"
        self.send_button = Button(self.frame_button_send_exit, text="Enviar Pedido", command=self.send_order, bg="#4682B4", fg="white")
        self.send_button.place(relx=0.42, rely=0.3, relwidth=0.4, relheight=0.7)


    def send_order(self):
        """
            Método para enviar os itens selecionados como um pedido.
        """
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado.")
            return

        try:
            items = self.selected_items
            new_order_message = {'type': 'new_order', 'item': items}
            self.client_socket.send(json.dumps(new_order_message).encode('utf-8'))
            time.sleep(0.1)  # Adiciona um pequeno atraso entre os envios

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
