import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from database.db import conectar
from models.avaliacao import Avaliacao

class Acompanhamento(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Acompanhamento")
        self.geometry("450x500")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Nova Avaliação",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(self, text="Criança").pack(pady=(10, 5))
        self.crianca_combo = ctk.CTkComboBox(self, values=[])
        self.crianca_combo.pack(fill="x", padx=40)

        ctk.CTkLabel(self, text="Peso (kg)").pack(pady=(15,5))
        self.peso_entry = ctk.CTkEntry(self)
        self.peso_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(self, text="Altura (m)").pack(pady=(15, 5))
        self.altura_entry = ctk.CTkEntry(self)
        self.altura_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(self, text="IMC").pack(pady=(15, 5))
        self.imc_label = ctk.CTkLabel(self, text="-", font=("Arial", 16))
        self.imc_label.pack()

        ctk.CTkButton(
            self,
            text="Calcular IMC",
            command=self.calcular_imc
            ).pack(pady=15)
        
        ctk.CTkButton(
            self,
            text="Salvar",
            command=self.salvar
        ).pack(pady=10)


        self.criancas = {}
        self.carregar_criancas()


    def carregar_criancas(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome FROM crianca")
        registros = cursor.fetchall()
        conn.close()

        if not registros:
            messagebox.showwarning(
                "Aviso",
                "Nenhuma criança cadastrada"
            )
            self.destroy()
            return
        
        nomes = []
        for cid, nome in registros:
            nomes.append(nome)
            self.criancas[nome] = cid

        self.crianca_combo.configure(values=nomes)
        self.crianca_combo.set(nome[0])


    def calcular_imc(self):
        try:
            peso = float(self.peso_entry.get())
            altura = float(self.altura_entry.get())

            avaliacao = Avaliacao(0, peso, altura)
            self.imc_label.configure(text=str(avaliacao.imc))

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Peso e altura devem ser números válidos"
            )
    
    def salvar(self):
        try:
            nome_crianca = self.crianca_combo.get()
            id_crianca = self.criancas[nome_crianca]

            peso = float(self.peso_entry.get())
            altura = float(self.altura_entry.get())

            avaliacao = Avaliacao(id_crianca, peso, altura)

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO avaliacao (id_crianca, data_avaliacao, peso, altura, imc)
            VALUES (?, ?, ?, ?, ?)
            """,(
                avaliacao.id_crianca,
                avaliacao.data_avaliacao,
                avaliacao.peso,
                avaliacao.altura,
                avaliacao.imc
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Sucesso!",
                "Avaliação salva"
            )
            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao salvar avaliacao:\n{e}"
            )
        