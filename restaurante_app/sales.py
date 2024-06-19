# restaurante_app/sales.py
import tkinter as tk

class Sales(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = controller
        label = tk.Label(self, text="Ventas", font=('Arial', 18), bg='#2e2e2e', fg='white')
        label.pack(pady=10, padx=10)
