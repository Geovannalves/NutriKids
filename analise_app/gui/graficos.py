import customtkinter as ctk
import sqlite3
from database.db import conectar

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Grafico(ctk.CTkToplevel):

    def __init__(self, master, id_crianca):
        super().__init__(master)

        self.title("Gráfico de Evolução")
        self.geometry("700x500")

        self.id_crianca = id_crianca

        self.carregar_dados()


    def carregar_dados(self):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT data_avaliacao, peso, imc
            FROM avaliacao
            WHERE id_crianca = ?
            ORDER BY data_avaliacao
        """, (self.id_crianca,))

        dados = cursor.fetchall()
        conn.close()

        if not dados:
            label = ctk.CTkLabel(
                self,
                text="Nenhum dado para exibir gráfico"
            )
            label.pack(pady=20)
            return

        datas = [linha[0] for linha in dados]
        pesos = [linha[1] for linha in dados]
        imcs = [linha[2] for linha in dados]

        self.criar_grafico(datas, pesos, imcs)


    def criar_grafico(self, datas, pesos, imcs):

        fig, ax = plt.subplots(figsize=(6,4))

        ax.plot(datas, pesos, marker="o", label="Peso (kg)")
        ax.plot(datas, imcs, marker="o", label="IMC")

        ax.set_title("Evolução Nutricional")
        ax.set_xlabel("Data")
        ax.set_ylabel("Valor")

        ax.legend()
        ax.grid(True)

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
    
    def destroy(self):
        try:
            self.canvas.get_tk_widget().destroy()
        except:
            pass

        super().destroy()

