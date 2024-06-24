# restaurante_app/sales.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Sales(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        search_frame = tk.Frame(self, bg='#2e2e2e')
        search_frame.pack(pady=10, padx=10, fill='x')

        # Search by order number
        order_number_label = tk.Label(search_frame, text="Buscar por número de comanda:", bg='#2e2e2e', fg='white')
        order_number_label.grid(row=0, column=0, padx=5, pady=5)
        self.order_number_var = tk.StringVar()
        order_number_entry = tk.Entry(search_frame, textvariable=self.order_number_var)
        order_number_entry.grid(row=0, column=1, padx=5, pady=5)
        search_by_number_button = tk.Button(search_frame, text="Buscar", command=self.search_by_order_number, bg='#2e2e2e', fg='white')
        search_by_number_button.grid(row=0, column=2, padx=5, pady=5)

        # Search by date
        date_label = tk.Label(search_frame, text="Buscar por fecha (YYYY-MM-DD):", bg='#2e2e2e', fg='white')
        date_label.grid(row=1, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar()
        date_entry = tk.Entry(search_frame, textvariable=self.date_var)
        date_entry.grid(row=1, column=1, padx=5, pady=5)
        search_by_date_button = tk.Button(search_frame, text="Buscar", command=self.search_by_date, bg='#2e2e2e', fg='white')
        search_by_date_button.grid(row=1, column=2, padx=5, pady=5)

        # Treeview for displaying orders
        self.orders_tree = ttk.Treeview(self, columns=('Order Number', 'Table Number', 'Date', 'Total'), show='headings')
        self.orders_tree.heading('Order Number', text='Número de Comanda')
        self.orders_tree.heading('Table Number', text='Número de Mesa')
        self.orders_tree.heading('Date', text='Fecha')
        self.orders_tree.heading('Total', text='Total')
        self.orders_tree.pack(pady=10, padx=10, fill='both', expand=True)
        self.orders_tree.bind("<Double-1>", self.on_order_double_click)

        # Treeview for displaying order details
        self.details_tree = ttk.Treeview(self, columns=('Product Name', 'Quantity', 'Unit Price', 'Total Price'), show='headings')
        self.details_tree.heading('Product Name', text='Nombre del Producto')
        self.details_tree.heading('Quantity', text='Cantidad')
        self.details_tree.heading('Unit Price', text='Precio Unitario')
        self.details_tree.heading('Total Price', text='Precio Total')
        self.details_tree.pack(pady=10, padx=10, fill='both', expand=True)

    def search_by_order_number(self):
        order_number = self.order_number_var.get()
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, table_number, order_date, SUM(total_price)
            FROM orders
            WHERE id = ?
            GROUP BY id, table_number, order_date
        ''', (order_number,))
        orders = cursor.fetchall()
        conn.close()

        self.display_orders(orders)

    def search_by_date(self):
        date = self.date_var.get()
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, table_number, order_date, SUM(total_price)
            FROM orders
            WHERE order_date LIKE ?
            GROUP BY id, table_number, order_date
        ''', (f'{date}%',))
        orders = cursor.fetchall()
        conn.close()

        self.display_orders(orders)

    def display_orders(self, orders):
        for i in self.orders_tree.get_children():
            self.orders_tree.delete(i)
        
        for order in orders:
            self.orders_tree.insert('', 'end', values=order)

    def on_order_double_click(self, event):
        selected_item = self.orders_tree.selection()[0]
        order_number = self.orders_tree.item(selected_item, 'values')[0]

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT product_name, quantity, unit_price, total_price
            FROM orders
            WHERE id = ?
        ''', (order_number,))
        order_details = cursor.fetchall()
        conn.close()

        self.display_order_details(order_details)

    def display_order_details(self, order_details):
        for i in self.details_tree.get_children():
            self.details_tree.delete(i)
        
        for detail in order_details:
            self.details_tree.insert('', 'end', values=detail)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ventas de Comandas")
    root.geometry("800x600")
    root.configure(bg='#2e2e2e')

    sales_frame = Sales(root, None)
    sales_frame.pack(fill='both', expand=True)

    root.mainloop()

