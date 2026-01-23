import customtkinter as ctk
from gui.cadastro_crianca import CadastroCrianca
from gui.lista_criancas import ListaCriancas

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NutriKids")
        self.geometry("900x600")

        label = ctk.CTkLabel(
            self,
            text="Acompanhamento Nutricional",
            font=("Arial", 20)
        )
        label.pack(pady=40)

        ctk.CTkButton(
            self,
            text="Cadastrar Criança",
            command=self.abrir_cadastro
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Crianças Cadastradas",
            command=self.abrir_lista
        ).pack(pady=10)

    def abrir_cadastro(self):
        CadastroCrianca(self)

    def abrir_lista(self):
        ListaCriancas(self)
