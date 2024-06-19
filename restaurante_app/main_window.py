# restaurante_app/main_window.py
import tkinter as tk
from tkinter import ttk
from restaurante_app.inventory import Inventory
from restaurante_app.tables import Tables
from restaurante_app.sales import Sales

class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Restaurante App")
        self.geometry("800x600")
        self.configure(bg='#2e2e2e')

        # Estilo de las pestañas
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TNotebook", background='#2e2e2e', borderwidth=0)
        style.configure("TNotebook.Tab", background='#2e2e2e', foreground='white', padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", '#4e4e4e')])

        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, expand=True)
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Pestañas
        self.frames = {}
        for F in (Home, Inventory, Tables, Sales):
            page_name = F.__name__
            frame = F(parent=notebook, controller=self)
            notebook.add(frame, text=page_name)
            self.frames[page_name] = frame

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_tab_changed(self, event):
        selected_tab = event.widget.tab('current')['text']
        if selected_tab == 'Inventory':
            self.frames['Inventory'].load_data()

class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = controller
        label = tk.Label(self, text="Bienvenido al Restaurante App", font=('Arial', 18), bg='#2e2e2e', fg='white')
        label.pack(pady=10, padx=10)

if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()
