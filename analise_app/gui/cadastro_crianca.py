import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database.db import conectar
from models.crianca import Crianca

class CadastroCrianca(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Cadastro da Criança")
        self.geometry("400x500")
        self.resizable(False, False)

        titulo = ctk.CTkLabel(
            self,
            text="Cadastro da Criança",
            font=("Arial", 20, "bold")
        )
        titulo.pack()

        self.nome_entry = self.campo("Nome completo")

        self.data_entry = self.campo("Data de nascimento")

        sexo_label = ctk.CTkLabel(self, text="Sexo")
        sexo_label.pack(pady=(15, 5))

        self.sexo_combox = ctk.CTkComboBox(
            self,
            values=["Feminino", "Masculino", "Outro"]
        )
        self.sexo_combox.pack(fill="x", padx=40)

        obs_label = ctk.CTkLabel(self, text="Observações")
        obs_label.pack(pady=(15, 5))

        self.obs_text = ctk.CTkTextbox(self, height=80)
        self.obs_text.pack(fill="x", padx=40)

        botoes_frame = ctk.CTkFrame(self)
        botoes_frame.pack(pady=30)

        salvar_btn = ctk.CTkButton(
            botoes_frame,
            text="Salvar",
            command=self.salvar
        )
        salvar_btn.pack(side="left", padx=10)

        cancelar_btn = ctk.CTkButton(
            botoes_frame,
            text="Cancelar",
            command=self.destroy
        )
        cancelar_btn.pack(side="left", padx=10)

    def campo(self, label_text):
        label = ctk.CTkLabel(self, text=label_text)
        label.pack(pady=(15, 5))

        entry = ctk.CTkEntry(self)
        entry.pack(fill="x", padx=40)

        return entry
    
    def salvar(self):
        nome = self.nome_entry.get()
        data = self.data_entry.get()
        sexo = self.sexo_combox.get()
        obs = self.obs_text.get("1.0", "end").strip()

        if not nome:
            messagebox.showerror("Error", "O nome é obrigatório!")
            return
        
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida. Use formato DD/MM/AAAA")
            return
        
        if not sexo:
            messagebox.showerror("Erro", "Selecione o sexo")

        print("Dados validados")

        crianca = Crianca(nome, data, sexo, obs)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        insert into crianca(nome, data_nascimento, sexo, observacoes)
        values(?, ?, ?, ?)
        """, (crianca.nome, crianca.data_nascimento, crianca.sexo, crianca.observacoes))

        conn.commit()
        conn.close()

        self.destroy()