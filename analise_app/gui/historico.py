import customtkinter as ctk
from tkinter import messagebox
import csv
from tkinter import filedialog
from database.db import conectar
from gui.graficos import Grafico



class Historico(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Histórico de Avaliações")
        self.geometry("600x500")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Histórico Nutricional",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(self, text="Selecione a Criança").pack(pady=(10, 5))

        self.crianca_combo = ctk.CTkComboBox(self, values=[])
        self.crianca_combo.pack(fill="x", padx=40)

        ctk.CTkButton(
            self,
            text="Carregar Histórico",
            command=self.carregar_historico
        ).pack(pady=15)

        self.textbox = ctk.CTkTextbox(self, state="disabled")
        self.textbox.pack(fill="both", expand=True, padx=20, pady=10)

        self.criancas = {}
        self.carregar_criancas()

        self.btn_grafico = ctk.CTkButton(
            self,
            text="Ver gráfico",
            command=self.abrir_grafico
        )
        self.btn_grafico.pack(pady=10)

    def carregar_criancas(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome FROM crianca")
        registros = cursor.fetchall()
        conn.close()

        if not registros:
            messagebox.showwarning(
                "Aviso",
                "Nenhuma criança cadastrada."
            )
            self.destroy()
            return

        nomes = []
        for cid, nome in registros:
            nomes.append(nome)
            self.criancas[nome] = cid

        self.crianca_combo.configure(values=nomes)
        self.crianca_combo.set(nomes[0])

    def carregar_historico(self):
        nome = self.crianca_combo.get()
        id_crianca = self.criancas[nome]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT data_avaliacao, peso, altura, imc
            FROM avaliacao
            WHERE id_crianca = ?
            ORDER BY data_avaliacao
        """, (id_crianca,))

        registros = cursor.fetchall()
        conn.close()

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        if not registros:
            self.textbox.insert("end", "Nenhuma avaliação encontrada.\n")
        else:
            for data, peso, altura, imc in registros:
                self.textbox.insert(
                    "end",
                    f"{data} | Peso: {peso} kg | Altura: {altura} m | IMC: {imc}\n"
                )

        self.textbox.configure(state="disabled")

        ctk.CTkButton(
            self,
            text="Exportar CSV",
            command=self.exportar_csv,
            fg_color="green"
        ).pack(pady=5)

    def exportar_csv(self):
        nome = self.crianca_combo.get()
        id_crianca = self.criancas[nome]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT data_avaliacao, peso, altura, imc
            FROM avaliacao
            WHERE id_crianca = ?
            ORDER BY data_avaliacao
        """, (id_crianca,))

        registros = cursor.fetchall()
        conn.close()

        if not registros:
            messagebox.showwarning("Aviso", "Nenhuma avaliação para exportar.")
            return

        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")],
            initialfile=f"historico_{nome}.csv"
        )

        if not caminho:
            return

        with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["Data", "Peso (kg)", "Altura (m)", "IMC"])

            for registro in registros:
                writer.writerow(registro)

        messagebox.showinfo("Sucesso", "Arquivo exportado com sucesso!")


    def abrir_grafico(self):

        nome = self.crianca_combo.get()

        if not nome:
            return

        id_crianca = self.criancas.get(nome)

        if not id_crianca:
            return

        Grafico(self, id_crianca)

