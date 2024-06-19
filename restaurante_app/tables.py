import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Inicialización de la base de datos
def initialize_database():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER,
            product_name TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL,
            order_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()

class Tables(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#4e4e4e')
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Mesas", font=('Arial', 18), bg='#4e4e4e', fg='white')
        label.pack(pady=10, padx=10)

        # Crear botones para cada mesa
        button_frame = tk.Frame(self, bg='#4e4e4e')
        button_frame.pack(pady=10, padx=10)

        for i in range(1, 61):
            button = tk.Button(button_frame, text=f"Mesa {i}", command=lambda i=i: self.open_table(i), bg='#4e4e4e', fg='white')
            button.grid(row=(i-1)//10, column=(i-1)%10, padx=5, pady=5)

    def open_table(self, table_number):
        TableWindow(self, table_number)

class TableWindow(tk.Toplevel):
    def __init__(self, parent, table_number):
        super().__init__(parent)
        self.title(f"Orden de Mesa {table_number}")
        self.geometry("800x600")
        self.configure(bg='#4e4e4e')
        self.table_number = table_number

        self.product_name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()

        # Fecha y hora de creación de la comanda
        self.order_datetime = datetime.now()
        self.order_number = self.generate_order_number()

        self.create_widgets()
        self.load_inventory()

    def generate_order_number(self):
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) FROM orders')
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            return result[0] + 1
        return 1

    def create_widgets(self):
        # Scrollbar
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas para contener todos los widgets
        canvas = tk.Canvas(self, bg='#4e4e4e', yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        # Frame para los widgets dentro del canvas
        frame = tk.Frame(canvas, bg='#4e4e4e')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Título "NOTA DE CUENTA"
        title_label = tk.Label(frame, text="NOTA DE CUENTA", font=('Arial', 18, 'bold'), bg='#4e4e4e', fg='white')
        title_label.pack(pady=5)

        # Crear sombreado (opción con relieve de borde)
        title_label.configure(relief="solid", bd=1)

        # Mostrar número de comanda, fecha y hora
        order_info_frame = tk.Frame(frame, bg='#4e4e4e')
        order_info_frame.pack(pady=5)

        order_number_label = tk.Label(order_info_frame, text=f"Número de Comanda: {self.order_number}", bg='#4e4e4e', fg='white')
        order_number_label.grid(row=0, column=0, padx=5)

        table_number_label = tk.Label(order_info_frame, text=f"Orden de Mesa: {self.table_number}", bg='#4e4e4e', fg='white')
        table_number_label.grid(row=1, column=0, padx=5)

        order_date_label = tk.Label(order_info_frame, text=f"Fecha: {self.order_datetime.strftime('%Y-%m-%d')}", bg='#4e4e4e', fg='white')
        order_date_label.grid(row=2, column=0, padx=5)

        order_time_label = tk.Label(order_info_frame, text=f"Hora: {self.order_datetime.strftime('%H:%M:%S')}", bg='#4e4e4e', fg='white')
        order_time_label.grid(row=3, column=0, padx=5)

        product_name_label = tk.Label(frame, text="Nombre del Producto:", bg='#4e4e4e', fg='white')
        product_name_label.pack(pady=5)
        self.product_name_entry = ttk.Combobox(frame, textvariable=self.product_name_var)
        self.product_name_entry.pack(pady=5)

        quantity_label = tk.Label(frame, text="Cantidad:", bg='#4e4e4e', fg='white')
        quantity_label.pack(pady=5)
        quantity_entry = tk.Entry(frame, textvariable=self.quantity_var, bg='#4e4e4e', fg='white')
        quantity_entry.pack(pady=5)

        add_button = tk.Button(frame, text="Agregar Producto", command=self.add_product, bg='#4e4e4e', fg='white')
        add_button.pack(pady=10)

        self.tree = ttk.Treeview(frame, columns=('Nombre', 'Cantidad', 'Precio', 'Total'), show='headings')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Total', text='Total')
        self.tree.pack(pady=10, padx=10, fill='both', expand=True)

        self.tree.bind("<Double-1>", self.on_item_double_click)

        self.summary_frame = tk.Frame(frame, bg='#4e4e4e')
        self.summary_frame.pack(pady=10, padx=10, fill='x')

        self.net_total_var = tk.DoubleVar()
        self.tax_var = tk.DoubleVar()
        self.tip_var = tk.DoubleVar()
        self.total_var = tk.DoubleVar()

        net_total_label = tk.Label(self.summary_frame, text="Valor Neto:", bg='#4e4e4e', fg='white')
        net_total_label.grid(row=0, column=0, pady=5, padx=5)
        net_total_value = tk.Label(self.summary_frame, textvariable=self.net_total_var, bg='#4e4e4e', fg='white')
        net_total_value.grid(row=0, column=1, pady=5, padx=5)

        tax_label = tk.Label(self.summary_frame, text="IVA 19%:", bg='#4e4e4e', fg='white')
        tax_label.grid(row=1, column=0, pady=5, padx=5)
        tax_value = tk.Label(self.summary_frame, textvariable=self.tax_var, bg='#4e4e4e', fg='white')
        tax_value.grid(row=1, column=1, pady=5, padx=5)

        tip_label = tk.Label(self.summary_frame, text="Propina 10%:", bg='#4e4e4e', fg='white')
        tip_label.grid(row=2, column=0, pady=5, padx=5)
        tip_value = tk.Label(self.summary_frame, textvariable=self.tip_var, bg='#4e4e4e', fg='white')
        tip_value.grid(row=2, column=1, pady=5, padx=5)

        total_label = tk.Label(self.summary_frame, text="Valor Total:", bg='#4e4e4e', fg='white')
        total_label.grid(row=3, column=0, pady=5, padx=5)
        total_value = tk.Label(self.summary_frame, textvariable=self.total_var, bg='#4e4e4e', fg='white')
        total_value.grid(row=3, column=1, pady=5, padx=5)

        button_frame = tk.Frame(frame, bg='#4e4e4e')
        button_frame.pack(pady=10, padx=10, fill='x')

        save_button = tk.Button(button_frame, text="Guardar", command=self.save_order, bg='#4e4e4e', fg='white')
        save_button.pack(side='left', padx=5)

        print_button = tk.Button(button_frame, text="Imprimir", command=self.print_order, bg='#4e4e4e', fg='white')
        print_button.pack(side='left', padx=5)

        close_button = tk.Button(button_frame, text="Cerrar", command=self.destroy, bg='#4e4e4e', fg='white')
        close_button.pack(side='left', padx=5)

    def load_inventory(self):
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM inventory')
        products = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.product_name_entry['values'] = products

    def add_product(self):
        product_name = self.product_name_var.get()
        quantity = self.quantity_var.get()

        if not product_name or quantity <= 0:
            messagebox.showwarning("Advertencia", "Debe ingresar un producto y una cantidad válida.")
            return

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT quantity, price FROM inventory WHERE name = ?', (product_name,))
        result = cursor.fetchone()

        if not result:
            messagebox.showwarning("Advertencia", "Producto no encontrado en el inventario.")
            conn.close()
            return

        available_quantity, unit_price = result

        if quantity > available_quantity:
            messagebox.showwarning("Advertencia", "No hay suficiente inventario para este producto.")
            conn.close()
            return

        total_price = unit_price * quantity

        # Descontar la cantidad del inventario
        new_quantity = available_quantity - quantity
        cursor.execute('UPDATE inventory SET quantity = ? WHERE name = ?', (new_quantity, product_name))
        conn.commit()
        conn.close()

        self.tree.insert('', 'end', values=(product_name, quantity, unit_price, total_price))
        self.update_totals()

    def update_totals(self):
        net_total = sum(float(self.tree.set(item, 'Total')) for item in self.tree.get_children())
        tax = net_total * 0.19
        tip = net_total * 0.10
        total = net_total + tax + tip

        self.net_total_var.set(f"{net_total:.2f}")
        self.tax_var.set(f"{tax:.2f}")
        self.tip_var.set(f"{tip:.2f}")
        self.total_var.set(f"{total:.2f}")

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, 'values')

        product_name, quantity = item_values[0], int(item_values[1])
        response = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar {quantity} de {product_name}?")

        if response:
            self.tree.delete(selected_item)
            self.update_totals()

    def save_order(self):
        order_items = [self.tree.item(item, 'values') for item in self.tree.get_children()]
        if not order_items:
            messagebox.showwarning("Advertencia", "No hay productos en la orden para guardar.")
            return

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        for item in order_items:
            product_name, quantity, unit_price, total_price = item
            cursor.execute('''
                INSERT INTO orders (table_number, product_name, quantity, unit_price, total_price, order_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.table_number, product_name, quantity, unit_price, total_price, self.order_datetime))

        conn.commit()
        conn.close()

        messagebox.showinfo("Información", "Orden guardada exitosamente.")

    def print_order(self):
        messagebox.showinfo("Información", "Función de impresión no implementada.")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Comandas")
        self.geometry("1200x800")
        self.configure(bg='#4e4e4e')

        self.frames = {}
        container = tk.Frame(self, bg='#4e4e4e')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frame = Tables(container, self)
        self.frames[Tables] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Tables)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
