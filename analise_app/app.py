import customtkinter as ctk
from database.db import criar_tabelas
from gui.main_window import MainWindow

ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

def main():
    criar_tabelas()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()    