import customtkinter as ctk
from database.db import conectar

class ListaCriancas(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Crianças Cadastradas")
        self.geometry("500x400")

        self.lista = ctk.CTkTextbox(self)
        self.lista.pack(fill="both", expand=True, padx=20, pady=20)

        self.carregar()

    def carregar(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome, data_nascimento, sexo, observacoes FROM crianca")
        registros = cursor.fetchall()

        conn.close()

        for r in registros:
            self.lista.insert("end", f"{r[0]} - {r[1]} ({r[2]})\n")
