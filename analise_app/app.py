import customtkinter as ctk
from database.db import criar_tabelas
from gui.main_window import MainWindow

def main():
    criar_tabelas()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
